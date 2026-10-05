from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_pokemons():
    response = client.get("/pokemons?page=1&limit=20")

    assert response.status_code == 200

    dados = response.json()

    assert dados["pagina"] == 1
    assert dados["limite"] == 20
    assert dados["offset"] == 0
    assert "total" in dados
    assert "next" in dados
    assert "previous" in dados
    assert "Pokemons" in dados