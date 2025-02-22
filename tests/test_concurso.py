import pytest
from concurso import Concurso

def test_concurso_corresponde_ao_candidato():
    concurso = Concurso("SEJUS", "15/2017", "61828450843", ["carpinteiro", "professor de matemática", "assistente administrativo"])
    assert concurso.corresponde_ao_candidato(["carpinteiro", "marceneiro"]) == True
    assert concurso.corresponde_ao_candidato(["engenheiro"]) == False

def test_concurso_de_linha():
    linha = "SEJUS\t15/2017\t61828450843\t['carpinteiro', 'professor de matemática', 'assistente administrativo']"
    concurso = Concurso.de_linha(linha)
    assert concurso.orgao == "SEJUS"
    assert concurso.edital == "15/2017"
    assert concurso.codigo == "61828450843"
    assert concurso.vagas == ["carpinteiro", "professor de matemática", "assistente administrativo"]

def test_concurso_corresponde_ao_candidato_com_vagas_none():
    concurso = Concurso("SEJUS", "15/2017", "61828450843", None)
    assert concurso.corresponde_ao_candidato(["carpinteiro"]) == False

def test_concurso_corresponde_ao_candidato_com_profissoes_none():
    concurso = Concurso("SEJUS", "15/2017", "61828450843", ["carpinteiro"])
    assert concurso.corresponde_ao_candidato(None) == False