import React, {useEffect, useState} from "react";
import {Link} from "react-router-dom";

export default function RemoverCliente() {
    const [clienteId, setClienteId] = useState(0)
    const [clientesOptions, setClientesOptions] = useState([])

    useEffect(()=>{
        async function fetchClientes(){
            fetch("http://localhost:8000/cliente").then(response => response.json()).then(data =>
            setClientesOptions(data.map(cliente => <option key={cliente.id} value={cliente.id}>{cliente.nome} | {cliente.cpf}</option>)))
        }
        fetchClientes();
    },[])


    async function handleSubmit(e) {
        e.preventDefault();
        await fetch(`http://localhost:8000/cliente/deletar/${clienteId}`, {
            method: "DELETE"
        })
        window.history.back();
    }

    return (
        <>
            <div className="menuLateralPrincipal">
                <h1><Link to={"/cliente"}> Voltar</Link></h1>
            </div>
            <div className="conteudoAdicionar">
                <form onSubmit={handleSubmit}>
                    <select value={clienteId} onChange={e => {
                        setClienteId(e.target.value);
                    }}>
                        <option value="">Clientes</option>{clientesOptions}
                    </select>
                    <button type={"submit"}>Enviar</button>
                </form>
            </div>
        </>
    );
}