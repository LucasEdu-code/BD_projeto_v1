import React, {useEffect, useState} from "react";
import {Link} from "react-router-dom";

function PedidoDiv(props) {
    const pedido = props.pedido
    if (pedido === undefined) return <></>
    const estado = pedido.entregue ? "entregue" : "não foi entregue"
    const date = new Date(pedido.data)


    return (
        <div>
            <h3>#{pedido.id_pedido} {pedido.prato_nome} R$ {pedido.prato_preco} | quantidade: {pedido.quantidade} | {estado} |
                {date.toLocaleDateString()} - {date.toLocaleTimeString()}</h3>
            <h4>Para mesa: {pedido.id_mesa}</h4>
        </div>
    )
}

export default function Pedidos() {
    const [pedidos, setPedidos] = useState([])

    useEffect(() => {
        fetch("http://localhost:8000/pedidos")
            .then(response => {
                if (response.ok) {
                    return response.json();
                }
                else {
                    throw response
                }
            }).then(data => setPedidos(data))
            .catch(error => {
                console.log("Error ao buscar pedidos");
            })

    }, [pedidos])

    const listaPedidos = pedidos.map(pedido => <PedidoDiv key={pedido.id_pedido} pedido={pedido}></PedidoDiv>)

    return (
        <>
            <div className="menuLateralPrincipal">
                <h1><Link to={"adicionar"}> Adicionar Pedido</Link></h1>
                <h1><Link to={"remover"}> Remover Pedido</Link></h1>
                <h1><Link to={"editar"}> Alterar Pedido</Link></h1>
            </div>
            <div className="conteudoPratos">{listaPedidos}</div>
        </>
    )
}