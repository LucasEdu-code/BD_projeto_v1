import React, {useEffect, useState} from "react";
import {Link} from "react-router-dom";

export default function EditarPedido() {
    const [pedidoId, setPedidoId] = useState(0);
    const [pedidosOptions, setPedidosOptions] = useState([]);
    const [pratoOptions, setPratoOptions] = useState([])



    const [prato, setPrato] = useState(0)
    const [quantidade, setQuantidade] = useState(0)
    const [estado, setEstado] = useState("")

    async function handleSubmit(e) {
        e.preventDefault();
        try {
            fetch(`http://localhost:8000/pedidos/modificar/${pedidoId}`,
                {
                    method: "PUT",
                    headers: {"Content-Type":"application/json"},
                    body: JSON.stringify(
                        {
                            "id_prato": prato === 0 ? undefined : prato,
                            "quantidade": quantidade === 0 ? undefined : quantidade,
                            "entregue": estado === "Entregue"
                        }
                    )
                })
        }
        catch (e) {
            console.log(e)
        }
        window.history.back();
    }
    
    useEffect(
        () => {
            async function fetchPedidos() {
                fetch("http://localhost:8000/pedidos").then(response => response.json()).then(data => {
                    if (data !== undefined) {
                        setPedidosOptions(data.map(
                            pedido => <option value={pedido.id_pedido} key={pedido.id_pedido}>id: {pedido.id_pedido} | prato: {pedido.prato_nome}</option>));
                    }
                })
            }


            async function fetchPratos() {
                fetch("http://localhost:8000/pratos").then(response => response.json()).then(data => {
                    if (data !== undefined) {
                        setPratoOptions(data.map(
                            prato => <option key={prato.id} value={prato.id}>{prato.id} | {prato.nome}</option>));
                    }
                })
            }


            fetchPedidos();
            fetchPratos();
        },[]
    )


    return (
        <>
            <div className="menuLateralPrincipal">
                <h1><Link to={"/pedidos"}>Voltar</Link></h1>
            </div>
            <form className={"formPrato"} onSubmit={handleSubmit}>
                <select value={pedidoId} onChange={e => {
                    const value = parseInt(e.target.value)
                    if (!isNaN(value))
                        setPedidoId(value);
                }}>
                    <option value="">Pedidos</option>{pedidosOptions}
                </select>

                <select value={prato} onChange={e => {
                    if (e.target.value !== 0) setPrato(e.target.value);
                }}>
                    <option value="">Pratos</option>{pratoOptions}
                </select>

                <select value={estado} onChange={e => {
                    setEstado(e.target.value);
                }}>
                    <option value="">Estado</option>
                    <option value="Entregue">Entregue</option>
                    <option value="Não Entregue">Não Entregue</option>
                </select>
                <label>Quantidade</label>
                <input type="number" value={quantidade} onChange={e => {

                    setQuantidade(e.target.value)}}/>
                <button type={"submit"}>Enviar</button>
            </form>
        </>
    );
}