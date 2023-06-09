import {useState} from "react";

export default function AdicionarCategoria() {
    const [nome, setNome] = useState("")

    function handleSubmit(e) {
        e.preventDefault();

        fetch("http://localhost:8000/categorias/criar",
            {
                method: "POST",
                headers: {"Content-Type":"application/json"},
                body: JSON.stringify({"nome": nome})
            })
        window.history.back();
    }

    return (
        <>
            <form onSubmit={handleSubmit}>
                <label>Nome da categoria</label>
                <input type="text" value={nome} onChange={event => setNome(event.target.value)}/>
                <button type={"submit"}>Enviar</button>
            </form>
        </>
    )
}