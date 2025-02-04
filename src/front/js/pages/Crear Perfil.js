import React, { useContext, useState, useEffect } from "react";
import { Context } from "../store/appContext";
import "../../styles/home.css";
import { useNavigate } from "react-router-dom";

export const Perfil = () => {
	const { store, actions } = useContext(Context);
	const navigate = useNavigate();

	const [newProfile, setNewProfile] = useState({
		nombre: "",
		apellido: "",
		direccion: "",
		telefono: "",
		codigo_postal: "",
		comunidad_autonoma: "",
		provincia: "",
		municipio: "",
		nombre_huerta: "",
		problemas: "",
		donde_encontrar: "",
		descripcion: ""
	});
	const [resp, setResp] = useState("");

	const handleChange = event => {
		const { name, value } = event.target;

		// Manejar cambios en los dropdowns de comunidades autónomas y provincias
		if (name === "comunidad_autonoma") {
			setNewProfile({
				...newProfile,
				[name]: value,
				provincia: "" // Resetear la provincia cuando cambia la comunidad
			});
		} else {
			setNewProfile({ ...newProfile, [name]: value });
		}
	};

	async function handleSubmit(e) {
		e.preventDefault();

		let nuevo_productor = await actions.crearPerfil(
			newProfile.nombre,
			newProfile.apellido,
			newProfile.direccion,
			newProfile.telefono,
			newProfile.codigo_postal,
			newProfile.comunidad_autonoma,
			newProfile.provincia,
			newProfile.municipio,
			newProfile.nombre_huerta,
			newProfile.problemas,
			newProfile.donde_encontrar,
			newProfile.descripcion
		);

		if (nuevo_productor) {
			navigate('/perfil'); /* Perfil del productor */
		} else {
			setNewProfile({
				nombre: "",
				apellido: "",
				direccion: "",
				telefono: "",
				codigo_postal: "",
				comunidad_autonoma: "",
				provincia: "",
				municipio: "",
				nombre_huerta: "",
				problemas: "",
				donde_encontrar: "",
				descripcion: ""
			});
			setResp("");
			newProfile.nombre === "" ||
				newProfile.apellido === "" ||
				newProfile.direccion === "" ||
				newProfile.telefono === "" ||
				newProfile.codigo_postal === "" ||
				newProfile.comunidad_autonoma === "" ||
				newProfile.provincia === "" ||
				newProfile.municipio === "" ||
				newProfile.nombre_huerta === "" ||
				newProfile.problemas === "" ||
				newProfile.donde_encontrar === "" ||
				newProfile.descripcion === "" ?
				setResp(
					<div className="alert alert-danger" role="alert">
						Debes rellenar todos los campos
					</div>)
				: setResp(
					<div className="alert alert-danger" role="alert">
						Información incorrecta
					</div>);


		}
	}

	return (
		<div className="Container">
			<div className="row justify-content-center">
				<div className="col-md-6">
					<h1 className="text-center mb-5 mt-5 display-2">Crear Perfil</h1>
					<form onSubmit={handleSubmit}>
						<div className="form-floating mb-3">
							<input
								type="text"
								value={newProfile.nombre}
								onChange={handleChange}
								className="form-control"
								placeholder="Añada aquí su nombre"
								name="nombre"
							/>
							<label htmlFor="floatingInput">Nombre</label>
						</div>
						<div className="form-floating mb-3">

							<input
								type="text"
								value={newProfile.apellido}
								onChange={handleChange}
								className="form-control"
								placeholder="Añada aquí sus apellidos"
								name="apellido"
							/>
							<label htmlFor="floatingInput">Apellidos</label>
						</div>
						<div className="form-floating mb-3">

							<input
								type="tel"
								value={newProfile.telefono}
								onChange={handleChange}
								className="form-control"
								placeholder="Añada aquí el telefono"
								name="telefono"
							/>
							<label htmlFor="floatingInput">Telefono</label>
						</div>


						<div className="form-floating mb-3">

							<select
								onChange={handleChange}
								value={newProfile.comunidad_autonoma}
								className="form-select"
								name="comunidad_autonoma"
								id="id1"
							>

								{/* <option value=""></option> */}
								<option selected>Selecciona una opción</option>
								{Object.keys(store.communityData).map((community, index) => (
									<option key={index} value={community}>
										{community}
									</option>

								))}
							</select>
							<label for="id1">Comunidad Autónoma</label>
						</div>

						<div className="form-floating mb-3">
							
							<select
								onChange={handleChange}
								className="form-select"
								name="provincia"
								id="id2"
							>
								{/* <option value=""></option> */}
								<option selected>Selecciona una opción</option>
								{newProfile.comunidad_autonoma && store.communityData[newProfile.comunidad_autonoma]?.map((province, index) => (
									<option key={index} value={province}>
										{province}
									</option>
								))}
							</select>
							<label for="id2">Provincia</label>
						</div>

						<div className="form-floating mb-3">

							<input
								type="text"
								value={newProfile.municipio}
								onChange={handleChange}
								className="form-control"
								placeholder="Añada aquí su Municipio"
								name="municipio"
							/>
							<label htmlFor="floatingInput">Municipio</label>
						</div>

						<div className="form-floating mb-3">

							<input
								type="text"
								value={newProfile.codigo_postal}
								onChange={handleChange}
								className="form-control"
								placeholder="Añada aquí su codigo postal"
								name="codigo_postal"
							/>
							<label htmlFor="floatingInput">Codigo Postal</label>
						</div>

						<div className="form-floating mb-3">

							<input
								type="text"
								value={newProfile.direccion}
								onChange={handleChange}
								className="form-control"
								placeholder="Añada aquí su dirección"
								name="direccion"
							/>
							<label htmlFor="floatingInput">Dirección</label>
						</div>
						<div className="form-floating mb-3">
							<input
								type="text"
								value={newProfile.nombre_huerta}
								onChange={handleChange}
								className="form-control"
								placeholder="Nombre Huerta"
								name="nombre_huerta"
							/>
							<label htmlFor="floatingInput">Nombre Huerta</label>
						</div>

						<div className="form-floating mb-3">
							<input
								type="text"
								value={newProfile.problemas}
								onChange={handleChange}
								className="form-control"
								placeholder="Tus problemas"
								name="problemas"
							/>
							<label htmlFor="floatingInput">¿Cuáles son tus problemas como agricultor?</label>
						</div>


						<div className="form-floating mb-3">

							<input
								type="text"
								value={newProfile.descripcion}
								onChange={handleChange}
								className="form-control"
								placeholder="descripcion"
								name="descripcion"
							/>
							<label htmlFor="floatingInput">Descripcion</label>
						</div>

						<div className="form-floating mb-3">

							<input
								type="text"
								value={newProfile.donde_encontrar}
								onChange={handleChange}
								className="form-control"
								placeholder="donde_encontrar"
								name="donde_encontrar"
							/>
							<label htmlFor="floatingInput">Donde encontrar</label>
						</div>

						<br />

						<div className="d-flex justify-content-center" >
							{resp}
						</div>

						<div className="d-flex justify-content-center">

							<button type="submit" className="btn btn-submit mt-3 mb-4 form-control col-4 fw-bold text-white fs-5" id="cre">
								Registro
							</button>
						</div>
					</form>
				</div>
			</div>
		</div>
	);
};












