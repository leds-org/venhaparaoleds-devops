import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Obtém a URL de conexão com o banco de dados a partir de uma variável de ambiente
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///:memory:")

# Verifica se a variável de ambiente DATABASE_URL não está vazia
if not DATABASE_URL:
    raise ValueError("A variável de ambiente DATABASE_URL não está definida!")

# Cria uma engine de conexão com o banco de dados
engine = create_engine(DATABASE_URL)

# Configura a sessão do banco de dados (sem commit ou flush automáticos)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Cria a base para os modelos declarativos
Base = declarative_base()
