import ast

class Candidato:
    def __init__(self, nome: str, data_nascimento: str, cpf: str, profissoes: list):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.profissoes = profissoes

    @classmethod
    def de_linha(cls, linha: str):
        dados = linha.strip().split("\t")
        profissoes = ast.literal_eval(dados[3])  # Usa ast.literal_eval para processar a lista
        return cls(dados[0], dados[1], dados[2], profissoes)

    def corresponde_ao_concurso(self, vagas: list) -> bool:
        if vagas is None or self.profissoes is None:
            return False
        return any(profissao in vagas for profissao in self.profissoes)