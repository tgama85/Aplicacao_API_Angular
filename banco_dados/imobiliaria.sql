--create database imobiliaria;

--criacao tabela endereco da imobiliaria
create table endereco(
	id_endereco serial primary key,
	rua varchar (255) not null,
	numero numeric (10) not null,
	andar numeric (10),
	bloco varchar (10),
	bairro varchar (100) not null,
	cidade varchar (255) not null,
	uf varchar (2) not null,
	cep varchar (10) not null
);

--criacao tabela cliente da imobiliaria
create table cliente(
	id_cliente serial primary key,
	id_endereco integer,
	nome varchar (255) not null,
	data_nascimento date not null,
	telefone numeric (11) not null,
	email varchar (100) not null,
	cpf varchar (14) not null,
	rg varchar (12) not null,
	estado_civil varchar (100) not null,
	profissao varchar (100) not null,
	foreign key (id_endereco)
		references endereco(id_endereco)
);

--criacao tabela proprietario da imobiliaria
create table proprietario(
	id_proprietario serial primary key,
	id_endereco integer,
	nome varchar (255) not null,
	data_nascimento date not null,
	telefone numeric (11) not null,
	email varchar (100) not null,
	cpf varchar (14) not null,
	rg varchar (12) not null,
	estado_civil varchar (100) not null,
	tempo_imovel varchar (50) not null,
	foreign key (id_endereco)
		references endereco(id_endereco)
);

--criacao tabela vendedor da imobiliaria
create table vendedor(
	id_vendedor serial primary key,
	id_endereco integer,
	nome varchar (255) not null,
	data_nascimento date not null,
	telefone numeric (11) not null,
	email varchar (100) not null,
	cpf varchar (14) not null,
	rg varchar (12) not null,
	cargo varchar (100) not null,
	foreign key (id_endereco)
		references endereco(id_endereco)
);

--criacao tabela tipo do imovel da imobiliaria
create table tipo_imovel(
	id_tipo serial primary key,
	casa boolean,
	apartamento boolean,
	kitnet boolean
);

--criacao tabela imovel da imobiliaria
create table imovel(
	id_imovel serial primary key,
	id_endereco integer,
	id_proprietario integer,
	id_tipo integer,
	valor_luz varchar (100) not null,
	valor_agua varchar (100) not null,
	condominio varchar (100) not null,
	propaganda varchar (100) not null,
	preco_total varchar (100) not null,
	foreign key (id_endereco)
		references endereco(id_endereco),
	foreign key (id_proprietario)
		references proprietario(id_proprietario),
	foreign key (id_tipo)
		references tipo_imovel(id_tipo)
);

--criacao tabela banco da imobiliaria
create table banco(
	id_banco serial primary key,
	nome_banco varchar (255) unique not null
);

--criacao tabela financiamento da imobiliaria
create table financiamento(
	id_financiamento serial primary key,
	id_banco integer,
	valor_financiado varchar (100) not null,
	valor_entrada varchar (100) not null,
	quantidade_parcela varchar (100) not null,
	foreign key (id_banco)
		references banco(id_banco)
);

--criacao tabela solicitacao de compra da imobiliaria
create table solicitacao_compra(
	id_solicitacao serial primary key,
	id_tipo integer,
	id_cliente integer,
	id_vendedor integer,
	id_financiamento integer,
	id_imovel integer,
	valor_venda varchar (100) not null,
	pagamento_vista varchar (100) not null,
	foreign key (id_tipo)
		references tipo_imovel(id_tipo),
	foreign key (id_cliente)
		references cliente(id_cliente),
	foreign key (id_vendedor)
		references vendedor(id_vendedor),
	foreign key (id_financiamento)
		references financiamento(id_financiamento),
	foreign key (id_imovel)
		references imovel(id_imovel)
);

