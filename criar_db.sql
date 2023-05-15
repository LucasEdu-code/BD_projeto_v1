
CREATE TABLE mesa(
	mesa_id integer PRIMARY KEY,
	numero_integrantes int NOT NULL DEFAULT 0,
	consumo_total float NOT NULL DEFAULT 0,
	pago bool DEFAULT false
);

CREATE TABLE cardapio (
	prato_id int PRIMARY KEY,
	prato_nome text NOT NULL DEFAULT ' ',
	prato_categoria text NOT NULL DEFAULT ' ',
	prato_tipo text NOT NULL DEFAULT ' ',
	prato_preco float NOT NULL DEFAULT 0
);

CREATE TABLE pedido (
	pedido_id int PRIMARY KEY,
	mesa_id int REFERENCES teste_schema.mesa (mesa_id) ON DELETE CASCADE,
	prato_id int REFERENCES teste_schema.cardapio (prato_id) ON DELETE CASCADE,
	quantidade int NOT NULL DEFAULT 1,
	entregue bool NOT NULL DEFAULT false,
	data_criacao timestamp NOT NULL
);