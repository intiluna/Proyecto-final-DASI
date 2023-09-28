import React, { useContext, useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios"

import { Context } from "../store/appContext.js";

export const Navbar = () => {

	const { actions, store } = useContext(Context);
	const navigate = useNavigate()

	const handlerPerfil = (e) => {
		e.preventDefault()
		console.log(store.is_productor);
		store.log === false && store.is_productor === false ? navigate('/login') :
			store.log === true && store.is_productor === false ? navigate('/crear_perfil') :
				navigate("/perfil") /* --> Enlace a perfil productor*/
	}

	const handlerHome = (e) => {
		e.preventDefault()
		navigate("/") /* --> Enlace a la home*/
	}

	const handlerEquipo = (e) => {
		e.preventDefault()
		navigate("/equipo") /* --> Enlace a la home*/
	}

	const handlerLogIn = (e) => {
		e.preventDefault()
		navigate("/login")
	}

	const handlerLogOut = (e) => {
		e.preventDefault()
		let logout = actions.logout()
		localStorage.removeItem("favo");
		if (!logout) {
			navigate("/login")
		}
		

	}

	function handlePerfilPublico(id) {
		//alert('hello');
		actions.getInfoPublicaProductor(id)
		actions.getProductosPorProductor(id)
		navigate(`/perfil/${id}`)
		console.log("funciona")
	}

console.log(store.favoritos);
        

	useEffect(() => {

		actions.getProfile();
		if (localStorage.getItem("favo") != null) {
        const storedJsonString = localStorage.getItem("favo");
        const storedObject = JSON.parse(storedJsonString);
        actions.addFavorito(storedObject)}

        // console.log(localStorage);
	}, []);


	return (
		<nav className="navbar navbar-expand-lg navbar-light bg-light sticky-top" id="nav" >
			<div className="container-fluid px-4">

				<div className="collapse navbar-collapse col-4" id="navbarSupportedContent">

					<a className="navbar-brand" href="#" onClick={handlerHome}>
						<img src="https://media.istockphoto.com/id/1023035296/es/vector/ensalada-icono-vector-de-se%C3%B1al-y-s%C3%ADmbolo-aisladas-sobre-fondo-blanco-el-concepto-de-logotipo.jpg?s=612x612&w=0&k=20&c=HMLUg1UhDlldPBK_ZNc9XBm9a5nJtbJrDk3JCj9qD30=" alt="" width="50" height="50" />
					</a>

					<button id="btn-ir" className="btn btn-success p-0 " >

						<li className="nav-item float-start ">
							<a className="nav-link active link-light" aria-current="page" href="#" onClick={handlerPerfil}>Ir a mi huerto</a>
						</li>

					</button>
					<h1 id="titulo" className="fs.3 fw-semibold" >De la huerta</h1>

				</div >


				<div className="d-flex col-6justify-content-end ">

					<button id="btn-home" className="btn btn-success p-0 btn-block mx-2" >

						<li className="nav-item" onClick={handlerHome}>
							<a className="nav-link active link-light" aria-current="page" href="#" onClick={handlerHome}>Home</a>
						</li>

					</button>
					<button id="btn-eq" className="btn btn-success p-0 btn-block mx-2" >

						<li className="nav-item" onClick={handlerEquipo}>
							<a className="nav-link active link-light" aria-current="page" href="#" onClick={handlerEquipo}>Equipo</a>
						</li>

					</button>


					{(store.log === false) ?

						<button id="btn-login" className="btn btn-success p-0 mx-2" >

							<li className="nav-item" onClick={handlerLogIn}>
								<a className="nav-link active link-light" aria-current="page" href="#">Log in</a>
							</li>
						</button>

						: <button id="btn-login" className="btn btn-success p-0 mx-2">
							<li className="nav-item" onClick={handlerLogOut}>
								<a className="nav-link active link-light" aria-current="page" href="#">Log out</a>
							</li>
						</button>

					}

					{/* FAVORITOS */}

					{(store.log === true) ?

						<button id="btn-fav" className="btn btn-success p-0 mx-2" >


							<li className="nav-item dropdown">
								<a className="nav-link dropdown-toggle link-light" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
									Favoritos


									{/* CONTADOR */}

									<span className="badge bg-secondary mx-2">{store.favoritos.length}</span>
								</a>

								<ul className="dropdown-menu dropdown-menu-end" aria-labelledby="navbarDropdown">

									{/* CONDICIONAL LISTADO FAVORITOS */}


									{store.favoritos.length === 0 ?

										<li className="mx-2" >
											Vacío
										</li>

										: store.favoritos.map((el, i) => (

											<li id={i} key={i} className="mx-2" onClick={e => handlePerfilPublico(el.id)}>


												{el.nombre_huerta}


												{/* BOTON ELIMINAR */}

												< button type="button" onClick={(e) => actions.removeFav(e, el)} className="btn float-end px-1 py-0" aria-label="Close">
													<i className="fas fa-trash"></i>
												</button>

											</li>
										))
									}
								</ul>
							</li>

						</button>

						: null}


					{/* CARRITO */}

					{/* {(store.log === true) ?
						<button id="btn-car" className="btn btn-success p-0 " >


							<li className="nav-item dropdown">
								<a className="nav-link dropdown-toggle link-light" href="#" id="carrito" role="button" data-bs-toggle="dropdown" aria-expanded="false">
									<i className="fa-solid fa-cart-arrow-down"></i>
								</a>
								<ul className="dropdown-menu dropdown-menu-end" aria-labelledby="navbarDropdown">
									<li><a className="dropdown-item" href="#">Action</a></li>
									<li><a className="dropdown-item" href="#">Another action</a></li>
									<li><hr className="dropdown-divider" /></li>
									<li><a className="dropdown-item" href="#">Something else here</a></li>
								</ul>
							</li>
						</button>

						: null} */}
				</div>

			</div >
		</nav >

	);
};
