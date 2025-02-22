import pytest
from src.concurso import Concurso

def test_concurso_corresponde_ao_candidato():
    # Caso 1: Há correspondência entre as profissões do candidato e as vagas do concurso
    concurso = Concurso("SEJUS", "1/2023", "12345", ["carpinteiro"])
    assert concurso.corresponde_ao_candidato(["carpinteiro", "marceneiro"]) == True

    # Caso 2: Não há correspondência
    assert concurso.corresponde_ao_candidato(["professor"]) == False

    # Caso 3: Lista de vagas do concurso está vazia
    concurso_sem_vagas = Concurso("SEJUS", "1/2023", "12345", [])
    assert concurso_sem_vagas.corresponde_ao_candidato(["carpinteiro"]) == False

    # Caso 4: Lista de profissões do candidato está vazia
    assert concurso.corresponde_ao_candidato([]) == False

    # Caso 5: Múltiplas correspondências
    concurso_multiplas_vagas = Concurso("SEJUS", "1/2023", "12345", ["carpinteiro", "marceneiro"])
    assert concurso_multiplas_vagas.corresponde_ao_candidato(["carpinteiro", "pedreiro"]) == True

    # Caso 6: Nenhuma correspondência, mas as listas não estão vazias
    assert concurso_multiplas_vagas.corresponde_ao_candidato(["engenheiro", "arquiteto"]) == False

def test_concurso_de_linha():
    # Testar o método de_linha (se existir)
    linha = "SEJUS;1/2023;12345;carpinteiro,marceneiro"
    concurso = Concurso.de_linha(linha)
    assert concurso.orgao == "SEJUS"
    assert concurso.edital == "1/2023"
    assert concurso.codigo == "12345"
    assert concurso.vagas == ["carpinteiro", "marceneiro"]