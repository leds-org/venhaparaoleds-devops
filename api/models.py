from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.dialects.postgresql import JSONB
from api.database import Base

# Definição da tabela Candidato
class Candidato(Base):
    __tablename__ = "candidato"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    data_nascimento = Column(Date, nullable=False)
    cpf = Column(String(14), unique=True, nullable=False)
    profissoes = Column(JSONB, nullable=False)

# Definição da tabela Concurso
class Concurso(Base):
    __tablename__ = "concurso"
    id = Column(Integer, primary_key=True, index=True)
    orgao = Column(String(50), nullable=False)
    edital = Column(String(10), nullable=False)
    codigo = Column(String(14), unique=True, nullable=False)
    vagas = Column(JSONB, nullable=False)
