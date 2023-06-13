import React, {useEffect, useState} from "react";
import {Link} from "react-router-dom";

function PagamentoDiv(props) {
    const pagamento = props.pagamento
    if (pagamento === undefined) return <></>


    return (
        <div>
            <h3>#{pagamento.id} {pagamento.metodo_pagamento} R$ {pagamento.valor} | mesa: {pagamento.mesa} |
                {pagamento.cliente_nome} - {pagamento.cliente_cpf}</h3>
        </div>
    )
}


export default function BuscarPagamentos() {
    const [clienteId, setClienteId] = useState(0)
    const [clientesOptions, setClientesOption] = useState([])

    const [pagamentos, setPagamentos] = useState([])


    useEffect(() => {
        async function fetchClientes() {
            fetch("http://localhost:8000/cliente")
                .then(response => response.json())
                .then(data => setClientesOption(data.map(cliente => <option key={cliente.id} value={cliente.id}>{cliente.nome} | CPF: {cliente.cpf}</option>)))
        }

        async function fetchPagamentos(cliente_id) {
            fetch(`http://localhost:8000/pagamento/${cliente_id}`)
                .then(response => response.json())
                .then(data => setPagamentos(data))
        }
        fetchClientes();

        if (clienteId !== 0) {
            fetchPagamentos(clienteId)
        }
        else {
            setPagamentos([])
        }
    }, [clienteId])

    const listarPagamentos = pagamentos.map(pagamento => <PagamentoDiv key={pagamento.id} pagamento={pagamento}></PagamentoDiv>)

    return (
        <>
            <div className="menuLateralPrincipal">
                <h1><Link to={"/clientes"}>Voltar</Link></h1>
            </div>

            <div className="conteudoPratos">
                <div>
                    <select value={clienteId} onChange={e => {
                        const value = parseInt(e.target.value)
                        if (!isNaN(value))
                            setClienteId(value);
                        else setClienteId(0)
                    }}>
                        <option value="">Pratos</option>{clientesOptions}
                    </select>
                </div>
                {listarPagamentos}
            </div>
        </>
    )
}