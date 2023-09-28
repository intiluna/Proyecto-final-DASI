import React, { useContext, useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import PropTypes from "prop-types";
import { Context } from "../store/appContext";

export const Card_P = (props,{ hasSearched }) => {
    const { store, actions } = useContext(Context);
    const [isFavorite, setIsFavorite] = useState(false);
    const perfiles = store.perfil;

    const navigate = useNavigate();

    // FUNCION ICONO DE ME GUSTA

    const handleClick = (e, id, nombre_huerta) => {
        e.preventDefault()
        // console.log(store.favoritos);
        let favs = [...store.favoritos]
        setIsFavorite(!isFavorite)

        if (!isFavorite === true) {
            favs.push({
                nombre_huerta: nombre_huerta,
                id: id,
                
            })

        } else (
            favs = favs.filter((item) => item.nombre_huerta !== nombre_huerta)
            // favs = favs.filter((item) => item.id !== id)
        )
     
        actions.addFavorito(favs)
        console.log(store.favoritos);
        const jsonString = JSON.stringify(favs);
        localStorage.setItem("favo", jsonString);
        console.log(localStorage);
        console.log(store.favoritos);
    }



    function handlePerfilPublico(id) {
        actions.getInfoPublicaProductor(id);
        actions.getProductosPorProductor(id);
        navigate(`/perfil/${id}`);
    }
    useEffect(() => {
        const esFavorito = store.favoritos.some((favorite) => favorite.nombre_huerta === props.nombre_huerta);
        setIsFavorite(esFavorito);
       
     
    }, [store.favoritos]);

    return (
   
                <div className="card rounded card-home mb-2">
                    <div className="card-body">
                        <h4 className="card-title text-center">{props.nombre_huerta}</h4>
                        <p className="card-text"><b>Nombre:</b> {props.nombre}</p>
                        <p className="card-text"><b>Municipio:</b> {props.municipio}</p>
                        <p className="card-text"><b>Teléfono:</b> {props.telefono}</p>
                        <p className="card-text"><b>Dónde encontrar:</b> {props.donde_encontrar}</p>

                        <button type="button" className="btn btn-success" onClick={e => handlePerfilPublico(props.id)}>Ir a perfil</button>

                        {(store.log === true) ?
                            <button type="button" className="btn btn-outline-success float-end" onClick={e => handleClick(e, props.id, props.nombre_huerta)}>

                                {

                                    (isFavorite) ? <i className="fas fa-heart"></i> : <i className="far fa-heart"></i>

                                    
                                }

                            </button>
                            
                            : null}
                    </div>
                    
                </div>
    );


};
Card_P.propTypes = {

	nombre: PropTypes.string,
	id: PropTypes.number,
    nombre_huerta: PropTypes.string,
    municipio: PropTypes.string,
    telefono: PropTypes.number,
    donde_encontrar: PropTypes.string

};