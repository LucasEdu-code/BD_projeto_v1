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

export default function FiltrarPorTipo() {
    const [nomeTipo, setNomeTipo] = useState("")

    const [pedidos, setPedidos] = useState([])
    const [tipos, setTipos] = useState([])

    const [qnt_pedidos, setQntPedidos] = useState(0)
    const [custo_total, setCustoTotal] = useState(0)

    useEffect(() => {
        async function fetchPedidos() {
            if (nomeTipo !== "") {
                await fetch(`http://localhost:8000/pedidos/buscar/tipo/${nomeTipo}`).then(response => {
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
        }


        async function fetchTipos() {
            fetch("http://localhost:8000/tipos").then(response => response.json()).then(data => setTipos(data.map(prato => <option key={prato.id} value={prato.id}>{prato.id} | {prato.nome}</option> )))
        }
        fetchPedidos();
        fetchTipos();
        console.log(nomeTipo)
    }, [nomeTipo])

    const listaPedidos = pedidos.map(pedido => <PedidoDiv key={pedido.id_pedido} pedido={pedido}></PedidoDiv>)

    return (
        <>
            <div className="menuLateralPrincipal">
                <h1><Link to={"/pedidos"}>Voltar</Link></h1>
            </div>
            <div>
                <select value={nomeTipo} onChange={e => {
                    setNomeTipo(e.target.value);
                }}>
                    <option value="0">Tipos</option>{tipos}
                </select>

                <div className="conteudoPratos">

                    <div className={"resumoPedidos"}>
                        <h3>Quantidade de pedidos: {qnt_pedidos}</h3>
                        <h3>Custo total: {custo_total}</h3>
                    </div>
                    {listaPedidos}
                </div>
            </div>

        </>
    )
}