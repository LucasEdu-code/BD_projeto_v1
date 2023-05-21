CREATE TABLE IF NOT EXISTS mesa (
	id_mesa serial,
	numero_integrantes integer,
	consumo_total float,
	pago bool,
	PRIMARY KEY (id_mesa)
);

CREATE TABLE IF NOT EXISTS prato (
	id_prato serial,
	prato_nome text,
	preco float,
	prato_categoria text,
	prato_tipo text,
	PRIMARY KEY (id_prato)
);

CREATE TABLE IF NOT EXISTS pedido (
	id_pedido serial,
	id_mesa integer,
	id_prato integer,
	quantidade integer,
	entregue bool,
	data timestamp,
	PRIMARY KEY (id_pedido),
	FOREIGN KEY (id_mesa) REFERENCES mesa(id_mesa) ON DELETE RESTRICT,
	FOREIGN KEY (id_prato) REFERENCES prato(id_prato) ON DELETE RESTRICT
);
