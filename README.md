```markdown
# Concurso Público - Automação CI/CD

## Descrição
Este projeto é uma solução para buscar concursos públicos compatíveis com candidatos e vice-versa, utilizando os arquivos `candidatos.txt` e `concursos.txt`. A automação do processo de integração e entrega contínua (CI/CD) garante a qualidade do código e a eficiência na implantação.

## Tecnologias
- **Python 3.9**: Linguagem principal do projeto.
- **pytest**: Framework para execução de testes unitários.
- **Docker**: Containerização da aplicação para garantir consistência entre ambientes.
- **GitHub Actions**: Automação do pipeline de CI/CD.
- **SonarQube**: Análise estática de código para garantir a qualidade.

## CI/CD
O pipeline de CI/CD inclui as seguintes etapas:

1. **Execução de Testes**:
   - Utiliza `pytest` para executar testes unitários.
   - Falha se a cobertura de testes for inferior a 80%.

2. **Análise de Qualidade**:
   - Utiliza o SonarQube para análise estática de código.
   - Verifica bugs, vulnerabilidades e code smells.

3. **Construção e Publicação da Imagem Docker**:
   - Constrói a imagem Docker da aplicação.
   - Publica a imagem no GitHub Packages apenas em push para o branch `main`.

## Como Executar

### Pré-requisitos
- Docker instalado.
- Git instalado.

### Passos

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/AgnerLoss/venhaparaoleds-devops.git
   cd venhaparaoleds-devops
   ```

2. **Construa a imagem Docker**:
   ```bash
   docker build -t concurso-publico .
   ```

3. **Execute o contêiner**:
   ```bash
   docker run concurso-publico
   ```

### Executando Testes Localmente
Para executar os testes unitários localmente:
```bash
pip install pytest pytest-cov
pytest tests/ --cov=src --cov-report=term-missing
```

## Diferenciais
- **Clean Code**: Código limpo e bem estruturado, seguindo boas práticas de desenvolvimento.
- **Testes Unitários**: Cobertura de testes superior a 80%, garantindo a qualidade do código.
- **Dockerização**: Facilidade de implantação e consistência entre ambientes.
- **Automação CI/CD**: Pipeline automatizado com GitHub Actions para integração e entrega contínua.

## Licença
Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
```

