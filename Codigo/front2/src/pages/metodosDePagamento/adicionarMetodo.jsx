import React, {useState} from "react";
import {Link} from "react-router-dom";

export default function AdicionarMetodo() {
    const [nome, setNome] = useState("")


    async function handleSubmit(e) {
        e.preventDefault();

        await fetch("http://localhost:8000/metodoPagamento",
            {
                method: "POST",
                headers: {"Content-Type":"application/json"},
                body: JSON.stringify(
                    {
                        "nome": nome
                    }
                )
            })
        window.history.back();
    }


    return(
        <>
            <div className="menuLateralPrincipal">
                <h1><Link to={"/pedidos"}>Voltar</Link></h1>
            </div>
            <form onSubmit={handleSubmit} className={"formPrato"}>
                <label>Nome:</label>
                <input type="text" value={nome} onChange={e => setNome(e.target.value)}/>
                <button type={"submit"}>Enviar</button>
            </form>
        </>
    );
}