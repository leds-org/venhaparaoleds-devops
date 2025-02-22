import pytest
from candidato import Candidato

def test_candidato_corresponde_ao_concurso():
    candidato = Candidato("Lindsey Craft", "19/05/1976", "182.845.084-34", ["carpinteiro"])
    assert candidato.corresponde_ao_concurso(["carpinteiro", "marceneiro"]) == True
    assert candidato.corresponde_ao_concurso(["professor"]) == False

def test_candidato_de_linha():
    linha = "Lindsey Craft\t19/05/1976\t182.845.084-34\t[carpinteiro]"
    candidato = Candidato.de_linha(linha)
    assert candidato.nome == "Lindsey Craft"
    assert candidato.data_nascimento == "19/05/1976"
    assert candidato.cpf == "182.845.084-34"
    assert candidato.profissoes == ["carpinteiro"]

def test_candidato_corresponde_ao_concurso_com_vagas_none():
    candidato = Candidato("Lindsey Craft", "19/05/1976", "182.845.084-34", ["carpinteiro"])
    assert candidato.corresponde_ao_concurso(None) == False

def test_candidato_corresponde_ao_concurso_com_profissoes_none():
    candidato = Candidato("Lindsey Craft", "19/05/1976", "182.845.084-34", None)
    assert candidato.corresponde_ao_concurso(["carpinteiro"]) == False