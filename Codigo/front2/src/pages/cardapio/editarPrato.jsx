import React, {useEffect, useState} from "react";
import {Link} from "react-router-dom";
import "./adicionarPrato.css"

export function PratoInfoDiv(props) {
    let prato = props.prato
    if (prato.id_prato === undefined) return <></>
    return (
        <div className={"infoPrato"}>
            <h3>Prato #{prato.id_prato} | {prato.prato_nome}</h3>
            <h3>Preço: {prato.preco}</h3>
            <h3>Categoria: {prato.prato_categoria}</h3>
            <h3>Tipo: {prato.prato_tipo}</h3>
        </div>
    )
}


export default function EditarPrato() {
    const [pratos, setPratos] = useState([])
    const [pratoId, setPratoID] = useState(0)
    const [pratoInfo, setPratoInfo] = useState({})
    const [pratosOptions, setPratoOptions] = useState([]);

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
        }
        catch (e) {
            console.log(e)
        }
        window.history.back()
    }

    useEffect(() => {
        fetch("http://localhost:8000/pratos").then(response => response.json()).then(data => setPratos(data))
        setPratoOptions(pratos.map(prato => <option key={prato.id_prato} value={prato.id_prato}>{prato.id_prato}</option> ))
        if (pratoId != 0)
            fetch(`http://localhost:8000/pratos/buscar/id/${pratoId}`).then(response => response.json()).then(data => setPratoInfo(data))
    }, [pratoId, pratos])

    return (
        <>
            <div className="menuLateralPrincipal">
                <h1><Link to={"/pratos"}>Voltar</Link></h1>
            </div>
            <form onSubmit={handleSubmit} className={"formPrato"}>
                <select value={pratoId} onChange={e => {
                    setPratoID(e.target.value);
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