import os
import pytest
from fastapi.testclient import TestClient
from api.main import app
from api.database import SessionLocal, engine, Base

# Configuração do banco de dados em memória para testes
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///:memory:")

# Fixture para criar e limpar o banco de dados para cada teste
@pytest.fixture(scope="function")
def test_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)  # Limpa o banco de dados após o teste

# Fixture para o cliente de testes
@pytest.fixture(scope="function")
def client():
    with TestClient(app) as client:
        yield client
