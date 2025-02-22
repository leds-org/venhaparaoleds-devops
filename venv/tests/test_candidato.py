import pytest
from src.candidato import Candidato

def test_candidato_corresponde_ao_concurso():
    candidato = Candidato("Teste", "01/01/2000", "123.456.789-00", ["carpinteiro"])
    assert candidato.corresponde_ao_concurso(["carpinteiro", "marceneiro"]) == True
    assert candidato.corresponde_ao_concurso(["professor"]) == False