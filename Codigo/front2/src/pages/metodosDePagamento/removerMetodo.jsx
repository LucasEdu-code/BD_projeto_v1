import React, {useEffect, useState} from "react";
import {Link} from "react-router-dom";

export default function RemoverMetodo() {
    const [metodos, setMetodos] = useState([]);
    const [metodoId, setMetodoId] = useState(0);

    useEffect(() => {
        async function fetchMetodo() {
            fetch("http://localhost:8000/metodoPagamento")
                .then(response => response.json())
                .then(data => setMetodos(data.map(metodo => <option key={metodo.id} value={metodo.id}>{metodo.nome}</option>)))
        }

        fetchMetodo();
    }, [])


    async function handleSubmit(e) {
        e.preventDefault();

        await fetch(`http://localhost:8000/metodoPagamento/${metodoId}`, {
            method: "DELETE"
        })
        window.history.back();
    }

    return(
        <>
            <div className="menuLateralPrincipal">
                <h1><Link to={"/pedidos"}>Voltar</Link></h1>
            </div>
            <form onSubmit={handleSubmit} className={"formPrato"}>
                <select value={metodoId} onChange={e => {
                    const temp = parseInt(e.target.value)
                    if (!isNaN(temp)) setMetodoId(temp)
                }}>
                    <option value="">Metodos</option>
                    {metodos}
                </select>
                <button type={"submit"}>Enviar</button>
            </form>
        </>
    );

}