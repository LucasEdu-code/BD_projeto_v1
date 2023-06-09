import {Link} from "react-router-dom";
import React, {useEffect, useState} from "react";

import "./adicionarPrato.css"

export default function AdicionarPrato() {
    const [nome, setNome] = useState("")
    const [preco, setPreco] = useState("")
    const [categoria, setCategoria] = useState("")
    const [quantidade, setQuantidade] = useState(0)
    const [categoriasOptions, setCategoriasOptions] = useState([])
    const [tipo, setTipo] = useState("")
    const [tipos, setTipos] = useState([])
    const [tiposOptions, setTiposOptions] = useState([])

    useEffect(() => {
        async function fetchData() {
            const _tipos = await fetch("http://localhost:8000/tipos").then(response => response.json())
            const _categorias = await fetch("http://localhost:8000/categorias").then(response => response.json())
            setTipos(_tipos)
            setCategoria(_categorias)
            setTiposOptions(_tipos.map(__tipo => <option key={__tipo.id} value={__tipo.nome}>{__tipo.id} | {__tipo.nome}</option> ))
            setCategoriasOptions(_categorias.map(__categoria => <option key={__categoria.id} value={__categoria.nome}>{__categoria.id} | {__categoria.nome}</option> ))
        }

        fetchData();
    }, [])

    async function handleSubmit(e) {
        e.preventDefault();
        console.log(tipo)
        console.log(categoria)
        await fetch("http://localhost:8000/pratos/criar",
            {
                method: "POST",
                headers: {"Content-Type":"application/json"},
                body: JSON.stringify(
                    {
                        "nome": nome,
                        "preco": preco,
                        "categoria": categoria,
                        "tipo": tipo,
                        "quantidade_disponivel": quantidade
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
                <select value={categoria} onChange={e => {
                    setCategoria(e.target.value);
                }}>
                    <option value="0">Categorias</option>{categoriasOptions}
                </select>
                <select value={tipo} onChange={e => {
                    setTipo(e.target.value);
                }}>
                    <option value="0">Tipos</option>{tiposOptions}
                </select>
                <label> Quantidade Disponível</label>
                <input type="number" value={quantidade} onChange={e => {
                    setQuantidade(e.target.value)
                }}/>
                <button type={"submit"}>Enviar</button>
            </form>
        </>
    )
}