import React, {useEffect, useState} from "react";
import {Link} from "react-router-dom";

export default function RemoverPrato() {
    const [pratoId, setPratoID] = useState(0)
    const [pratos, setPratos] = useState([])
    let [pratosOptions, setPratoOptions] = useState([]);

    useEffect(() => {
        async function fetchData() {
            const _pratos = await fetch("http://localhost:8000/pratos").then(response => response.json())
            setPratos(_pratos)
            setPratoOptions(_pratos.map(_prato => <option key={_prato.id} value={_prato.id}>{_prato.id} | {_prato.nome}</option> ))
        }
        fetchData()
    }, [])

    async function handleSubmit(e){
        e.preventDefault();
        await fetch(`http://localhost:8000/pratos/deletar/${pratoId}`, {
            method: "DELETE"
        })
        window.history.back();
    }



    return (
        <>
            <div className="menuLateralPrincipal">
                <h1><Link to={"/pratos"}> Voltar</Link></h1>
            </div>
            <div className="conteudoAdicionar">
                <form onSubmit={handleSubmit}>
                    <select value={pratoId} onChange={e => {
                        setPratoID(e.target.value);
                    }}>
                        <option value="">Pratos</option>{pratosOptions}
                    </select>
                    <button type={"submit"}>Enviar</button>
                </form>
            </div>
        </>
    );

}