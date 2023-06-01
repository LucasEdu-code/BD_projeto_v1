import React, {useEffect, useState} from "react";
import {Link} from "react-router-dom";

export default function RemoverPedidos() {
    const [pedidoId, setPedidoId] = useState(0);
    const [pedidos, setPedidos] = useState([]);
    const [pedidosOptions, setPedidosOptions] = useState([]);

    useEffect(
        () => {
            fetch("http://localhost:8000/pedidos")
                .then(response => {
                    if (response.ok) return response.json()
                    else console.log(response)
                })
                .then(data => setPedidos(data))

            setPedidosOptions(pedidos.map(
                pedido => <option value={pedido.id_pedido} key={pedido.id_pedido}>id: {pedido.id_pedido} | prato: {pedido.prato_nome}</option>
            ))
        },
        [pedidos]
    );

    async function handleSubmit(e) {
        e.preventDefault();
        await fetch(`http://localhost:8000/pedidos/deletar/${pedidoId}`, {
            method: "DELETE"
        })
        window.history.back();
    }

    return (
        <>
            <div className="menuLateralPrincipal">
                <h1><Link to={"/"}> Voltar</Link></h1>
            </div>
            <div className="conteudoAdicionar">
                <form onSubmit={handleSubmit}>
                    <select value={pedidoId} onChange={e => {
                        setPedidoId(e.target.value);
                    }}>
                        <option value="">Pratos</option>{pedidosOptions}
                    </select>
                    <button type={"submit"}>Enviar</button>
                </form>
            </div>
        </>
    );
}