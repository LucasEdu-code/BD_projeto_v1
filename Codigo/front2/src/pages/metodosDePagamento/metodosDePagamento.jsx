import {Link} from "react-router-dom";
import React, {useEffect, useState} from "react";


function MetodosDiv(props) {
    const metodo = props.metodo
    if (metodo === undefined) return <></>


    return (
        <div>
            <h3>#{metodo.id} {metodo.nome}</h3>
        </div>
    )
}


export default function MetodosDePagamento() {
    const [metodos, setMetodos] = useState([]);
    useEffect(() => {
        async function fetchMetodos(){
            await fetch("http://localhost:8000/metodoPagamento")
                .then(response => response.json())
                .then(data => setMetodos(data))
        }

        fetchMetodos()
    }, [])


    const listaMetodos = metodos.map(metodo => <MetodosDiv key={metodo.id} metodo={metodo}></MetodosDiv>)


    return (
        <>
            <div className="menuLateralPrincipal">
                <h1><Link to={"adicionar"}>Adicionar</Link></h1>
                <h1><Link to={"remover"}>Remover</Link></h1>
                <h1><Link to={"editar"}>Alterar</Link></h1>
            </div>
            <div className="conteudoPratos">
                {listaMetodos}
            </div>
        </>
    )
}