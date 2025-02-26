import pytest

def test_listar_candidatos_por_concurso(client):
    # Testa o endpoint /candidatos/{codigo_concurso} com um código de concurso existente
    codigo_concurso = "61828450843"
    response = client.get(f"/candidatos/{codigo_concurso}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 7867
    cpf_candidatos = [candidato["cpf"] for candidato in data]
    assert cpf_candidatos[0] == "182.845.084-34"

def test_listar_candidatos_por_concurso_nao_encontrado(client):
    # Testa o endpoint /candidatos/{codigo_concurso} com um código que não existe
    response = client.get("/candidatos/99999999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Concurso não encontrado"
    

def test_listar_candidatos_comportamental(client):
    """Teste comportamental verificando se a resposta contém as chaves esperadas."""
    codigo_concurso = "61828450843"
    response = client.get(f"/candidatos/{codigo_concurso}")
    assert response.status_code == 200
    data = response.json()
    print(data)
    assert isinstance(data, list)
    assert all("cpf" in candidato and "nome" in candidato for candidato in data)