import pytest

def test_listar_concursos_por_cpf(client):
    # Testa o endpoint /concursos/{cpf} com um CPF existente
    cpf = "182.845.084-34"
    response = client.get(f"/concursos/{cpf}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 445
    assert data[0]["codigo"] == "61828450843"

def test_listar_concursos_por_cpf_nao_encontrado(client):
    # Testa o endpoint /concursos/{cpf} com um CPF inexistente
    response = client.get("/concursos/000.000.000-00")
    assert response.status_code == 404
    assert response.json()["detail"] == "Candidato não encontrado"
    
def test_listar_concursos_comportamental(client):
    """Teste comportamental verificando se a resposta contém as chaves esperadas."""
    cpf = "182.845.084-34"
    response = client.get(f"/concursos/{cpf}")
    assert response.status_code == 200
    data = response.json()
    print(data)
    assert isinstance(data, list)
    assert all("codigo" in concurso and "orgao" in concurso and "edital" in concurso and "vagas" in concurso for concurso in data)