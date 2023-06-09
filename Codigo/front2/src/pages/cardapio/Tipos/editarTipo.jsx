import React, {useEffect, useState} from "react";
import {Link} from "react-router-dom";

export function TipoInfoDiv(props) {
    let tipo = props.tipo
    if (tipo.id_prato === undefined) return <></>
    return (
        <div className={"infoPrato"}>
            <h3>Prato #{tipo.id_prato} | {tipo.nome}</h3>
        </div>
    )
}





export default function EditarTipo() {
    const [tipos, setTipos] = useState([])
    const [tipoId, setTipoId] = useState(0)
    const [tipoInfo, setTipoInfo] = useState({})
    const [tipoOptions, setTipoOptions] = useState([]);
    const [nome, setNome] = useState("")

    useEffect(() => {
        fetch("http://localhost:8000/tipos").then(response => response.json()).then(data => {
            setTipos(data)
            setTipoOptions(data.map(tipo => <option key={tipo.id} value={tipo.id}>{tipo.id} | {tipo.nome}</option> ))
        })

        if (tipoId !== 0)
            fetch(`http://localhost:8000/tipos/buscar/id/${tipoId}`).then(response => response.json()).then(data => setTipoInfo(data))
    }, [tipoId])


    async function handleSubmit(e) {
        e.preventDefault();

        try {
            const response = await fetch(`http://localhost:8000/tipos/alterar/${tipoId}`,
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
                <select value={tipoId} onChange={e => {
                    const value = parseInt(e.target.value)
                    if (!isNaN(value))
                        setTipoId(value);
                }}>
                    <option value="">Tipos</option>{tipoOptions}
                </select>
                <TipoInfoDiv tipo={tipoInfo} />
                <label>Alterar Nome</label>
                <input type="text" value={nome} onChange={e => {
                    setNome(e.target.value)
                }}/>
                <button type={"submit"}>Enviar</button>
            </form>
        </>
    )
}