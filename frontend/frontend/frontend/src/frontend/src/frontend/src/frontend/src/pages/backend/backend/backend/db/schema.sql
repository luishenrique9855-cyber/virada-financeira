-- Schema básico para Virada Financeira

create table cartoes (
  id integer primary key autoincrement,
  nome text,
  limite_total numeric,
  limite_utilizado numeric default 0
);

create table compras (
  id integer primary key autoincrement,
  cartao_id integer,
  descricao text,
  valor_total numeric,
  parcelas integer,
  data text
);

create table parcelas_cartao (
  id integer primary key autoincrement,
  compra_id integer,
  cartao_id integer,
  num_parcela integer,
  mes text,
  valor numeric,
  status text
);

create table dividas (
  id integer primary key autoincrement,
  nome text,
  descricao text,
  valor_total numeric,
  parcelas integer,
  saldo_restante numeric
);

create table parcelas_divida (
  id integer primary key autoincrement,
  divida_id integer,
  num_parcela integer,
  mes text,
  valor numeric,
  status text
);

create table renda (
  id integer primary key autoincrement,
  tipo text,
  descricao text,
  valor numeric,
  data text
);

create table gastos (
  id integer primary key autoincrement,
  descricao text,
  categoria text,
  valor numeric,
  data text
);

create table metas (
  id integer primary key autoincrement,
  categoria text,
  percentual_ideal numeric
);
