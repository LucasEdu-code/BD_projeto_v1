import {Link} from "react-router-dom";
import React, {useEffect, useState} from "react";

function TipoDiv(props) {
    const tipo = props.tipo

    return (
        <div className={"pratos"}>
            <h3>#{tipo.id} {tipo.nome}</h3>
        </div>
    )
}


export default function Tipos() {
    const [tipos, setTipos] = useState([])

    useEffect(() => {
        fetch("http://localhost:8000/tipos")
            .then(response => {
                if (response.ok) {
                    return response.json();
                }
                else {
                    throw response
                }
            }).then(data => setTipos(data))
            .catch(error => {
                console.log("Error ao buscar tipos");
            })

    }, [])

    const listarTipos = tipos.map(tipo => <TipoDiv key={tipo.id_prato} tipo={tipo}></TipoDiv>)

    return (
        <>
            <div className="menuLateralPrincipal">
                <h1><Link to={"adicionar"}>Adicionar</Link></h1>
                <h1><Link to={"remover"}>Remover</Link></h1>
                <h1><Link to={"editar"}>Alterar</Link></h1>
                <h1><Link to={"/pratos"}>Voltar</Link></h1>
            </div>
            <div className="conteudoPratos">{listarTipos}</div>
        </>
    )
}