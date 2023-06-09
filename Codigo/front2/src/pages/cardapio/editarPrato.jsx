import React, {useEffect, useState} from "react";
import {Link} from "react-router-dom";
import "./adicionarPrato.css"

export function PratoInfoDiv(props) {
    let prato = props.prato
    if (prato.id === undefined) return <></>
    return (
        <div className={"infoPrato"}>
            <h3>Prato #{prato.id} | {prato.nome}</h3>
            <h3>Preço: {prato.preco}</h3>
            <h3>Categoria: {prato.categoria}</h3>
            <h3>Tipo: {prato.tipo}</h3>
        </div>
    )
}


export default function EditarPrato() {
    const [pratos, setPratos] = useState([])
    const [pratoId, setPratoID] = useState(0)
    const [pratoInfo, setPratoInfo] = useState({})
    const [pratosOptions, setPratoOptions] = useState([]);
    const [categoriasOptions, setCategoriasOptions] = useState([])
    const [tiposOptions, setTiposOptions] = useState([])

    const [nome, setNome] = useState("")
    const [categoria, setCategoria] = useState("")
    const [tipo, setTipo] = useState("")
    const [preco, setPreco] = useState(0)

    async function handleSubmit(e) {
        e.preventDefault();

        try {
            const response = await fetch(`http://localhost:8000/pratos/alterar/${pratoId}`,
                {
                    method: "PUT",
                    headers: {"Content-Type":"application/json"},
                    body: JSON.stringify(
                        {
                            "nome": nome === "" ? undefined : nome,
                            "preco": preco === 0 ? undefined : preco,
                            "categoria": categoria === "" ? undefined : categoria,
                            "tipo": tipo === "" ? undefined : tipo
                        }
                    )
                })
            console.log(response)
        }
        catch (e) {
            console.log(e)
        }
        window.history.back()
    }

    useEffect(() => {
        async function fetchData() {
            const _pratos = await fetch("http://localhost:8000/pratos").then(response => response.json())
            const _tipos = await fetch("http://localhost:8000/tipos").then(response => response.json())
            const _categorias = await fetch("http://localhost:8000/categorias").then(response => response.json())
            setPratoOptions(_pratos.map(prato => <option key={prato.id} value={prato.id}>{prato.id} | {prato.nome}</option> ))
            setTiposOptions(_tipos.map(__tipo => <option key={__tipo.id} value={__tipo.nome}>{__tipo.id} | {__tipo.nome}</option> ))
            setCategoriasOptions(_categorias.map(__categoria => <option key={__categoria.id} value={__categoria.nome}>{__categoria.id} | {__categoria.nome}</option> ))
            if (pratoId !== 0)
                fetch(`http://localhost:8000/pratos/buscar/id/${pratoId}`).then(response => response.json()).then(data => setPratoInfo(data))
        }

        fetchData();
    }, [pratoId])

    return (
        <>
            <div className="menuLateralPrincipal">
                <h1><Link to={"/pratos"}>Voltar</Link></h1>
            </div>
            <form onSubmit={handleSubmit} className={"formPrato"}>
                <select value={pratoId} onChange={e => {
                    const value = parseInt(e.target.value)
                    if (!isNaN(value))
                        setPratoID(value);
                    else setPratoID(0)
                }}>
                    <option value="">Pratos</option>{pratosOptions}
                </select>
                <PratoInfoDiv prato={pratoInfo}/>
                <label>Nome</label>
                <input type="text" value={nome} onChange={e => {
                    setNome(e.target.value)
                }}/>
                <label>Preco</label>
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

                <button type={"submit"}>Enviar</button>
            </form>
        </>
    )
}