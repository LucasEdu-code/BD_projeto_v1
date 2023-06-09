import React, {useEffect, useState} from "react";
import {Link} from "react-router-dom";

export default function RemoverMesa() {
    const [mesaId, setMesaID] = useState(0)
    let [mesasOptions, setMesaOptions] = useState([]);

    useEffect(() => {
        fetch("http://localhost:8000/mesas").then(response => response.json()).then(data => {
            if (data !== undefined) {
                setMesaOptions(data.map(mesa => <option key={mesa.id} value={mesa.id}>{mesa.id}</option>));
            }
        })
    }, [])

    async function handleSubmit(e){
        e.preventDefault();
        await fetch(`http://localhost:8000/mesas/deletar/${mesaId}`, {
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
                    <select value={mesaId} onChange={e => {
                        setMesaID(e.target.value);
                    }}>
                        <option value="">Mesas</option>{mesasOptions}
                    </select>
                    <button type={"submit"}>Enviar</button>
                </form>
            </div>
        </>
    );

}