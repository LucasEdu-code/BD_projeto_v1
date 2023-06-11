import React, {useEffect, useState} from "react";
import {Link} from "react-router-dom";
import PratoInfoDiv from "../cardapio/editarPrato"
import {MesaInfoDiv} from "../Mesas/editarMesa";

export default function AdicionarPedido() {
    const [pratos, setPratos] = useState([])
    const [pratosOption, setPratosOption] = useState([])
    const [mesas, setMesas] = useState([])
    const [mesasOption, setMesasOption] = useState([])

    const [mesaId, setMesaId] = useState(0)
    const [pratoId, setPratoId] = useState(0)

    const [qnt, setQuantidade] = useState(0)


    function set_pratos_option() {
        if (pratos.length === 0) return;
        setPratosOption(pratos.map(prato => <option key={prato.id} value={prato.nome}>{prato.nome}</option>))
    }


    useEffect(() => {
        async function get_pratos() {
            fetch("http://localhost:8000/pratos")
                .then(response => {
                    if (response.ok) {
                        return response.json();
                    }
                    else throw response
                })
                .then(data => {
                    if (data !== undefined) {
                        setPratos(data)
                        if (data.length === 0) return;
                        setPratosOption(data.map(prato => <option key={prato.id} value={prato.id}>{prato.nome}</option>))
                    }
                })
                .catch(e => console.log("Erro ao buscar pratos"))
        }

        async function get_mesas() {
            fetch("http://localhost:8000/mesas").then(response => {
                    if (response.ok) {
                        return response.json();
                    }
                    else throw response
                })
                .then(data => {
                    setMesas(data)
                    if (data.length === 0) return;
                    setMesasOption(data.map(mesa => <option key={mesa.id} value={mesa.id}>{mesa.id}</option>))
                })
                .catch(e => console.log("Erro ao buscar mesas"))
        }

        get_pratos();
        get_mesas();

    },[])


    async function handleSubmit(e) {
        e.preventDefault();

        try {
            await fetch("http://localhost:8000/pedidos/criar",
                {
                    method: "POST",
                    headers: {"Content-Type":"application/json"},
                    body: JSON.stringify(
                        {
                            "id_mesa": mesaId,
                            "id_prato": pratoId,
                            "quantidade": qnt,
                            "entregue": false
                        }
                    )
                })
        } catch (e) {
            console.log(e)
        }
        window.history.back();
    }


    return(
        <>
            <div className="menuLateralPrincipal">
                <h1><Link to={"/pedidos"}>Voltar</Link></h1>
            </div>
            <form onSubmit={handleSubmit} className={"formPrato"}>
                <select value={mesaId} onChange={e => setMesaId(e.target.value)}>
                    <option value="">Mesas</option>
                    {mesasOption}
                </select>
                <select value={pratoId} onChange={e => setPratoId(e.target.value)}>
                    <option value="">Pratos</option>
                    {pratosOption}
                </select>
                <label>Quantidade:</label>
                <input type="number" value={qnt} onChange={e => setQuantidade(e.target.value)}/>
                <button type={"submit"}>Enviar</button>
            </form>
        </>
    );
}

