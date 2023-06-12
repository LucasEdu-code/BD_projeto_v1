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
	quantidade_disponivel int,
	PRIMARY KEY (id),
	FOREIGN KEY (categoria) REFERENCES categoria(id) ON DELETE RESTRICT,
	FOREIGN KEY (tipo) REFERENCES tipo(id) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS metodo_pagamento(
    id serial,
    nome text,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS pagamento (
	id serial,
	metodo_pagamento int,
	valor float,
	mesa int,
	cliente int,
	PRIMARY KEY (id, metodo_pagamento, mesa, cliente),
	FOREIGN KEY (metodo_pagamento) REFERENCES metodo_pagamento(id) ON DELETE RESTRICT,
	FOREIGN KEY (mesa) REFERENCES mesa(id) On DELETE NO ACTION,
	FOREIGN KEY (cliente) REFERENCES cliente(id) ON DELETE RESTRICT
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


CREATE VIEW pedido_info AS SELECT id_pedido(PE), id_mesa(PE), id_prato(PE), nome(PA) AS prato_nome,
                                       preco(PA) AS prato_preco, quantidade(PE), tipo(PA),
                                       nome(T) AS tipo_nome, categoria(PA), nome(C) AS categoria_nome, entregue(PE), data(PE)
                                       FROM pedido PE, prato PA, tipo T, categoria C
										WHERE id_prato(PE) = id(PA) AND categoria(PA) = id(C)
										AND tipo(PA) = id(T);


CREATE VIEW prato_info AS SELECT id(P), nome(P), preco(P), categoria(P), nome(C) AS categoria_nome,
                                 tipo(P), nome(T) AS tipo_nome, quantidade_disponivel(P)
                          FROM prato P, categoria C, tipo T
						  WHERE categoria(P) = id(C) AND tipo(P) = id(T);


CREATE VIEW pagamento_info AS SELECT P.id, Mp.nome as metodo_pagamento, P.valor, M.id as mesa,
                                     C.nome as cliente_nome, C.cpf as cliente_cpf
                                  FROM pagamento P, mesa M, cliente C, metodo_pagamento MP
								  WHERE P.metodo_pagamento = MP.id AND P.mesa = M.id AND
								        P.cliente = C.id;


CREATE PROCEDURE efetuar_pagamento(cliente_id int, mesa_id int, metodo_pagamento_id int) LANGUAGE plpgsql AS $$
    	DECLARE
    	    total float := 0;
    	BEGIN
			SELECT sum(P.quantidade*Pa.preco) INTO total FROM pedido P, prato PA WHERE id_mesa = mesa_id AND P.id_prato = PA.id;
			INSERT INTO pagamento (metodo_pagamento, valor, mesa, cliente) VALUES (metodo_pagamento_id, total, mesa_id, cliente_id);
    		DELETE FROM pedido WHERE id_mesa = mesa_id;
    		UPDATE mesa SET consumo_total = 0, pago = false WHERE id = mesa_id;
		end;
    $$
