# Stage 1: Build
FROM cgr.dev/chainguard/python:latest-dev as builder
WORKDIR /app

# Copiar o arquivo de dependências
COPY requirements.txt .

# Criar um ambiente virtual e instalar as dependências
RUN python3 -m venv /app/venv && \
    /app/venv/bin/pip install --no-cache-dir -r requirements.txt

# Copiar o código-fonte e os arquivos de dados
COPY src/ ./src/
COPY candidatos.txt concursos.txt ./

# Stage 2: Run
FROM cgr.dev/chainguard/python:latest
WORKDIR /app

# Copiar o ambiente virtual e as dependências do estágio anterior
COPY --from=builder /app/venv /app/venv

# Copiar o código-fonte e os arquivos de dados
COPY --from=builder /app/src ./src
COPY --from=builder /app/candidatos.txt .
COPY --from=builder /app/concursos.txt .

# Configurar o PATH para usar o ambiente virtual
ENV PATH="/app/venv/bin:$PATH"

# Definir o comando padrão
ENTRYPOINT ["python", "src/main.py"]