from typing import List

class Concurso:
    def __init__(self, orgao: str, edital: str, codigo: str, vagas: List[str]):
        self.orgao = orgao
        self.edital = edital
        self.codigo = codigo
        self.vagas = [v.strip() for v in vagas]

    @staticmethod
    def de_linha(linha: str) -> 'Concurso':
        orgao, edital, codigo, vagas = linha.strip().split('\t')
        vagas = vagas.strip('[]')
        vagas = [vaga.strip() for vaga in vagas.split(',')]
        return Concurso(orgao, edital, codigo, vagas)

    def corresponde_ao_candidato(self, profissoes_candidato: List[str]) -> bool:
        return any(vaga.strip() in (p.strip() for p in profissoes_candidato) for vaga in self.vagas)