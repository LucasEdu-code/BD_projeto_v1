import React, {useEffect, useState} from "react";

export default function EditarMesa() {
    const [mesas, setMesas] = useState([])
    const [mesaId, setMesaID] = useState(0)
    const [mesaInfo, setMesaInfo] = useState({})
    let [mesasOptions, setMesaOptions] = useState([]);

    useEffect(() => {
        fetch("http://localhost:8000/mesas").then(response => response.json()).then(data => setMesas(data))
        setMesaOptions(mesas.map(mesa => <option key={mesa.id_mesa} value={mesa.id_mesa}>{mesa.id_mesa}</option> ))
    }, [mesas])

    return (
        <form>
            <select value={mesaId} onChange={e => {
                setMesaID(e.target.value);
                fetch(`http://localhost:8000/mesas/${mesaId}`).then(response => response.json()).then(data => setMesaInfo(data))
            }}>
                <option value="">Mesas</option>{mesasOptions}
            </select>
            <button type={"submit"}>Enviar</button>
        </form>
    )
}