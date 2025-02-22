import pytest # type: ignore
from src.concurso import Concurso

def test_concurso_corresponde_ao_candidato():
    concurso = Concurso("SEJUS", "1/2023", "12345", ["carpinteiro"])
    assert concurso.corresponde_ao_candidato(["carpinteiro", "marceneiro"]) == True
    assert concurso.corresponde_ao_candidato(["professor"]) == False

