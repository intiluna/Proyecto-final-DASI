"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
#from flask import Flask, request, jsonify, url_for, Blueprint
#from api.models import db, User
#from api.utils import generate_sitemap, APIException
#
import os
from flask import Flask, request, jsonify, url_for, Blueprint
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
#from utils import APIException, generate_sitemap
# from admin import setup_admin
from api.models import db, User, ProductoNombre,Producto,PerfilProductor,Pedido
#from models import Person
#for authentication
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
#for checking email
import re
#for geocode /#Importing the Nominatim geocoder class 
from geopy.geocoders import Nominatim
import time
# for sending email
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


api = Blueprint('api', __name__)

#funciones generales
def validar_email(email):
            # Patrón de expresión regular para validar el email
            patron_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            
            # Usamos re.match() para verificar el patrón en el email proporcionado
            if re.match(patron_email, email):
                return True
            else:
                return False

@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200


# probando acceso a bd
@api.route('/users', methods=['GET'])
def get_all_users():

    users_query = User.query.all()
    results = list(map(lambda item: item.serialize(), users_query))

    response_body = {
       "results": results
    }

    return jsonify(response_body), 200


# -------------------- CREAR PRODUCTO --------------------

@api.route('/producto', methods=['POST'])
def add_producto():

    request_body = request.get_json(force=True)

    producto = Producto(
        nombre= request_body ['nombre'],
        cantidad= request_body['cantidad'],
        unidad_medida= request_body['unidad_medida'],
        variedad= request_body['variedad'],
        tipo_produccion= request_body['tipo_produccion'],
        recogida= request_body['recogida'],
        precio= request_body['precio'],
        productor_id= request_body['productor_id']
    )
    
    db.session.add(producto)
    db.session.commit()


    response_body = {
        'msg':'ok',
        "result": {'Producto Created': producto.serialize()}
    }

    return jsonify(response_body), 200


# -------------------- ELIMINAR PRODUCTO --------------------

@api.route('/producto/<int:id>', methods=['DELETE'])
def del_producto(id):
 

    producto_query= Producto.query.filter_by(id=id).first()
    
    if producto_query is None:
        return jsonify({"msg": "the product does not exist"})

    db.session.delete(producto_query)
    db.session.commit()


    response_body = {
        'msg':'ok',
        "results": 'Product deleted'
    }
    
    
    return jsonify(response_body), 200

# -------------------- EDITAR PRODUCTO --------------------

@api.route('/producto/<int:id>', methods=['PUT'])
def edit_product(id):

    body = request.get_json(force=True) #{ 'username': 'new_username'}

    product1 = Producto.query.get(id)
    product1.nombre = body["nombre"]
    product1.variedad = body["variedad"]
    product1.cantidad = body["cantidad"]
    product1.unidad_medida = body["unidad_medida"]
    product1.precio = body["precio"]
    product1.recogida = body["recogida"]
    product1.tipo_produccion = body["tipo_produccion"]

    db.session.commit()

    if product1.nombre is None:
        return jsonify({"msg": "the product does not exist"})

    return jsonify(product1.serialize()), 200

    

#get lista de productoNombre
@api.route('/producto', methods=['Get'])
def get_all_products():

    productos_query = Producto.query.all()
    results = list(map(lambda item: item.serialize(), productos_query))

    response_body = {
       "results": results
    }

    return jsonify(response_body), 200

# get lista de Productos by ID de Productor
@api.route('/producto_by_productor/<int:id>', methods=['Get'])
def get_all_products_by_Id(id):

    productos_query = Producto.query.filter_by(productor_id=id).all()
    results = list(map(lambda item: item.serialize(), productos_query))
    response_body = {
       "results": results
    }

    return jsonify(response_body), 200


# crear usuario

@api.route('/registro', methods=['POST'])
def add_user():

    request_body = request.get_json(force=True)
    if isinstance(request_body, list):
        for x in request_body:
            item = User(password=x['password'],
                email=x['email'])
            db.session.add(item)
        db.session.commit()
    else:
        item = User(password=request_body['password'],
                email=request_body['email'])
    
        if item is None:
            return jsonify({"msg": "falta información"}), 404
        db.session.add(item)
        db.session.commit()






    response_body = {
        'msg': 'ok',
        "results": ['Usuario Created', item.serialize()]
    }

    return jsonify(response_body), 200



@api.route('/users', methods=['POST'])

def create_user():

    email = request.json.get("email", None)

    request_body = request.get_json(force=True)

    user = User(email=request_body['email'],
                password=request_body['password'])
    
    usuario = User.query.filter_by(email=email).first()
    
    if usuario :
        return jsonify({"msg": "El usuario ya existe"}),402
    
    if request_body['email'] == "" or request_body['password'] == "":
        return jsonify ({
            'msg':'Debes rellenar todos los campos'
        }), 401
    
    else:

        # se comenta porque se hizo funcion general
        # Verificamos email válido (pro)
        # def validar_email(email):
        #     # Patrón de expresión regular para validar el email
        #     patron_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            
        #     # Usamos re.match() para verificar el patrón en el email proporcionado
        #     if re.match(patron_email, email):
        #         return True
        #     else:
        #         return False



        # Ejemplo de uso:

        # email_ejemplo = "usuario@example.com"
        if validar_email(request_body['email']):
            print("El email es válido.")
        else:
            return jsonify ({
                'msg':'Formato de email incorrecto (revise @ .)'
            }), 400

    db.session.add(user)
    db.session.commit()


    response_body = {
       "results": 'User Created'
    }

    return jsonify(response_body), 200


