import React, {useEffect, useState} from "react";
import {Link} from "react-router-dom";

export default function RemoverTipo() {
    const [tipoId, setTipoId] = useState(0)
    const [tipos, setTipos] = useState([])
    let [tiposOptions, setTiposOption] = useState([]);


        useEffect(() => {
            fetch("http://localhost:8000/tipos").then(response => response.json()).then(data => {
                setTipos(data)
                setTiposOption(data.map(tipo => <option key={tipo.id} value={tipo.id}>{tipo.id} | {tipo.nome}</option> ))
            })
        }, [])


    async function handleSubmit(e){
        e.preventDefault();
        fetch(`http://localhost:8000/tipos/deletar/${tipoId}`, {
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
                    <select value={tipoId} onChange={e => {
                        setTipoId(e.target.value);
                    }}>
                        <option value="">Tipos</option>{tiposOptions}
                    </select>
                    <button type={"submit"}>Enviar</button>
                </form>
            </div>
        </>
    );
}