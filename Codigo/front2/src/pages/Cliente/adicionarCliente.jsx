import React, {useState} from "react";
import {Link} from "react-router-dom";

export default function AdicionarCliente() {
    const [nome, setNome] = useState("")
    const [cpf, setCPF] = useState("")

    async function handleSubmit(e) {
        e.preventDefault();

        await fetch("http://localhost:8000/cliente/criar",
            {
                method: "POST",
                headers: {"Content-Type":"application/json"},
                body: JSON.stringify(
                    {
                        "nome": nome,
                        "cpf": cpf
                    }
                )
            })
        window.history.go(-1)
    }


    return (
        <>
            <div className="menuLateralPrincipal">
                <h1><Link to={"/clientes"}> Voltar</Link></h1>
            </div>

            <form onSubmit={handleSubmit}>
                <label>Nome</label>
                <input type="text" value={nome} onChange={e => {
                    setNome(e.target.value)
                }}/>

                <label>CPF</label>
                <input type="text" value={cpf} onChange={e => {
                    setCPF(e.target.value)
                }}/>

                <button type={"submit"}>Enviar</button>
            </form>
        </>
    );
}