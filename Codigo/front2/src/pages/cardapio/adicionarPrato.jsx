import {Link} from "react-router-dom";
import React, {useState} from "react";

import "./adicionarPrato.css"

export default function AdicionarPrato() {
    const [nome, setNome] = useState("")
    const [preco, setPreco] = useState("")
    const [categoria, setCategoria] = useState("")
    const [tipo, setTipo] = useState("")

    async function handleSubmit(e) {
        e.preventDefault();

        fetch("http://localhost:8000/pratos/criar",
            {
                method: "POST",
                headers: {"Content-Type":"application/json"},
                body: JSON.stringify(
                    {
                        "nome": nome,
                        "preco": preco,
                        "categoria": categoria,
                        "tipo": tipo,
                    })
            })
        window.history.back()
    }

    return (
        <>
            <div className="menuLateralPrincipal">
                <h1><Link to={"/pratos"}> Voltar</Link></h1>
            </div>
            <form className={"formPrato"} onSubmit={handleSubmit}>
                <label> Nome do prato</label>
                <input type="text" value={nome} onChange={e => {
                    setNome(e.target.value)
                }}/>
                <label>Preço</label>
                <input type="number" value={preco} onChange={e => {
                    setPreco(e.target.value)
                }}/>
                <label>Categoria</label>
                <input type="text" value={categoria} onChange={e => {
                    setCategoria(e.target.value)
                }}/>
                <label>Tipo</label>
                <input type="text" value={tipo} onChange={e => {
                    setTipo(e.target.value)
                }}/>
                <button type={"submit"}>Enviar</button>
            </form>
        </>
    )
}