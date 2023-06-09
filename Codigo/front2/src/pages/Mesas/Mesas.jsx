import "./mesas.css"
import React from 'react';
import {useEffect, useState} from "react";
import {Link} from "react-router-dom";

function MesaDiv(props) {
    const mesa = props.mesa
    if (mesa.pago) {
        return (
            <div className="EstaPago mesa" >
                <h1>mesa {mesa.id}</h1>
                <h2>cadeiras: {mesa.numero_integrantes}</h2>
                <h2>consumo total: R$ {mesa.consumo_total}</h2>
            </div>
        )
    }
    return (
        <div className="NaoEstaPago mesa">
            <h1>mesa {mesa.id}</h1>
            <h2>cadeiras: {mesa.numero_integrantes}</h2>
            <h2>consumo total: R$ {mesa.consumo_total}</h2>
        </div>
    )
}


export default function Mesas() {
    const [mesas, setMesas] = useState([])


    useEffect(() => {
        fetch("http://localhost:8000/mesas")
            .then(response => {
                if (response.ok) {
                    return response.json();
                }
                else {
                    throw response
                }
            }).then(data => {
                if (data !== undefined) {
                    setMesas(data)
                }
        })
            .catch(error => {
                console.log("Error ao buscar mesas");
            })

    }, [])
    const listMesas = mesas.map(mesa => <MesaDiv key={mesa.id} mesa={mesa}></MesaDiv>)
    return (
        <>
            <div className="menuLateralPrincipal">
                <h1><Link to={"criar_mesa"}> Adicionar Mesa</Link></h1>
                <h1><Link to={"remover_mesa"}> Remover Mesa</Link></h1>
                <h1><Link to={"editar_mesa"}>Editar Mesa</Link></h1>
                <h1><Link to={"/pedidos/adicionar"}>Adicionar Pedido</Link></h1>
            </div>
            <div className="conteudo">{listMesas}</div>
        </>
    )
}