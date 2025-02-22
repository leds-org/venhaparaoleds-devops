import pytest
from src.candidato import Candidato

def test_candidato_corresponde_ao_concurso():
    # Caso 1: Há correspondência entre as profissões do candidato e as vagas do concurso
    candidato = Candidato("Lindsey Craft", "19/05/1976", "182.845.084-34", ["carpinteiro"])
    assert candidato.corresponde_ao_concurso(["carpinteiro", "marceneiro"]) == True

    # Caso 2: Não há correspondência
    assert candidato.corresponde_ao_concurso(["engenheiro"]) == False

    # Caso 3: Lista de vagas do concurso está vazia
    assert candidato.corresponde_ao_concurso([]) == False

    # Caso 4: Lista de profissões do candidato está vazia
    candidato_sem_profissoes = Candidato("Lindsey Craft", "19/05/1976", "182.845.084-34", [])
    assert candidato_sem_profissoes.corresponde_ao_concurso(["carpinteiro"]) == False

    # Caso 5: Múltiplas correspondências
    candidato_multiplas_profissoes = Candidato("Cory Mendoza", "11/02/1957", "565.512.353-92", ["carpinteiro", "marceneiro"])
    assert candidato_multiplas_profissoes.corresponde_ao_concurso(["carpinteiro", "pedreiro"]) == True

    # Caso 6: Nenhuma correspondência, mas as listas não estão vazias
    assert candidato_multiplas_profissoes.corresponde_ao_concurso(["engenheiro", "arquiteto"]) == False

def test_candidato_de_linha():
    # Testar o método de_linha
    linha = "Lindsey Craft\t19/05/1976\t182.845.084-34\t['carpinteiro']"
    candidato = Candidato.de_linha(linha)
    assert candidato.nome == "Lindsey Craft"
    assert candidato.data_nascimento == "19/05/1976"
    assert candidato.cpf == "182.845.084-34"
    assert candidato.profissoes == ["carpinteiro"]

def test_candidato_init():
    # Testar o método __init__
    candidato = Candidato("Lindsey Craft", "19/05/1976", "182.845.084-34", ["carpinteiro"])
    assert candidato.nome == "Lindsey Craft"
    assert candidato.data_nascimento == "19/05/1976"
    assert candidato.cpf == "182.845.084-34"
    assert candidato.profissoes == ["carpinteiro"]

def test_candidato_corresponde_ao_concurso_com_vagas_none():
    # Caso 7: Lista de vagas é None
    candidato = Candidato("Lindsey Craft", "19/05/1976", "182.845.084-34", ["carpinteiro"])
    assert candidato.corresponde_ao_concurso(None) == False

def test_candidato_corresponde_ao_concurso_com_profissoes_none():
    # Caso 8: Lista de profissões é None
    candidato = Candidato("Lindsey Craft", "19/05/1976", "182.845.084-34", None)
    assert candidato.corresponde_ao_concurso(["carpinteiro"]) == False