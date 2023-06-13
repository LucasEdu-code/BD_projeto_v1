import React, {useEffect, useState} from "react";
import {Link} from "react-router-dom";


function ClienteDiv(props) {
    const cliente = props.cliente
    if (cliente === undefined) return <></>

    return (
        <div>
            <h3>#{cliente.id} | {cliente.nome} - CPF: {cliente.cpf} </h3>
        </div>
    )
}


export default function Clientes() {
    const [clientes, setClientes] = useState([])

    useEffect( () => {
        async function fetchClientes() {
            fetch("http://localhost:8000/cliente").then(response => response.json()).then(data => setClientes(data))
        }

        fetchClientes();
    }, [])

    const listaDeClientes = clientes.map(cliente => <ClienteDiv key={cliente.id} cliente={cliente}></ClienteDiv>)

    return (
        <>
            <div className="menuLateralPrincipal">
                <h1><Link to={"adicionar"}>Adicionar Cliente</Link></h1>
                <h1><Link to={"remover"}>Remover Cliente</Link></h1>
                <h1><Link to={"editar"}>Alterar Cliente</Link></h1>
                <h1><Link to={"pagar"}>Efetuar Pagamento</Link></h1>
                <h1><Link to={"buscar-pagamento"}>Buscar Pagamentos do cliente</Link></h1>
                <h1><Link to={"/"}>Voltar</Link></h1>
            </div>
            <div className="conteudoPratos">
                {listaDeClientes}
            </div>
        </>
    );
}