import React, {useEffect, useState} from "react";
import {Link} from "react-router-dom";
import {PratoInfoDiv} from "../cardapio/editarPrato";


function ClienteInfoDiv(props) {
    let cliente = props.cliente
    if (cliente === undefined) return <></>
    return (
        <div className={"infoPrato"}>
            <h3> #{cliente.id} | Nome: {cliente.nome}</h3>
            <h3>CPF: {cliente.cpf}</h3>
        </div>
    )
}

export default function EditarCliente() {
    const [clienteId, setClienteId] = useState(0)
    const [clienteInfo, setClienteInfo] = useState({})
    const [nome, setNome] = useState("")
    const [cpf, setCPF] = useState("")
    const [clientesOptions, setClientesOptions] = useState([])
    async function handleSubmit(e) {
        e.preventDefault();

        fetch(`http://localhost:8000/cliente/modificar/${clienteId}`,
            {
                method: "PUT",
                headers: {"Content-Type":"application/json"},
                body: JSON.stringify(
                    {
                        "nome": nome === "" ? undefined : nome,
                        "cpf": cpf === "" ? undefined : cpf,
                    }
                )
            })
        window.history.back()
    }

    useEffect(()=>{
        async function fetchClientes() {
            fetch("http://localhost:8000/cliente")
                .then(response => response.json())
                .then(data => setClientesOptions(data.map(cliente => <option key={cliente.id} value={cliente.id}>{cliente.nome} | CPF: {cliente.cpf}</option>)))
            if (clienteId !== 0) {
                fetch(`http://localhost:8000/cliente/buscar/id/${clienteId}`)
                    .then(response => response.json())
                    .then(data => setClienteInfo(data))
            }
        }

        fetchClientes()
    },[clienteId])

    return (
        <>
            <div className="menuLateralPrincipal">
                <h1><Link to={"/clientes"}>Voltar</Link></h1>
            </div>
            <form onSubmit={handleSubmit} className={"formPrato"}>
                <select value={clienteId} onChange={e => {
                    const value = parseInt(e.target.value)
                    if (!isNaN(value))
                        setClienteId(value);
                    else setClienteId(0)
                }}>
                    <option value="">Clientes</option>{clientesOptions}
                </select>
                <ClienteInfoDiv prato={clienteInfo}/>
                <label>Nome</label>
                <input type="text" value={nome} onChange={e => {
                    setNome(e.target.value)
                }}/>
                <label>CPF</label>
                <input type="number" value={cpf} onChange={e => {
                    setCPF(e.target.value)
                }}/>

                <button type={"submit"}>Enviar</button>
            </form>
        </>
    )
}