# Concurso Público - Automação CI/CD

## Descrição
Solução para buscar concursos públicos compatíveis com candidatos e vice-versa, utilizando os arquivos `candidatos.txt` e `concursos.txt`.

## Tecnologias
- Python 3.9
- pytest (testes)
- Docker (containerização)
- GitHub Actions (CI/CD)
- SonarQube (qualidade de código)

## CI/CD
O pipeline:
1. Executa testes com `pytest` (falha se cobertura < 80%)
2. Analisa qualidade com SonarQube
3. Constrói e publica a imagem Docker no GitHub Packages (apenas em push para main)

## Como Executar
1. Clone o repositório
2. `docker build -t concurso-publico .`
3. `docker run concurso-publico`

## Diferenciais
- Clean Code
- Testes unitários
- Dockerização