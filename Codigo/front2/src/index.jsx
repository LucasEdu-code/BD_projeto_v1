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
