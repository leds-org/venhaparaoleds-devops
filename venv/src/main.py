from candidato import Candidato
from concurso import Concurso
from typing import List

def carregar_candidatos(caminho_arquivo: str) -> List[Candidato]:
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        return [Candidato.de_linha(linha) for linha in arquivo.readlines()[1:]]  # Ignora cabeçalho

def carregar_concursos(caminho_arquivo: str) -> List[Concurso]:
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        return [Concurso.de_linha(linha) for linha in arquivo.readlines()[1:]]  # Ignora cabeçalho

def buscar_concursos_por_cpf(cpf: str, candidatos: List[Candidato], concursos: List[Concurso]) -> List[dict]:
    candidato = next((c for c in candidatos if c.cpf == cpf), None)
    if not candidato:
        raise ValueError(f"CPF {cpf} não encontrado.")
    return [{"orgao": c.orgao, "codigo": c.codigo, "edital": c.edital} 
            for c in concursos if candidato.corresponde_ao_concurso(c.vagas)]

def buscar_candidatos_por_codigo_concurso(codigo: str, candidatos: List[Candidato], concursos: List[Concurso]) -> List[dict]:
    concursos_encontrados = [c for c in concursos if c.codigo == codigo]  # Pega todos os concursos com o código
    if not concursos_encontrados:
        raise ValueError(f"Código {codigo} não encontrado.")
    # Inclui candidatos compatíveis com qualquer um dos concursos
    return [{"nome": c.nome, "data_nascimento": c.data_nascimento, "cpf": c.cpf} 
            for c in candidatos if any(concurso.corresponde_ao_candidato(c.profissoes) for concurso in concursos_encontrados)]

if __name__ == "__main__":
    candidatos = carregar_candidatos("candidatos.txt")
    concursos = carregar_concursos("concursos.txt")
    print(buscar_concursos_por_cpf("182.845.084-34", candidatos, concursos))
    print(buscar_candidatos_por_codigo_concurso("61828450843", candidatos, concursos))