# -------------------- PERFIL PRODUCTOR --------------------

@api.route('/perfil_productor_home', methods=['POST'])
def get_all_productores():
    request_body = request.get_json(force=True)

    Productor_query = PerfilProductor.query

    if request_body['selectedOptions'] and request_body['selectedOptions']['Producto']:
        product_name = request_body['selectedOptions']['Producto']
        Productor_query = Productor_query.filter(PerfilProductor.producto.any(nombre=product_name))

    if request_body['selectedCommunity'] and request_body['selectedCommunity']:
        community_name = request_body['selectedCommunity']
        Productor_query = Productor_query.filter(PerfilProductor.comunidad_autonoma == community_name)
    
    if request_body['selectedProvince'] and request_body['selectedProvince']:
        province_name = request_body['selectedProvince']
        Productor_query = Productor_query.filter(PerfilProductor.provincia == province_name)

    results = list(map(lambda item: item.serialize(), Productor_query))

    response_body = {
        "results": results
    }

    return jsonify(response_body), 200

# -------------------- CREAR PERFIL PRODUCTOR --------------------

@api.route('/perfil_productor', methods=['POST'])
def add_productor():



    request_body = request.get_json(force=True)

    #applying geocode method to get the location
    #making an instance of Nominatim class

    # Requiere al menos, CA, PROV, Municipio y CP
#     print(request_body)
#     geolocator = Nominatim(user_agent="delahuerta_request")
#     loc_list = [request_body['direccion'],request_body['municipio'],request_body['provincia'],request_body['comunidad_autonoma'], request_body['codigo_postal']]
#     loc =  ','.join(loc_list)
#     location = geolocator.geocode(loc)
#     print("ok")


    print(request_body)
    geolocator = Nominatim(user_agent="delahuerta_request")
    #falta verificar dirección
    # try :
    #     loc_list = [request_body['direccion'],request_body['municipio'],request_body['provincia'],request_body['comunidad_autonoma'], request_body['codigo_postal']]
    #     loc =  ','.join(loc_list)
    #     location = geolocator.geocode(loc)
    #     print("ok con dirección completa")
    # except :
    #     loc_list = [request_body['municipio'],request_body['provincia'],request_body['comunidad_autonoma'], request_body['codigo_postal']]
    #     loc =  ','.join(loc_list)
    #     location = geolocator.geocode(loc)
    #     print("ok con municipio")
    


    try :
        loc_list = [request_body['direccion'],request_body['municipio'],request_body['provincia'],request_body['comunidad_autonoma'], request_body['codigo_postal']]
        loc =  ','.join(loc_list)
        location = geolocator.geocode(loc)
        print(f"direccion usada 1: {loc}" )
        

        if location == None:
            location = { 'latitude' :None,'longitude':None}
            print("geolocation address not found, so we use municipio")
            time.sleep(1)
            loc_list = [request_body['municipio'],request_body['provincia'],request_body['comunidad_autonoma'], request_body['codigo_postal']]
            loc =  ','.join(loc_list)
            print(f"direccion usada 2: {loc}" )
            location = geolocator.geocode(loc)
    except:
        print ("error when geocoding, location not found, please use at least comunidad autonoma, provincia and municipio")
        
            
    


    productor = PerfilProductor(
        nombre= request_body['nombre'],
        apellido= request_body['apellido'],
        direccion= request_body['direccion'],
        telefono= request_body['telefono'],
        codigo_postal= request_body['codigo_postal'],
        comunidad_autonoma= request_body['comunidad_autonoma'],
        provincia= request_body['provincia'],
        municipio= request_body['municipio'],
        nombre_huerta= request_body['nombre_huerta'],     
        problemas= request_body['problemas'],
        donde_encontrar= request_body['donde_encontrar'],
        descripcion= request_body['descripcion'],
        user_id=request_body['user_id'],
        latitud = location.latitude,
        longitud =location.longitude
          )
    


    db.session.add(productor)
    db.session.commit()


    response_body = {
        'msg':'ok',
        #"address":loc,
        "results": ['Productor Created', productor.serialize()]
    }

    return jsonify(response_body), 200

# --------------- OBTENER TODOS LOS PRODUCTORES ------


@api.route('/crear_perfil', methods=['GET'])
def get_all_perfiles_productor():

    perfil_query = PerfilProductor.query.all()
    results = list(map(lambda item: item.serialize(), perfil_query))
    print(perfil_query)
    print(results)

    response_body = {
        "message": "ok",
        "results": results

    }

    return jsonify(response_body), 200

