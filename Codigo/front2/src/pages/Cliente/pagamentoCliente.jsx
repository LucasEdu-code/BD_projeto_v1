import React, {useEffect, useState} from "react";
import {Link} from "react-router-dom";
import {PratoInfoDiv} from "../cardapio/editarPrato";

export default function PagamentoCliente() {
    const [mesaOptions, setMesaOptions] = useState([])
    const [clientesOptions, setClientesOption] = useState([])
    const [metodosOption, setMetodosOption] = useState([])

    const [clienteId, setClienteId] = useState(0)
    const [mesaId, setMesaId] = useState(0)
    const [metodoId, setMetodoId] = useState(0)

    useEffect(()=>{
        async function fetchMesa() {
            fetch("http://localhost:8000/mesas")
                .then(response => response.json())
                .then(data => setMesaOptions(data.map(mesa => <option key={mesa.id} value={mesa.id}>{mesa.id} | R$ {mesa.consumo_total}</option>)))
        }

        async function fetchClientes() {
            fetch("http://localhost:8000/cliente")
                .then(response => response.json())
                .then(data => setClientesOption(data.map(cliente => <option key={cliente.id} value={cliente.id}>{cliente.nome} | CPF: {cliente.cpf}</option>)))
        }

        async function fetchMetodos() {
            fetch("http://localhost:8000/metodoPagamento")
                .then(response => response.json())
                .then(data => setMetodosOption(data.map(metodo => <option key={metodo.id} value={metodo.id}>{metodo.nome}</option>)))
        }

        fetchMesa();
        fetchClientes();
        fetchMetodos();
    },[])


    async function handleSubmit(e) {
        e.preventDefault();
        if (mesaId !== 0) {
            await fetch(`http://localhost:8000/pagamento/pagar/${mesaId}`,
                {
                    method: "POST",
                    headers: {"Content-Type":"application/json"},
                    body: JSON.stringify(
                        {
                            "metodo_id": metodoId === 0 ? undefined : metodoId,
                            "cliente_id": clienteId === 0 ? undefined : clienteId,
                        }
                    )
                })
        }
    }

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

                <select value={mesaId} onChange={e => {
                    const value = parseInt(e.target.value)
                    if (!isNaN(value))
                        setMesaId(value);
                    else setMesaId(0)
                }}>
                    <option value="">Mesas</option>{mesaOptions}
                </select>

                <select value={metodoId} onChange={e => {
                    const value = parseInt(e.target.value)
                    if (!isNaN(value))
                        setMetodoId(value);
                    else setMetodoId(0)
                }}>
                    <option value="">Metodos de Pagamento</option>{metodosOption}
                </select>

                <button type={"submit"}>Enviar</button>
            </form>
        </>
    )
}