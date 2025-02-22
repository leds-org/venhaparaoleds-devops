# Stage 1: Build
FROM python:3.9-slim as builder
WORKDIR /app

# Copiar o arquivo de dependências
COPY requirements.txt .

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código-fonte e os arquivos de dados
COPY src/ ./src/
COPY candidatos.txt concursos.txt ./

# Stage 2: Run
FROM python:3.9-slim
WORKDIR /app

# Copiar as dependências instaladas do estágio anterior
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

# Copiar o código-fonte e os arquivos de dados
COPY --from=builder /app/src ./src
COPY --from=builder /app/candidatos.txt .
COPY --from=builder /app/concursos.txt .

# Definir o comando padrão
ENTRYPOINT ["python", "src/main.py"]