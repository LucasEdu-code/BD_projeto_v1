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