# --------------- OBTENER UN PRODUCTOR ---------------------

@api.route('/perfil/<int:user_id>', methods=['GET'])
def get_one_productor(user_id):

    user_query = PerfilProductor.query.filter_by(id=user_id).first()

    response_body = {
        "message": "ok",
        "result": user_query.serialize()

    }

    return jsonify(response_body), 200


# -------------------- LOGIN --------------------

@api.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    user = User.query.filter_by(email=email).first()

    if user is None:
        return jsonify({"msg": "El email no existe"}), 404

    if password != user.password:
        return jsonify({"msg": "Contraseña incorrecta"}), 401
    
  
    
    print(user.serialize())

    results = list(map(lambda item: {"id": item.serialize()["id"],"nombre_huerta": item.serialize()["nombre_huerta"]} , user.favoritos))

    access_token = create_access_token(identity=email)
    
    return jsonify({"access_token":access_token, "user_id":user.id, "productor":user.serialize()["productor"], "info_productor":user.serialize()["info_productor"], "favoritos":results})



@api.route("/get_productor", methods=["GET"])
def getProductor():
    users = User.query.all()
    
    serialized_users = [user.serialize() for user in users]
    print(serialized_users)
    
    if serialized_users:
        # Devuelve el campo "productor" del primer usuario serializado si hay usuarios
        return jsonify({"productor": serialized_users[0]["productor"]})
    else:
        # Manejar el caso en el que no haya usuarios
        return jsonify({"message": "No hay usuarios disponibles"}), 404  # Otra respuesta HTTP apropiada


# -------------------- PROFILE --------------------

@api.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    user = User.query.filter_by(email=current_user).first()
    if user is None:
        return jsonify({"msg": "user do not exist"}), 404
    return jsonify(logged_in_as=current_user), 200

# -------------------- VALIDATE--------------------

@api.route("/validate", methods=["GET"])
@jwt_required()
def check_valid():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    user = User.query.filter_by(email=current_user).first()
    if user is None:
        return False
    return True

# -------------------- ENVIAR EMAIL --------------------

@api.route('/recover_access', methods=['POST'])
def send_mail():

    request_body = request.get_json(force=True)

    email = request_body ['email']

    #check email
    if validar_email(request_body['email']):
        print("El email es válido.")
    else:
        return jsonify ({
            'msg':'Formato de email incorrecto (revise @ .)'
            }), 400

    #check if email exist in database

    user = User.query.filter_by(email=email).first()
    
    if user is None:
        print("email does not exist in database")
        # response_body = {
        # 'msg':'ok',
        # "result": {'Email Received': email},
        #  }
        # return jsonify(response_body), 200
        return jsonify({"msg": "El usuario no existe"}), 404
    else:
        
        user_info_mail =user.serialize()
        clave_secreta = user.password
        print(user_info_mail)
        print(clave_secreta)

        #credenciales
        sender = 'dasi.development00@gmail.com'
        key = "otzxcumnjunhmwxo"

        recibe = email
        asunto = "DeLaHuerta / Recuperar Acceso"

        # crear mensaje
        mensaje = MIMEMultipart()
        mensaje["From"] =  sender
        mensaje["To"] = recibe
        mensaje["Subject"] = asunto

        # Agrega cuerpo de mensaje
        cuerpo = f"Este es un mensaje de recuperacion de clave. Su clave es: {clave_secreta}. En caso de que no haya solicitado porfavor contacte con nosotros"
        mensaje.attach(MIMEText(cuerpo, "plain"))

        # iniciar sesion
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender,key)

        #enviar correo
        texto = mensaje.as_string()
        server.sendmail(sender, recibe, texto)
        server.quit()
        print("correo enviado")
            
        response_body = {
            'msg':'ok',
            "result": {'Email Received': email},
            

        }

        return jsonify(response_body), 200
    
    # -------------------- FAVORITOS --------------------
@api.route('/users/<int:id>', methods=['PUT'])
def edit_user_fav(id):

    body = request.get_json(force=True) #{ 'username': 'new_username'}
    usuario = User.query.filter_by(id=id).first()
    if not usuario:
        return jsonify({"error": "User not found"}), 404
    
    #usuario.favoritos = body["favoritos"]
    print(body["favoritos"])
    print("usuario.favoritos antes de actualizar:",usuario.favoritos)
        # db.session.commit()
    #return jsonify(usuario.serialize()), 200
    #return jsonify(body), 200
    
    # Clear the current favoritos
    usuario.favoritos.clear()

    # Add new favoritos based on the ID
    new_favoritos_ids = body.get("favoritos", [])
    for fav_id in new_favoritos_ids:
        favorito = PerfilProductor.query.filter_by(id=fav_id).first()
        if favorito:
            usuario.favoritos.append(favorito)
        else:
            return jsonify({"error": f"Favorito with ID {fav_id} not found"}), 404

    db.session.commit()

    usuario = User.query.filter_by(id=id).first()

    print("usuario.favoritos despues de actualizar:",usuario.favoritos)

    return jsonify(usuario.serialize()), 200