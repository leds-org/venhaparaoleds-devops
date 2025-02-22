
---

```markdown
# Projeto: Sistema de Gerenciamento de Concurso Público

Este projeto foi desenvolvido com o auxílio de ferramentas de Inteligência Artificial (IA) para aprimorar a qualidade do código, documentação e boas práticas. 

- **[DeepSeek](https://www.deepseek.com/)**: Para insights e otimizações no desenvolvimento.
- **[ChatGPT](https://openai.com/chatgpt)**: Para revisão de código, sugestões e documentação.
- **[Grok](https://grok.ai/)**: Para análises e recomendações técnicas.

---

Este projeto é uma aplicação Python que gerencia candidatos e concursos públicos, permitindo a busca de concursos compatíveis com o perfil de um candidato e a listagem de candidatos que se encaixam em um concurso específico.

---

## Funcionalidades

### Listar Concursos Compatíveis com um Candidato
- **Descrição**: Dado o CPF de um candidato, o sistema retorna os concursos públicos que se encaixam no seu perfil, com base nas profissões cadastradas.
- **Exemplo de Uso**:
  ```bash
  python src/main.py --cpf 12345678901
  ```

### Listar Candidatos Compatíveis com um Concurso
- **Descrição**: Dado o código de um concurso, o sistema retorna os candidatos que possuem profissões compatíveis com as vagas do concurso.
- **Exemplo de Uso**:
  ```bash
  python src/main.py --concurso 98765
  ```

---

## Como Executar o Projeto

### Pré-requisitos

- **Python 3.9 ou superior**:
  - [Documentação oficial do Python](https://www.python.org/doc/)
  - Para instalar o módulo `venv` no Python 3.12:
    ```bash
    sudo apt install python3.12-venv
    ```

- **Docker (opcional, para execução em contêiner)**:
  - [Documentação oficial do Docker](https://docs.docker.com/)
  - Para usar o Docker sem `sudo`, siga o guia oficial:
    [Manage Docker as a non-root user](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user)

---

### 1. Usar um Ambiente Virtual (Recomendado)

Para evitar conflitos com pacotes do sistema, é altamente recomendado usar um ambiente virtual. Siga os passos abaixo:

1. **Instale o módulo `venv`** (se ainda não estiver instalado):
   ```bash
   sudo apt install python3.12-venv
   ```

2. **Crie um ambiente virtual**:
   ```bash
   python3 -m venv venv
   ```

3. **Ative o ambiente virtual**:
   - No Linux/Mac:
     ```bash
     source venv/bin/activate
     ```
   - No Windows:
     ```bash
     venv\Scripts\activate
     ```

4. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Execute o projeto**:
   ```bash
   python src/main.py
   ```

6. **Desative o ambiente virtual** quando terminar:
   ```bash
   deactivate
   ```

---

### 2. Executando com Docker

Se preferir usar Docker, siga os passos abaixo:

1. **Construa a imagem Docker**:
   ```bash
   docker build -t concurso-publico .
   ```

2. **Execute o contêiner**:
   ```bash
   docker run concurso-publico
   ```

---

## Vantagens do Multistage Build com Chainguard

O uso de **multistage build** com a imagem base **Chainguard** traz várias vantagens para o projeto. Abaixo está o Dockerfile utilizado:

```Dockerfile
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
```

### Benefícios do Multistage Build com Chainguard

1. **Imagens menores**:
   - A imagem final contém apenas o necessário para executar a aplicação, resultando em uma imagem Docker menor e mais eficiente.

2. **Segurança reforçada**:
   - A Chainguard é uma imagem base minimalista e focada em segurança, reduzindo a superfície de ataque e minimizando riscos de vulnerabilidades.

3. **Desempenho**:
   - A imagem final é leve e otimizada, o que melhora o tempo de inicialização e o consumo de recursos.

4. **Facilidade de manutenção**:
   - O Dockerfile fica mais organizado, com estágios claramente definidos para build e runtime.

---

## Uso da Ferramenta Trivy no Pipeline

O **Trivy** é uma ferramenta de segurança que escaneia imagens Docker em busca de vulnerabilidades. Ele foi integrado ao pipeline de CI/CD para garantir que as imagens geradas estejam livres de vulnerabilidades críticas antes de serem enviadas para o GitHub Container Registry.

### Benefícios do Trivy

1. **Detecção de vulnerabilidades**:
   - O Trivy identifica vulnerabilidades em pacotes instalados na imagem Docker, como bibliotecas Python e dependências do sistema operacional.

2. **Integração contínua**:
   - O Trivy é executado automaticamente no pipeline de CI/CD, garantindo que todas as imagens sejam escaneadas antes de serem publicadas.

3. **Falha controlada**:
   - O pipeline é configurado para falhar se vulnerabilidades com severidade `HIGH` ou `CRITICAL` forem detectadas, garantindo que apenas imagens seguras sejam publicadas.

4. **Relatórios detalhados**:
   - O Trivy gera relatórios claros sobre as vulnerabilidades encontradas, facilitando a correção de problemas.

Exemplo de integração no pipeline:
```yaml
- name: Install Trivy
  run: |
    sudo apt-get update
    sudo apt-get install -y wget apt-transport-https gnupg lsb-release
    wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
    echo deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main | sudo tee -a /etc/apt/sources.list.d/trivy.list
    sudo apt-get update
    sudo apt-get install -y trivy

- name: Scan Docker image with Trivy
  run: |
    trivy image --severity HIGH,CRITICAL concurso-publico
```

---

## Licença

Este projeto está licenciado sob a licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.
```

---
