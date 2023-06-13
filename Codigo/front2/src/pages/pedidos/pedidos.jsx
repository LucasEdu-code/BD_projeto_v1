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
    const [pratos, setPratos] = useState([])
    const [tipos, setTipos] = useState([])
    const [categorias, setCategorias] = useState([])
    const [qnt_pedidos, setQntPedidos] = useState(0)
    const [custo_total, setCustoTotal] = useState(0)


    useEffect(() => {
        async function fetchPedidos() {
            await fetch("http://localhost:8000/pedidos/listar").then(response => {
                if (response.ok) return response.json();
                else throw response;
            }).then(data => {
                setPedidos(data)
                setQntPedidos(data.length)
                let temp = 0
                data.forEach(pedido => {
                    temp += pedido.prato_preco * pedido.quantidade
                })
                setCustoTotal(temp)
            })
                .catch(error => console.log("Error ao buscar pedidos"))
        }

        async function fetchPratos() {
            await fetch("http://localhost:8000/pratos")
                .then(response => response.json())
                .then(data => setPratos(data))
        }

        async function fetchTipos() {
            await fetch("http://localhost:8000/tipos")
                .then(response => response.json())
                .then(data => setTipos(data))
        }

        async function fetchCategorias() {
            await fetch("http://localhost:8000/categorias")
                .then(response => response.json())
                .then(data => setCategorias(data))
        }

        fetchPedidos();
        fetchPratos();
        fetchTipos();
        fetchCategorias();
    }, [])


    const listaPedidos = pedidos.map(pedido => <PedidoDiv key={pedido.id_pedido} pedido={pedido}></PedidoDiv>)


    return (
        <>
            <div className="menuLateralPrincipal">
                <h1><Link to={"adicionar"}>Adicionar</Link></h1>
                <h1><Link to={"remover"}>Remover</Link></h1>
                <h1><Link to={"editar"}>Alterar</Link></h1>
                <h1><Link to={"filtrarPorTempo"}>Filtrar por tempo</Link></h1>
                <h1><Link to={"filtrarPorPrato"}>Filtrar por Prato</Link></h1>
                <h1><Link to={"filtrarPorCategoria"}>Filtrar por Categoria</Link></h1>
                <h1><Link to={"filtrarPorTipo"}>Filtrar por Tipo</Link></h1>
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