CREATE SCHEMA IF NOT EXISTS historico;


CREATE TABLE IF NOT EXISTS historico.mesa (
	id_mesa integer,
	numero_integrantes integer,
	consumo_total float,
	pago bool,
	PRIMARY KEY (id_mesa)
);

CREATE TABLE IF NOT EXISTS historico.prato (
	id_prato integer,
	prato_nome text,
	preco float,
	prato_categoria text,
	prato_tipo text,
	PRIMARY KEY (id_prato)
);

CREATE TABLE IF NOT EXISTS historico.pedido (
	id_pedido integer,
	id_mesa integer,
	id_prato integer,
	quantidade integer,
	entregue bool,
	data timestamp,
	PRIMARY KEY (id_pedido),
	FOREIGN KEY (id_mesa) REFERENCES historico.mesa(id_mesa) ON DELETE RESTRICT,
	FOREIGN KEY (id_prato) REFERENCES historico.prato(id_prato) ON DELETE RESTRICT
);
