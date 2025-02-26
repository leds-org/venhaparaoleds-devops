# Usando a imagem base do Python 3.11 com uma versão slim para reduzir o tamanho da imagem
FROM python:3.11-slim

# Definindo uma variável de ambiente para a URL do banco de dados
ARG DATABASE_URL
ENV DATABASE_URL=$DATABASE_URL

# Definindo o diretório de trabalho dentro do container para /app
WORKDIR /app

# Copiando o arquivo de dependências para dentro do container
COPY requirements.txt .

# Instalando as dependências a partir do requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiando todo o conteúdo do diretório atual para o diretório de trabalho dentro do container
COPY . .

# Expondo a porta 8000 para a aplicação web (FastAPI)
EXPOSE 8000

# Definindo o comando padrão para rodar a aplicação com o Uvicorn, que é um servidor ASGI
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
