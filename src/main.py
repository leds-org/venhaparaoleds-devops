from candidato import Candidato
from concurso import Concurso

def carregar_candidatos(caminho_arquivo: str) -> list:
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        return [Candidato.de_linha(linha) for linha in arquivo.readlines()[1:]]  # Ignora cabeçalho

def carregar_concursos(caminho_arquivo: str) -> list:
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        return [Concurso.de_linha(linha) for linha in arquivo.readlines()[1:]]  # Ignora cabeçalho

def buscar_concursos_por_cpf(cpf: str, candidatos: list, concursos: list) -> list:
    candidato = next((c for c in candidatos if c.cpf == cpf), None)
    if not candidato:
        raise ValueError(f"CPF {cpf} não encontrado.")
    return [{"orgao": c.orgao, "codigo": c.codigo, "edital": c.edital} 
            for c in concursos if candidato.corresponde_ao_concurso(c.vagas)]

def buscar_candidatos_por_codigo_concurso(codigo: str, candidatos: list, concursos: list) -> list:
    concursos_encontrados = [c for c in concursos if c.codigo == codigo]
    if not concursos_encontrados:
        raise ValueError(f"Código {codigo} não encontrado.")
    return [{"nome": c.nome, "data_nascimento": c.data_nascimento, "cpf": c.cpf} 
            for c in candidatos if any(concurso.corresponde_ao_candidato(c.profissoes) for concurso in concursos_encontrados)]

if __name__ == "__main__":
    candidatos = carregar_candidatos("candidatos.txt")
    concursos = carregar_concursos("concursos.txt")
    print(buscar_concursos_por_cpf("182.845.084-34", candidatos, concursos))
    print(buscar_candidatos_por_codigo_concurso("61828450843", candidatos, concursos))