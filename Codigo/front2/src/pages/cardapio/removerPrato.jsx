import React, {useEffect, useState} from "react";
import {Link} from "react-router-dom";

export default function RemoverPrato() {
    const [pratoId, setPratoID] = useState(0)
    const [pratos, setPratos] = useState([])
    let [pratosOptions, setPratoOptions] = useState([]);

    useEffect(() => {
        fetch("http://localhost:8000/pratos").then(response => response.json()).then(data => setPratos(data))
        setPratoOptions(pratos.map(prato => <option key={prato.id_mesa} value={prato.id_prato}>{prato.id_prato}</option> ))
    }, [pratos])

    async function handleSubmit(e){
        e.preventDefault();
        fetch(`http://localhost:8000/pratos/deletar/${pratoId}`, {
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