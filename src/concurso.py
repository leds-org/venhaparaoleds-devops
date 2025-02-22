import ast

class Concurso:
    def __init__(self, orgao: str, edital: str, codigo: str, vagas: list):
        self.orgao = orgao
        self.edital = edital
        self.codigo = codigo
        self.vagas = vagas

    @classmethod
    def de_linha(cls, linha: str):
        dados = linha.strip().split("\t")
        vagas = ast.literal_eval(dados[3])  # Usa ast.literal_eval para processar a lista
        return cls(dados[0], dados[1], dados[2], vagas)

    def corresponde_ao_candidato(self, profissoes: list) -> bool:
        return any(profissao in self.vagas for profissao in profissoes)