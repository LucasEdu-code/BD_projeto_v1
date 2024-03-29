import React, {useEffect, useState} from "react";
import {Link} from "react-router-dom";


export function MesaInfoDiv(props) {
    let mesa = props.mesa
    if (mesa.pago === undefined) return <></>

    return (
        <div>
            <h3>Mesa {mesa.id}</h3>
            <h3>Número de integrantes: {mesa.numero_integrantes}</h3>
            <h3>Consumo total: {mesa.consumo_total}</h3>
            <h3>está pago: {mesa.pago.toString()}</h3>
        </div>
    )
}


export default function EditarMesa() {
    const [mesas, setMesas] = useState([])
    const [mesaId, setMesaID] = useState(0)
    const [mesaInfo, setMesaInfo] = useState({})
    const [mesasOptions, setMesaOptions] = useState([]);

    const [numero, setNumero] = useState(0)
    const [estado, setEstado] = useState("")

    async function handleSubmit(e) {
        e.preventDefault();

        try {
            const response = await fetch(`http://localhost:8000/mesas/modificar/${mesaId}`,
                {
                    method: "PUT",
                    headers: {"Content-Type":"application/json"},
                    body: JSON.stringify(
                        {
                            "numero_integrantes": numero=== 0 ? undefined : numero,
                            "pago": estado === "" ? undefined : (estado === "Pago")
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
        fetch("http://localhost:8000/mesas").then(response => response.json()).then(data => {
            if (data !== undefined) {
                setMesas(data);
                setMesaOptions(data.map(mesa => <option key={mesa.id} value={mesa.id}>{mesa.id}</option>));
            }
        })

        if (mesaId !== 0)
            fetch(`http://localhost:8000/mesas/buscar/${mesaId}`).then(response => response.json()).then(data => setMesaInfo(data))
    }, [mesaId])

    return (
        <>
            <div className="menuLateralPrincipal">
                <h1><Link to={"/"}>Voltar</Link></h1>
            </div>
            <form onSubmit={handleSubmit}>
                <select value={mesaId} onChange={e => {
                    const value = parseInt(e.target.value)
                    if (!isNaN(value))
                        setMesaID(value);
                }}>
                    <option value="0">Mesas</option>{mesasOptions}
                </select>
                <input type="number" value={numero} onChange={e => {
                    setNumero(e.target.value)
                }}/>
                <select value={estado} onChange={e => {
                    setEstado(e.target.value);
                }}>
                    <option value="">Estado</option>
                    <option value="Não Pago">Não Pago</option>
                    <option value="Pago">Pago</option>
                </select>
                <MesaInfoDiv mesa={mesaInfo}/>
                <button type={"submit"}>Enviar</button>
            </form>
        </>
    )
}