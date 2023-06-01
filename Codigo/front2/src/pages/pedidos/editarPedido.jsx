import React, {useEffect, useState} from "react";
import {Link} from "react-router-dom";

export default function EditarPedido() {
    const [pedidos, setPedidos] = useState([]);
    const [pedidoId, setPedidoId] = useState(0);
    const [pedidoInfo, setPedidoInfo] = useState({});
    const [pedidosOptions, setPedidosOptions] = useState([]);

    const [pratos, setPratos] = useState([])
    const [pratoOptions, setPratoOptions] = useState([])

    const [mesas, setMesas] = useState([])
    const [mesasOption, setMesaOptions] = useState([])



    const [mesa, setMesa] = useState(0)
    const [prato, setPrato] = useState(0)
    const [quantidade, setQuantidade] = useState()
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
                            "id_mesa": mesa === 0 ? undefined : mesa,
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
        //window.history.back();
    }
    
    useEffect(
        () => {
            fetch("http://localhost:8000/pedidos").then(response => response.json()).then(data => setPedidos(data))
            setPedidosOptions(pedidos.map(
                pedido => <option value={pedido.id_pedido} key={pedido.id_pedido}>id: {pedido.id_pedido} | prato: {pedido.prato_nome}</option>
            ))
            fetch("http://localhost:8000/pratos").then(response => response.json()).then(data => setPratos(data))
            setPratoOptions(pratos.map(prato => <option key={prato.id_prato} value={prato.id_prato}>{prato.id_prato} | {prato.prato_nome}</option> ))

            fetch("http://localhost:8000/mesas").then(response => response.json()).then(data => setMesas(data))
            setMesaOptions(mesas.map(mesa => <option key={mesa.id_mesa} value={mesa.id_mesa}>{mesa.id_mesa}</option> ))


            if (pedidoId != 0)
                fetch(`http://localhost:8000/pedidos/buscar/id/${pedidoId}`).then(response => response.json()).then(data => setPedidoInfo(data))
        },[mesas, pedidoId, pedidos, pratos]
    )


    return (
        <>
            <div className="menuLateralPrincipal">
                <h1><Link to={"/pedidos"}>Voltar</Link></h1>
            </div>
            <form className={"formPrato"} onSubmit={handleSubmit}>
                <select value={pedidoId} onChange={e => {
                    setPedidoId(e.target.value);
                }}>
                    <option value="">Pedidos</option>{pedidosOptions}
                </select>

                <select value={prato} onChange={e => {
                    if (e.target.value !== 0) setPrato(e.target.value);
                }}>
                    <option value="">Pratos</option>{pratoOptions}
                </select>

                <select value={mesa} onChange={e => {
                    setMesa(e.target.value);
                }}>
                    <option value="">Mesas</option>{mesasOption}
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