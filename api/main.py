from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from api.models import Candidato, Concurso
from api.schemas import CandidatoResponse, ConcursoResponse
from api.database import SessionLocal, engine

# Inicializa a aplicação FastAPI
app = FastAPI()

# Função de dependência para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint para listar concursos associados a um CPF
@app.get("/concursos/{cpf}", response_model=List[ConcursoResponse])
def listar_concursos_por_cpf(cpf: str, db: Session = Depends(get_db)):
    candidato = db.query(Candidato).filter(Candidato.cpf == cpf).first()
    if not candidato:
        raise HTTPException(status_code=404, detail="Candidato não encontrado")

    # Filtra os concursos com base nas profissões do candidato
    profissoes_candidato = candidato.profissoes
    concursos = db.query(Concurso).all()
    concursos_filtrados = []

    for concurso in concursos:
        vagas_concurso = concurso.vagas
        if any(profissao in vagas_concurso for profissao in profissoes_candidato):
            concursos_filtrados.append(concurso)

    return concursos_filtrados

# Endpoint para listar candidatos associados a um código de concurso
@app.get("/candidatos/{codigo_concurso}", response_model=List[CandidatoResponse])
def listar_candidatos_por_concurso(codigo_concurso: str, db: Session = Depends(get_db)):
    concurso = db.query(Concurso).filter(Concurso.codigo == codigo_concurso).first()
    if not concurso:
        raise HTTPException(status_code=404, detail="Concurso não encontrado")

    # Filtra os candidatos com base nas profissões exigidas no concurso
    vagas_concurso = concurso.vagas
    candidatos = db.query(Candidato).all()
    candidatos_filtrados = []

    for candidato in candidatos:
        profissoes_candidato = candidato.profissoes
        if any(profissao in vagas_concurso for profissao in profissoes_candidato):
            candidatos_filtrados.append(candidato)

    return candidatos_filtrados
