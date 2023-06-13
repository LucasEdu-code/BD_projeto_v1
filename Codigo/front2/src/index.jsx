import React from 'react';
import ReactDOM from 'react-dom/client';
import {createBrowserRouter, RouterProvider} from "react-router-dom";
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

import AdicionarMesa from "./pages/Mesas/adicionarMesa";
import RemoverMesa from "./pages/Mesas/removerMesa";
import Mesas from "./pages/Mesas/Mesas";
import Pratos from "./pages/cardapio/pratos";
import EditarMesa from "./pages/Mesas/editarMesa";
import AdicionarPrato from "./pages/cardapio/adicionarPrato";
import RemoverPrato from "./pages/cardapio/removerPrato";
import EditarPrato from "./pages/cardapio/editarPrato";
import Pedidos from "./pages/pedidos/pedidos";
import AdicionarPedido from "./pages/pedidos/adicionarPedido";
import RemoverPedidos from "./pages/pedidos/removerPedidos";
import EditarPedido from "./pages/pedidos/editarPedido";
import Tipos from "./pages/cardapio/Tipos/tipos";
import AdicionarTipo from "./pages/cardapio/Tipos/adicionarTipo";
import EditarTipo from "./pages/cardapio/Tipos/editarTipo";
import RemoverTipo from "./pages/cardapio/Tipos/removerTipo";
import Categorias from "./pages/cardapio/Categoria/categoria";
import AdicionarCategoria from "./pages/cardapio/Categoria/adicionarCategoria";
import EditarCategoria from "./pages/cardapio/Categoria/editarCategoria";
import RemoverCategoria from "./pages/cardapio/Categoria/removerCategoria";
import FiltrarPorTempo from "./pages/pedidos/Filtros/filtrarPorTempo/FiltrarPorTempo";
import FiltrarPorPrato from "./pages/pedidos/Filtros/filtrarPorPrato/filtrarPorPrato";
import FiltrarPorCategoria from "./pages/pedidos/Filtros/filtrarPorCategoria/filtrarPorCategoria";
import FiltrarPorTipo from "./pages/pedidos/Filtros/filtrarPorTipo/filtrarPorTipo";
import Clientes from "./pages/Cliente/clientes";
import AdicionarCliente from "./pages/Cliente/adicionarCliente";
import RemoverCliente from "./pages/Cliente/removerCliente";
import EditarCliente from "./pages/Cliente/editarCliente";
import PagamentoCliente from "./pages/Cliente/pagamentoCliente";
import BuscarPagamentos from "./pages/Cliente/buscarPagamentos";
import MetodosDePagamento from "./pages/metodosDePagamento/metodosDePagamento";
import AdicionarMetodo from "./pages/metodosDePagamento/adicionarMetodo";
import RemoverMetodo from "./pages/metodosDePagamento/removerMetodo";

const router = createBrowserRouter([
    {
        path: "/",
        element: <App />,
        children: [
            {
                path: "",
                element: <Mesas />
            },
            {
                path: "/criar_mesa",
                element: <AdicionarMesa />
            },
            {
                path: "/remover_mesa",
                element: <RemoverMesa />
            },
            {
                path: "/editar_mesa",
                element: <EditarMesa />
            },
            {
                path: "/pratos",
                element: <Pratos />
            },
            {
                path: "/pratos/tipos",
                element: <Tipos />
            },
            {
                path: "/pratos/tipos/adicionar",
                element: <AdicionarTipo />
            },
            {
                path: "/pratos/tipos/editar",
                element: <EditarTipo />
            },
            {
                path: "/pratos/tipos/remover",
                element: <RemoverTipo />
            },
            {
                path: "/pratos/categorias",
                element: <Categorias />
            },
            {
                path: "/pratos/categorias/adicionar",
                element: <AdicionarCategoria />
            },
            {
                path: "/pratos/categorias/editar",
                element: <EditarCategoria />
            },
            {
                path: "/pratos/categorias/remover",
                element: <RemoverCategoria />
            },
            {
                path: "/pratos/adicionar_prato",
                element: <AdicionarPrato />
            },
            {
                path: "/pratos/remover_prato",
                element: <RemoverPrato />
            },
            {
                path: "/pratos/editar_prato",
                element: <EditarPrato />
            },
            {
                path: "/pedidos",
                element: <Pedidos />
            },
            {
                path: "/pedidos/filtrarPorTempo",
                element: <FiltrarPorTempo />
            },
            {
                path: "/pedidos/filtrarPorPrato",
                element: <FiltrarPorPrato />
            },
            {
                path: "/pedidos/filtrarPorCategoria",
                element: <FiltrarPorCategoria />
            },
            {
                path: "/pedidos/filtrarPorTipo",
                element: <FiltrarPorTipo />
            },
            {
                path: "/pedidos/adicionar",
                element: <AdicionarPedido />
            },
            {
                path: "/pedidos/remover",
                element: <RemoverPedidos />
            },
            {
                path: "/pedidos/editar",
                element: <EditarPedido />
            },
            {
                path: "/clientes",
                element: <Clientes />
            },
            {
                path: "/clientes/adicionar",
                element: <AdicionarCliente />
            },
            {
                path: "/clientes/remover",
                element: <RemoverCliente />
            },
            {
                path: "/clientes/editar",
                element: <EditarCliente />
            },
            {
                path: "/clientes/pagar",
                element: <PagamentoCliente />
            },
            {
                path: "/clientes/buscar-pagamento",
                element: <BuscarPagamentos />
            },
            {
                path: "/metodos-de-pagamento",
                element: <MetodosDePagamento />
            },
            {
                path: "/metodos-de-pagamento/adicionar",
                element: <AdicionarMetodo />
            },
            {
                path: "/metodos-de-pagamento/remover",
                element: <RemoverMetodo />
            }
        ]
    }
])

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
      <link rel="icon" href="plate.png" />
      <RouterProvider router={router} />
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
