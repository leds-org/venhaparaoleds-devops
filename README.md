# LedsChallenge - Documentação Completa

Este repositório é uma solução DevOps completa, abrangendo a configuração do **Dockerfile**, **Terraform**, **GitHub Actions** e a **Infraestrutura na AWS** para uma aplicação FastAPI. A seguir, você encontrará todos os detalhes das configurações, decisões tomadas e passos necessários para replicar e entender o processo.

## Índice

1. [Pré-requisitos](#pré-requisitos)
2. [Estrutura do Repositório](#estrutura-do-repositório)
3. [Dockerfile](#dockerfile)
4. [GitHub Actions](#github-actions)
5. [Terraform](#terraform)
   - [Provedor AWS](#provedor-aws)
   - [Repositório ECR](#repositório-ecr)
   - [Instância EC2](#instância-ec2)
   - [IAM e Políticas](#iam-e-políticas)
6. [Como funciona a API](#como-funciona-a-api)
7. [Infraestrutura AWS](#infraestrutura-aws)
8. [Passos para Rodar Localmente](#passos-para-rodar-localmente)
9. [Notas Finais](#notas-finais)

---

## 1. Pré-requisitos

Antes de começar, verifique se você tem as ferramentas e configurações necessárias em seu ambiente:

- **Docker**: Para construir e rodar containers.
- **Terraform**: Para provisionamento de infraestrutura na AWS.
- **AWS CLI**: Para gerenciar e configurar recursos AWS diretamente do seu terminal.
- **GitHub Actions**: Para automação do CI/CD.
- **Conta AWS**: Com permissões apropriadas para criar e gerenciar recursos como EC2, IAM, ECR, etc.

---

## 2. Estrutura do Repositório

O repositório segue uma estrutura simples, porém organizada, para facilitar a navegação e execução de todos os componentes necessários:

```
.
├── Dockerfile                  # Configuração da imagem Docker
├── requirements.txt            # Dependências Python
├── api/                        # Código da aplicação FastAPI
│   ├── main.py                 # Arquivo principal da aplicação
│   ├── schemas.py              # Definições dos schemas Pydantic
│   ├── models.py               # Modelos de dados
│   └── database.py             # Conexão com o banco de dados
├── tests/                      # Testes da aplicação
│   ├── conftest.py             # Configurações de testes
│   ├── test_candidatos.py      # Testes dos candidatos
│   └── test_concursos.py       # Testes dos concursos
├── terraform/                  # Infraestrutura com Terraform
│   ├── main.tf                 # Definições principais do Terraform
│   ├── variables.tf            # Variáveis do Terraform
│   └── outputs.tf              # Saídas do Terraform
├── .github/                    # Configurações do GitHub Actions
│   └── workflows/
│       └── deploy.yml          # Workflow de deploy
└── README.md                   # Documentação do projeto
```

---

## 3. Dockerfile

O `Dockerfile` define a imagem Docker necessária para rodar a aplicação FastAPI dentro de um container.

```dockerfile
# Usando a imagem base do Python 3.11 com uma versão slim para reduzir o tamanho da imagem
FROM python:3.11-slim

# Definindo uma variável de ambiente para a URL do banco de dados
ARG DATABASE_URL
ENV DATABASE_URL=$DATABASE_URL

# Definindo o diretório de trabalho dentro do container
WORKDIR /app

# Copiando o arquivo de dependências para dentro do container
COPY requirements.txt . 

# Instalando as dependências do requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiando todos os arquivos do diretório atual para dentro do container
COPY . .

# Expondo a porta 8000 para a aplicação FastAPI
EXPOSE 8000

# Comando para iniciar a aplicação FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

### Explicação:
- **FROM python:3.11-slim**: Usa a versão leve do Python 3.11.
- **COPY requirements.txt**: Copia o arquivo de dependências para o container.
- **RUN pip install**: Instala as dependências Python no container.
- **CMD**: Inicia o servidor `uvicorn` para rodar a aplicação FastAPI na porta 8000.

---

## 4. GitHub Actions

A configuração de CI/CD está automatizada no GitHub Actions. O workflow, localizado em `.github/workflows/deploy.yml`, define todos os passos para automação de build, testes e deploy.

### Workflow de Exemplo

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: ["main"]
  pull_request:
    branches: ["main"]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Run tests with coverage
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
        run: pytest --cov=api --cov-report=xml

  sonar:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3
      - name: Download coverage report
        uses: actions/download-artifact@v4
        with:
          name: coverage-report
      - name: Install SonarScanner
        run: |
          curl -sSLo sonar-scanner.zip https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-7.0.2.4839-linux-x64.zip
          unzip sonar-scanner.zip -d $HOME
          echo "$HOME/sonar-scanner-7.0.2.4839-linux-x64/bin" >> $GITHUB_PATH
      - name: Run SonarQube scan
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
        run: sonar-scanner \
          -Dsonar.organization=filipesuhett \
          -Dsonar.projectKey=filipesuhett_ledschallenge \
          -Dsonar.sources=api \
          -Dsonar.python.coverage.reportPaths=coverage.xml \
          -Dsonar.host.url=https://sonarcloud.io
```

Este workflow faz o seguinte:
1. **Testes**: Executa os testes e gera um relatório de cobertura.
2. **SonarQube**: Faz a análise de qualidade de código com SonarQube.
3. **Infraestrutura**: Provisiona a infraestrutura utilizando Terraform.
4. **Build Docker**: Constrói a imagem Docker.
5. **Deploy**: Realiza o deploy da aplicação na AWS.

---

## 5. Terraform

O **Terraform** é utilizado para provisionar a infraestrutura na AWS. A configuração está dividida nos seguintes arquivos:

### 5.1 Provedor AWS

Configuração para autenticar e interagir com a AWS:

```hcl
provider "aws" {
  region = var.aws_region
}
```

### 5.2 Repositório ECR

Configuração para criar um repositório ECR para armazenar as imagens Docker:

```hcl
resource "aws_ecr_repository" "app_repo" {
  name = "ledschallenge-repo"
}
```

### 5.3 Instância EC2

Provisiona uma instância EC2 para rodar a aplicação:

```hcl
resource "aws_instance" "app_instance" {
  ami           = var.ami_id
  instance_type = "t2.micro"
}
```

### 5.4 IAM e Políticas

Define as permissões necessárias para interagir com outros recursos da AWS:

```hcl
resource "aws_iam_role" "app_role" {
  name = "ledschallenge-role"
  assume_role_policy = data.aws_iam_policy_document.assume_role_policy.json
}
```

---

## 6. Como funciona a API

A aplicação foi desenvolvida utilizando **FastAPI** e se comunica com um banco de dados relacional via **SQLAlchemy**. A API possui dois endpoints principais para buscar concursos e candidatos com base em um CPF ou código do concurso.

### 6.1 Dependências da API

A API depende das seguintes bibliotecas principais:
- `fastapi`: Para criação dos endpoints.
- `sqlalchemy`: Para interagir com o banco de dados.
- `pydantic`: Para definição dos schemas de entrada e saída.

A conexão com o banco de dados é gerenciada pelo **SQLAlchemy** e a sessão do banco é obtida através da função `get_db()`.

### 6.2 Endpoints Disponíveis

#### **Listar Concursos por CPF**
**Rota:** `GET /concursos/{cpf}`

**Descrição:** Retorna a lista de concursos disponíveis para um candidato com base em seu CPF. O sistema verifica quais profissões o candidato possui e filtra os concursos compatíveis com essas profissões.

**Exemplo de Requisição:**
```http
GET /concursos/12345678900
```

**Exemplo de Resposta:**
```json
[
    {
        "orgao": "SEDU",
        "edital": "4/2017",
        "codigo": "8972983713",
        "vagas": ["Engenheiro", "Analista de TI"]
    }
]
```

**Possíveis Erros:**
- `404 Not Found`: Caso o CPF não seja encontrado no banco de dados.

---

#### **Listar Candidatos por Código de Concurso**
**Rota:** `GET /candidatos/{codigo_concurso}`

**Descrição:** Retorna a lista de candidatos compatíveis com um determinado concurso, com base nas profissões exigidas para as vagas disponíveis.

**Exemplo de Requisição:**
```http
GET /candidatos/CONCURSO123
```

**Exemplo de Resposta:**
```json
[
    {
        "nome": "João Silva",
        "cpf": "12345678900",
        "data_nascimento": "1976-05-19",
        "profissoes": ["Engenheiro"]
    }
]
```

**Possíveis Erros:**
- `404 Not Found`: Caso o código do concurso não seja encontrado no banco de dados.

---

### 6.3 Banco de Dados

A API utiliza um banco de dados relacional, onde há duas tabelas principais:
- **Candidatos** (`Candidato`): Contém informações dos candidatos, incluindo CPF, nome e profissões.
- **Concursos** (`Concurso`): Contém informações sobre os concursos, incluindo código, nome e as profissões exigidas.

Os relacionamentos entre essas tabelas permitem que a API filtre os concursos e candidatos de forma eficiente.

---

## 7. Infraestrutura AWS

Aqui você vai encontrar todas as configurações necessárias para rodar a aplicação na AWS, incluindo a criação de EC2, IAM, ECR, e mais. As configurações detalhadas estão localizadas na pasta `terraform`.

---

## 8. Passos para Rodar Localmente

Se você deseja rodar o projeto localmente, siga os passos abaixo:

1. **Instale as dependências**:
   - Certifique-se de que você tenha o `Docker` e o `Terraform` instalados.
   - Execute `pip install -r requirements.txt` para instalar as dependências Python.

2. **Rodando a aplicação com Docker**:
   - Construa a imagem Docker com o comando `docker build -t ledschallenge .`
   - Execute a aplicação com `docker run -p 8000:8000 ledschallenge`.

3. **Testando localmente**:
   - Use `pytest` para rodar os testes locais: `pytest`.

---

## 9. Notas Finais

Este repositório tem como objetivo proporcionar uma solução completa e automatizada para o deployment de uma aplicação FastAPI usando práticas de DevOps. Ele integra Terraform para provisionamento de infraestrutura, GitHub Actions para automação de CI/CD e Docker para a criação de ambientes isolados.

---