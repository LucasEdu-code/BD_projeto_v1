import logo from './logo.svg';
import './App.css';
import Mesas from "./pages/Mesas/Mesas";
import {Link, Outlet} from "react-router-dom";
export default function App() {
  return (
    <div className="App">
      <header>
        <nav className="menuSuperior">
            <img src="full_plate.png" alt="logo" width="64" height="64"/>
            <Link to={"/"}>Mesa</Link>
            <Link to={"pratos"}>Pratos</Link>
            <Link to={"pedidos"}>Pedidos</Link>
            <Link to={"clientes"}>Clientes</Link>
            <Link to={"metodos-de-pagamento"}>Métodos de Pagamento</Link>
        </nav>
      </header>
        <main>
            <Outlet />
        </main>
    </div>
  );
}