CREATE TABLE IF NOT EXISTS mesa (
	id serial,
	numero_integrantes integer,
	consumo_total float,
	pago bool,
	PRIMARY KEY (id)
);


CREATE TABLE IF NOT EXISTS cliente (
    id serial,
    nome text,
    cpf text,
    mesa int,
    forma_de_pagamento text,
    valor_total float,
    PRIMARY KEY (id)
);


CREATE TABLE IF NOT EXISTS categoria (
    id serial,
    nome text,
    PRIMARY KEY (id)
);


CREATE TABLE IF NOT EXISTS tipo (
    id serial,
    nome text,
    PRIMARY KEY (id)
);


CREATE TABLE IF NOT EXISTS prato (
	id serial,
	nome text,
	preco float,
	categoria int,
	tipo int,
	PRIMARY KEY (id),
	FOREIGN KEY (categoria) REFERENCES categoria(id) ON DELETE RESTRICT,
	FOREIGN KEY (tipo) REFERENCES tipo(id) ON DELETE RESTRICT
);


CREATE TABLE IF NOT EXISTS pedido (
	id_pedido serial,
	id_mesa integer,
	id_prato integer,
	quantidade integer,
	entregue bool,
	data timestamp,
	PRIMARY KEY (id_pedido),
	FOREIGN KEY (id_mesa) REFERENCES mesa(id) ON DELETE RESTRICT,
	FOREIGN KEY (id_prato) REFERENCES prato(id) ON DELETE RESTRICT
);