{/* <div className="text-center mt-5">
			<h1 className="mb-5 display-2">Crear Perfil</h1>
			<di>
				<form style={{margin: "0 400px 0 400px"}}>
					<div className="input-group mb-3 border border-danger" style={{width: "50%", margin: "20px auto"}}>
						<label htmlFor="floatingInput">Nombre Huerto</label>
						<input type="text" className="form-control" aria-label="Sizing example input" aria-describedby="inputGroup-sizing-default" placeholder="Añade el nombre de tu huerto"/>
					</div>
					<div className="input-group mb-3" style={{width: "50%", margin: "20px auto"}}>
						<label htmlFor="floatingInput">¿Quién eres?</label>
						<input type="text" className="form-control" aria-label="Sizing example input" aria-describedby="inputGroup-sizing-default" placeholder="¿Cuéntanos sobre ti?"/>
					</div>
					<div className="input-group mb-3" style={{width: "50%", margin: "20px auto"}}>
						<label htmlFor="floatingInput">¿Cómo te podemos ayudar?</label>
						<input type="text" className="form-control" aria-label="Sizing example input" aria-describedby="inputGroup-sizing-default" placeholder="¿Cuáles son tus problemas como agriculltor?"/>
					</div>
					<div className="input-group mb-3" style={{width: "50%", margin: "20px auto"}}>
						<label htmlFor="floatingInput">Ubicación</label>
						<input type="text" className="form-control" aria-label="Sizing example input" aria-describedby="inputGroup-sizing-default" placeholder="¿Dónde y cuándo podemos encontrarte?"/>
					</div>
					<div>
						<button className="btn btn-success" type="submit">
							Registro
						</button>
					</div>
				</form>
			</di>
		</div> */}