import React, {useEffect, useState} from "react";
import {Link} from "react-router-dom";

function PratoDiv(props) {
    const prato = props.prato

    return (
        <div className={"pratos"}>
            <h3>#{prato.id} {prato.nome} R$ {prato.preco} | Quantidade Disponível: {prato.quantidade_disponivel} | Categoria: {prato.categoria_nome} | Tipo: {prato.tipo_nome}</h3>
        </div>
    )
}

export default function Pratos() {
    const [pratos, setPratos] = useState([])

    useEffect(() => {
        fetch("http://localhost:8000/pratos")
            .then(response => {
                if (response.ok) {
                    return response.json();
                }
                else {
                    throw response
                }
            }).then(data => setPratos(data))
            .catch(error => {
                console.log("Error ao buscar pratos");
            })

    }, [])

    const listaPratos = pratos.map(prato => <PratoDiv key={prato.id} prato={prato}></PratoDiv>)

    return (
        <>
            <div className="menuLateralPrincipal">
                <h1><Link to={"adicionar_prato"}>Adicionar Prato</Link></h1>
                <h1><Link to={"remover_prato"}>Remover Prato</Link></h1>
                <h1><Link to={"editar_prato"}>Alterar Prato</Link></h1>
                <h1><Link to={"tipos"}>Tipos</Link></h1>
                <h1><Link to={"categorias"}>Categoria</Link></h1>
            </div>
            <div className="conteudoPratos">{listaPratos}</div>
        </>
    )
}