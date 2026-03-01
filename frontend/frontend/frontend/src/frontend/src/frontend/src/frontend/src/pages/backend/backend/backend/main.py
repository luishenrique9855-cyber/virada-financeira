from fastapi import FastAPI, HTTPException
from sqlmodel import Session, select, create_engine
from init_db import Cartao, Compra, ParcelaCartao, Divida, ParcelaDivida, Renda, Gasto, DB_FILE
from sqlmodel import SQLModel
from typing import List
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "../db/virada.db")
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)

app = FastAPI(title="Virada Financeira API")

@app.on_event("startup")
def on_start():
    # garante que o DB exista
    SQLModel.metadata.create_all(engine)

# CARTÕES
@app.post("/cartoes")
def criar_cartao(cartao: Cartao):
    with Session(engine) as s:
        s.add(cartao)
        s.commit()
        s.refresh(cartao)
        return cartao

@app.get("/cartoes", response_model=List[Cartao])
def listar_cartoes():
    with Session(engine) as s:
        return s.exec(select(Cartao)).all()

# COMPRAS (cria parcelas e reduz limite)
@app.post("/compras")
def criar_compra(compra: Compra):
    with Session(engine) as s:
        cartao = s.get(Cartao, compra.cartao_id)
        if not cartao:
            raise HTTPException(404, "Cartão não encontrado")
        # reduzir limite imediatamente
        cartao.limite_utilizado += compra.valor_total
        s.add(cartao)
        s.commit()
        s.refresh(cartao)
        s.add(compra)
        s.commit()
        s.refresh(compra)
        # criar parcelas
        parcela_valor = round(compra.valor_total / max(1, compra.parcelas), 2)
        for i in range(1, compra.parcelas+1):
            # mes simples: mês atual + i-1 (formato YYYY-MM)
            from datetime import datetime
            m = datetime.now().month + i - 1
            y = datetime.now().year + (m-1)//12
            m = ((m-1) % 12) + 1
            mes = f"{y}-{m:02d}"
            p = ParcelaCartao(compra_id=compra.id, cartao_id=compra.cartao_id, num_parcela=i, mes=mes, valor=parcela_valor)
            s.add(p)
        s.commit()
        return compra

@app.get("/compras")
def listar_compras():
    with Session(engine) as s:
        return s.exec(select(Compra)).all()

# PARCELAS - marcar pagamento
@app.post("/parcelas/{parcela_id}/pagar")
def pagar_parcela(parcela_id: int):
    with Session(engine) as s:
        parcela = s.get(ParcelaCartao, parcela_id)
        if not parcela:
            raise HTTPException(404, "Parcela não encontrada")
        if parcela.status == "Pago":
            raise HTTPException(400, "Parcela já paga")
        parcela.status = "Pago"
        s.add(parcela)
        # restaurar limite proporcionalmente
        cartao = s.get(Cartao, parcela.cartao_id)
        if cartao:
            cartao.limite_utilizado -= parcela.valor
            if cartao.limite_utilizado < 0:
                cartao.limite_utilizado = 0
            s.add(cartao)
        s.commit()
        return {"ok": True}

# DÍVIDAS (simplificado)
@app.post("/dividas")
def criar_divida(divida: Divida):
    with Session(engine) as s:
        divida.saldo_restante = divida.valor_total
        s.add(divida)
        s.commit()
        s.refresh(divida)
        # criar parcelas de dívida
        parcela_valor = round(divida.valor_total / max(1, divida.parcelas), 2)
        from datetime import datetime
        for i in range(1, divida.parcelas+1):
            m = datetime.now().month + i - 1
            y = datetime.now().year + (m-1)//12
            m = ((m-1) % 12) + 1
            mes = f"{y}-{m:02d}"
            p = ParcelaDivida(divida_id=divida.id, num_parcela=i, mes=mes, valor=parcela_valor)
            s.add(p)
        s.commit()
        return divida

@app.post("/parcelas_divida/{parcela_id}/pagar")
def pagar_parcela_divida(parcela_id: int):
    with Session(engine) as s:
        parcela = s.get(ParcelaDivida, parcela_id)
        if not parcela:
            raise HTTPException(404, "Parcela não encontrada")
        if parcela.status == "Pago":
            raise HTTPException(400, "Parcela já paga")
        parcela.status = "Pago"
        s.add(parcela)
        # reduzir saldo da dívida
        divida = s.get(Divida, parcela.divida_id)
        if divida:
            divida.saldo_restante -= parcela.valor
            if divida.saldo_restante < 0:
                divida.saldo_restante = 0
            s.add(divida)
        s.commit()
        return {"ok": True}

# RENDAS / GASTOS / METAS (Endpoints básicos)
@app.post("/rendas")
def criar_renda(r: Renda):
    with Session(engine) as s:
        s.add(r)
        s.commit()
        s.refresh(r)
        return r

@app.get("/rendas")
def listar_rendas():
    with Session(engine) as s:
        return s.exec(select(Renda)).all()

@app.post("/gastos")
def criar_gasto(g: Gasto):
    with Session(engine) as s:
        s.add(g)
        s.commit()
        s.refresh(g)
        return g

@app.get("/gastos")
def listar_gastos():
    with Session(engine) as s:
        return s.exec(select(Gasto)).all()
