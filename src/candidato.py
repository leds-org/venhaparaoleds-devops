from typing import List

class Candidato:
    def __init__(self, nome: str, data_nascimento: str, cpf: str, profissoes: List[str]):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.profissoes = [p.strip() for p in profissoes]

    @staticmethod
    def de_linha(linha: str) -> 'Candidato':
        nome, data_nascimento, cpf, profissoes = linha.strip().split('\t')
        profissoes = profissoes.strip('[]')
        profissoes = [prof.strip() for prof in profissoes.split(',')]
        return Candidato(nome, data_nascimento, cpf, profissoes)

    def corresponde_ao_concurso(self, vagas_concurso: List[str]) -> bool:
        return any(profissao.strip() in (v.strip() for v in vagas_concurso) for profissao in self.profissoes)