import React, {useEffect, useState} from "react";
import {Link} from "react-router-dom";
import "./pedidos.css"

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
    const [qnt_pedidos, setQntPedidos] = useState(0)
    const [custo_total, setCustoTotal] = useState(0)

    useEffect(() => {
        fetch("http://localhost:8000/pedidos/listar")
            .then(response => {
                if (response.ok) {
                    return response.json();
                }
                else {
                    throw response
                }
            }).then(data => {
                setPedidos(data)
                setQntPedidos(data.length)
                let temp = 0
                data.forEach(pedido => {
                    temp += pedido.prato_preco * pedido.quantidade
                })
                setCustoTotal(temp)
        })
            .catch(error => {
                console.log("Error ao buscar pedidos");
            })
    }, [])

    const listaPedidos = pedidos.map(pedido => <PedidoDiv key={pedido.id_pedido} pedido={pedido}></PedidoDiv>)


    return (
        <>
            <div className="menuLateralPrincipal">
                <h1><Link to={"adicionar"}> Adicionar Pedido</Link></h1>
                <h1><Link to={"remover"}> Remover Pedido</Link></h1>
                <h1><Link to={"editar"}> Alterar Pedido</Link></h1>
            </div>
            <div className="conteudoPratos">
                <div className={"resumoPedidos"}>
                    <h3>Quantidade de pedidos: {qnt_pedidos}</h3>
                    <h3>Custo total: {custo_total}</h3>
                </div>
                {listaPedidos}
            </div>
        </>
    )
}