from sqlmodel import SQLModel, create_engine
from sqlmodel import Field, Session
from typing import Optional
import os

DB_FILE = os.path.join(os.path.dirname(__file__), "../db/virada.db")
if not os.path.isdir(os.path.dirname(DB_FILE)):
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
engine = create_engine(f"sqlite:///{DB_FILE}", echo=False)

class Cartao(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    limite_total: float
    limite_utilizado: float = 0.0

class Compra(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cartao_id: int
    descricao: str
    valor_total: float
    parcelas: int
    data: str

class ParcelaCartao(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    compra_id: int
    cartao_id: int
    num_parcela: int
    mes: str
    valor: float
    status: str = "Pendente"

class Divida(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    descricao: str
    valor_total: float
    parcelas: int
    saldo_restante: float

class ParcelaDivida(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    divida_id: int
    num_parcela: int
    mes: str
    valor: float
    status: str = "Pendente"

class Renda(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tipo: str
    descricao: str
    valor: float
    data: str

class Gasto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    descricao: str
    categoria: str
    valor: float
    data: str

class Meta(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    categoria: str
    percentual_ideal: float

def init_db():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        # seed básico
        if not session.exec("SELECT 1").one_or_none():
            pass
        c1 = Cartao(nome="Cartão Básico", limite_total=2000.0)
        session.add(c1)
        session.commit()

if __name__ == "__main__":
    init_db()
    print("Banco criado.")
