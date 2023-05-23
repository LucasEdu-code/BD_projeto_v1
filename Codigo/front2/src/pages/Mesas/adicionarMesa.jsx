import React, {useState} from "react";
import {Link} from "react-router-dom";

export default function AdicionarMesa() {
    const [quantidade, setQuantidade] = useState(0)

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch("http://localhost:8000/mesas/criar", {
                method: "POST",
                headers: {"Content-Type":"application/json"},
                body: JSON.stringify({"numero_integrantes": quantidade})
            })
        }
        catch (e) {
            console.log(e);
        }
        window.history.back();
    }
return (
    <>
        <div className="menuLateralPrincipal">
            <h1><Link to={"/"}> Voltar</Link></h1>
        </div>
        <div className="conteudoAdicionar">
            <form onSubmit={handleSubmit}>
                <label>Quantidade de Cadeiras</label>
                <input type="number" value={quantidade} onChange={e => {
                    setQuantidade(e.target.value)
                }}/>
                <button type={"submit"}>Enviar</button>
            </form>
        </div>
    </>

)
}