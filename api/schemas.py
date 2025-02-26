from pydantic import BaseModel, ConfigDict
from typing import List
from datetime import date

# Definição do schema base para Candidato
class CandidatoBase(BaseModel):
    nome: str
    data_nascimento: date
    cpf: str
    profissoes: List[str]

# Definição do schema base para Concurso
class ConcursoBase(BaseModel):
    orgao: str
    edital: str
    codigo: str
    vagas: List[str]

# Respostas para a API com configurações para Pydantic
class CandidatoResponse(CandidatoBase):
    model_config = ConfigDict(from_attributes=True)

class ConcursoResponse(ConcursoBase):
    model_config = ConfigDict(from_attributes=True)
