from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, Table, delete, select,Float

db = SQLAlchemy()

# add Favorito with many to many relationship

# step 1. table with tables ids
user_productor = db.Table('user_productor',
                    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                    db.Column('productor_id', db.Integer, db.ForeignKey('perfil_productores.id'))
                    )

#step 2.
#favoritos = db.relationship('PerfilProductor', secondary=user_productor, backref='users') # in User

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    #username = db.Column(db.String(20), unique=False, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    #one2one relationship with perfil_productor
    productor = db.relationship("PerfilProductor", uselist=False,back_populates="user")
    #many2many relationship with favoritos
    favoritos = db.relationship('PerfilProductor', secondary=user_productor, backref='users')
    pedido = db.relationship('Pedido', backref='users', lazy=True)

    def __repr__(self):
        return f"<User {self.email}>"

    def serialize(self):
        user_productor = PerfilProductor.query.filter_by(user_id=self.id).first()
        is_productor = False if user_productor is None else True
        info_productor = None if user_productor is None else user_productor.serialize()
        # serialized_favoritos = [favorito.serialize() for favorito in self.favoritos]
        serialized_favoritos = [favorito.id for favorito in self.favoritos]
        print(user_productor)
        return {
            "id": self.id,
            #"nombre": self.username,
            "email": self.email,
            "info_productor": info_productor,
            "productor": is_productor,
            "favoritos": serialized_favoritos
            # do not serialize the password, its a security breach
        }



    
class PerfilProductor(db.Model):
    __tablename__ = 'perfil_productores'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    producto = db.relationship('Producto', backref='perfil_productores', lazy=True)
    #user = db.relationship('User', backref='comunidades_autonomas', lazy=True)

    #one2one relationship with user
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", back_populates="productor")
    nombre_huerta = db.Column(db.String(250), nullable=True)
    nombre = db.Column(db.String(20), unique=False, nullable=False)
    apellido = db.Column(db.String(50), unique=False, nullable=False)
    direccion = db.Column(db.String(120), unique=False, nullable=False)
    telefono = db.Column(db.Integer, unique=True, nullable=False)
    codigo_postal = db.Column(db.Integer, unique=False, nullable=False)
    comunidad_autonoma = db.Column(db.String(80), unique=False, nullable=True)
    provincia = db.Column(db.String(80), unique=False, nullable=True)
    municipio = db.Column(db.String(80), unique=False, nullable=True)
    foto_portada = db.Column(db.String(250), nullable=True)
    foto_perfil = db.Column(db.String(250), nullable=True)
    problemas = db.Column(db.String(250), nullable=True)
    descripcion = db.Column(db.String(400), nullable=True)
    donde_encontrar = db.Column(db.String(250), nullable=True)
    latitud = db.Column(db.Float, nullable=True)
    longitud = db.Column(db.Float, nullable=True)
    # relationship with favorito
    #favoritos = db.relationship('favoritos_productores', backref='perfil_productores', lazy=True)

    def __repr__(self):
        return '<PerfilProductor %r>' % self.nombre_huerta

    def serialize(self):
        return {
            "id": self.id,
            "nombre" : self.nombre,
            "apellido" : self.apellido,
            "direccion" : self.direccion,
            "telefono" : self.telefono,
            "codigo_postal" : self.codigo_postal,
            "comunidad_autonoma" : self.comunidad_autonoma,
            "provincia ": self.provincia,
            "municipio ": self.municipio,
            "nombre_huerta": self.nombre_huerta,
            "problemas": self.problemas,
            "descripcion": self.descripcion,
            "donde_encontrar": self.donde_encontrar,
            "latitud": self.latitud,
            "longitud": self.longitud,
            "user_id": self.user_id 
            
            # do not serialize the password, its a security breach
        }

class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    productor_id = db.Column(db.Integer, db.ForeignKey('perfil_productores.id'),nullable=False)
    #comunidad_autonoma_id = db.Column(db.Integer, db.ForeignKey('comunidades_autonomas.id'),nullable=False)
    nombre = db.Column(db.String(250), nullable=True)
    variedad = db.Column(db.String(250), nullable=True)
    cantidad = db.Column(db.Integer, nullable=True)
    unidad_medida = db.Column(db.String(250), nullable=True)
    precio = db.Column(db.Float, nullable=True)
    tipo_produccion = db.Column(db.String(250), nullable=True)
    recogida = db.Column(db.String(250), nullable=True)
    pedido = db.relationship('Pedido', backref='productos', lazy=True)
  

    def __repr__(self):
        return '<Producto %r>' % self.nombre

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "tipo_produccion": self.tipo_produccion,
            "variedad": self.variedad,
            "cantidad": self.cantidad,
            "unidad_medida": self.unidad_medida,
            "precio": self.precio,
            "recogida": self.recogida,
            "productor_id": self.productor_id

        }


class ProductoNombre(db.Model):
    __tablename__ = 'productoNombres'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    nombre = db.Column(db.String(250), nullable=True)
    
    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "tipo_produccion": self.tipo_produccion
        }
  

    def __repr__(self):
        return '<ProductoNombre %r>' % self.nombre


#Pedido 
class Pedido(db.Model):
    __tablename__ = 'pedidos'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)
    # fecha_recogida = db.Column(db.Date, nullable=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'),nullable=False)
    cantidad_solicitada = db.Column(db.Integer, nullable=False)
    #productos = db.relationship('Producto', secondary=Pedido_producto, backref='Pedidos') de many to many
    

    
    
    def serialize(self):
        return {
            "id": self.id,
            "fecha_recogida": self.fecha_recogida
            
        }
  

    def __repr__(self):
        return '<ProductoNombre %r>' % self.nombre  