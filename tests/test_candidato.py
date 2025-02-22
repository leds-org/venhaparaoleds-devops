import pytest
from src.candidato import Candidato

def test_candidato_corresponde_ao_concurso():
    # Caso 1: Há correspondência entre as profissões do candidato e as vagas do concurso
    candidato = Candidato("Teste", "01/01/2000", "123.456.789-00", ["carpinteiro"])
    assert candidato.corresponde_ao_concurso(["carpinteiro", "marceneiro"]) == True

    # Caso 2: Não há correspondência
    assert candidato.corresponde_ao_concurso(["professor"]) == False

    # Caso 3: Lista de vagas do concurso está vazia
    assert candidato.corresponde_ao_concurso([]) == False

    # Caso 4: Lista de profissões do candidato está vazia
    candidato_sem_profissoes = Candidato("Teste", "01/01/2000", "123.456.789-00", [])
    assert candidato_sem_profissoes.corresponde_ao_concurso(["carpinteiro"]) == False

    # Caso 5: Múltiplas correspondências
    candidato_multiplas_profissoes = Candidato("Teste", "01/01/2000", "123.456.789-00", ["carpinteiro", "marceneiro"])
    assert candidato_multiplas_profissoes.corresponde_ao_concurso(["carpinteiro", "pedreiro"]) == True

    # Caso 6: Nenhuma correspondência, mas as listas não estão vazias
    assert candidato_multiplas_profissoes.corresponde_ao_concurso(["engenheiro", "arquiteto"]) == False

def test_candidato_de_linha():
    # Testar o método de_linha (se existir)
    linha = "Teste;01/01/2000;123.456.789-00;carpinteiro,marceneiro"
    candidato = Candidato.de_linha(linha)
    assert candidato.nome == "Teste"
    assert candidato.data_nascimento == "01/01/2000"
    assert candidato.cpf == "123.456.789-00"
    assert candidato.profissoes == ["carpinteiro", "marceneiro"]