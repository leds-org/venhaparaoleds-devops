FROM python:3.9-slim
WORKDIR /app
COPY src/ ./src/
COPY candidatos.txt concursos.txt ./
ENTRYPOINT ["python", "src/main.py"]