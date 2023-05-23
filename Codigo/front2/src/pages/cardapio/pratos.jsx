import React, {useEffect, useState} from "react";
import {Link} from "react-router-dom";

function PratoDiv(props) {
    const prato = props.prato

    return (
        <div>
            <h3>#{prato.id_prato} {prato.prato_nome} R$ {prato.preco}</h3>
        </div>
    )
}

export default function Pratos() {
    const [pratos, setPratos] = useState([])

    useEffect(() => {
        fetch("http://localhost:8000/pratos")
            .then(response => {
                if (response.ok) {
                    return response.json();
                }
                else {
                    throw response
                }
            }).then(data => setPratos(data))
            .catch(error => {
                console.log("Error ao buscar mesas");
            })

    }, [pratos])

    const listaPratos = pratos.map(prato => <PratoDiv key={prato.id_prato} prato={prato}></PratoDiv>)

    return (
        <>
            <div className="menuLateralPrincipal">
                <h1><Link to={"criar_mesa"}> Adicionar Prato</Link></h1>
                <h1><Link to={"remover_mesa"}> Remover Prato</Link></h1>
                <h1><Link to={"remover_mesa"}> Alterar Prato</Link></h1>
            </div>
            <div className="conteudo">{listaPratos}</div>
        </>
    )
}