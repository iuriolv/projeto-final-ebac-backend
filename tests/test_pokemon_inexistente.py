from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)


def test_pokemon_nao_encontrado():

    resposta_pokeapi = MagicMock()
    resposta_pokeapi.status_code = 404

    with patch("app.main.redis_client.get", return_value=None):
        with patch("app.main.requests.get", return_value=resposta_pokeapi):

            response = client.get("/pokemons/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Pokemon não encontrado"