import React, {useEffect, useState} from "react";
import {Link} from "react-router-dom";

export function TipoInfoDiv(props) {
    let categoria = props.categoria
    if (categoria === undefined) return <></>
    return (
        <div className={"infoPrato"}>
            <h3>Categoria #{categoria.id} | {categoria.nome}</h3>
        </div>
    )
}





export default function EditarCategoria() {
    const [categorias, setCategorias] = useState([])
    const [categoriaId, setCategoriaId] = useState(0)
    const [categoriaInfo, setCategoriaInfo] = useState({})
    const [categoriaOptions, setCategoriaOptions] = useState([]);
    const [nome, setNome] = useState("")

    useEffect(() => {
        fetch("http://localhost:8000/categorias").then(response => response.json()).then(data => {
            setCategorias(data)
            setCategoriaOptions(categorias.map(tipo => <option key={tipo.id} value={tipo.id}>{tipo.id} | {tipo.nome}</option> ))
        })


        if (categoriaId !== 0)
            fetch(`http://localhost:8000/categorias/buscar/id/${categoriaId}`).then(response => response.json()).then(data => setCategoriaInfo(data))
    }, [categoriaId])


    async function handleSubmit(e) {
        e.preventDefault();

        try {
            await fetch(`http://localhost:8000/categorias/alterar/${categoriaId}`,
                {
                    method: "PUT",
                    headers: {"Content-Type":"application/json"},
                    body: JSON.stringify(
                        {
                            "nome": nome === "" ? undefined : nome,
                        }
                    )
                })
        }
        catch (e) {
            console.log(e)
        }
        window.history.back()
    }


    return (
        <>
            <div className="menuLateralPrincipal">
                <h1><Link to={"/pratos"}>Voltar</Link></h1>
            </div>

            <form onSubmit={handleSubmit} className={"formPrato"}>
                <select value={categoriaId} onChange={e => {
                    setCategoriaId(parseInt(e.target.value));
                }}>
                    <option value="">Tipos</option>{categoriaOptions}
                </select>
                <TipoInfoDiv tipo={categoriaInfo} />
                <label>Alterar Nome</label>
                <input type="text" value={nome} onChange={e => {
                    setNome(e.target.value)
                }}/>
                <button type={"submit"}>Enviar</button>
            </form>
        </>
    )
}