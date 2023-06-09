import React, {useEffect, useState} from "react";
import {Link} from "react-router-dom";

export default function RemoverCategoria() {
    const [categoriaId, setCategoriaId] = useState(0)
    const [categorias, setCategorias] = useState([])
    let [categoriaOptions, setCategoriaOptions] = useState([]);


        useEffect(() => {
            fetch("http://localhost:8000/categorias").then(response => response.json()).then(data => {
                setCategorias(data)
                setCategoriaOptions(data.map(tipo => <option key={tipo.id} value={tipo.id}>{tipo.id} | {tipo.nome}</option> ))
            })
        }, [])


    async function handleSubmit(e){
        e.preventDefault();
        await fetch(`http://localhost:8000/categorias/deletar/${categoriaId}`, {
            method: "DELETE"
        })
        window.history.back();
    }


    return (
        <>
            <div className="menuLateralPrincipal">
                <h1><Link to={"/"}> Voltar</Link></h1>
            </div>
            <div className="conteudoAdicionar">
                <form onSubmit={handleSubmit}>
                    <select value={categoriaId} onChange={e => {
                        setCategoriaId(e.target.value);
                    }}>
                        <option value="">Categorias</option>{categoriaOptions}
                    </select>
                    <button type={"submit"}>Enviar</button>
                </form>
            </div>
        </>
    );
}