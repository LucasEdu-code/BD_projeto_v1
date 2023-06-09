import {Link} from "react-router-dom";
import React, {useEffect, useState} from "react";

function TipoDiv(props) {
    const categoria = props.categoria

    return (
        <div className={"pratos"}>
            <h3>#{categoria.id} {categoria.nome}</h3>
        </div>
    )
}


export default function Tipos() {
    const [categorias, setCategorias] = useState([])

    useEffect(() => {
        fetch("http://localhost:8000/categorias")
            .then(response => {
                if (response.ok) {
                    return response.json();
                }
                else {
                    throw response
                }
            }).then(data => setCategorias(data))
            .catch(error => {
                console.log("Error ao buscar tipos");
            })

    }, [])

    const listaCategorias = categorias.map(categoria => <TipoDiv key={categoria.id_prato} categoria={categoria}></TipoDiv>)

    return (
        <>
            <div className="menuLateralPrincipal">
                <h1><Link to={"adicionar"}>Adicionar</Link></h1>
                <h1><Link to={"remover"}>Remover</Link></h1>
                <h1><Link to={"editar"}>Alterar</Link></h1>
                <h1><Link to={"/pratos"}>Voltar</Link></h1>
            </div>
            <div className="conteudoPratos">{listaCategorias}</div>
        </>
    )
}