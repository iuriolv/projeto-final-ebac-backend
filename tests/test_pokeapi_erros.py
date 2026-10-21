from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_listagem_pokeapi_com_erro():
    resposta_falsa = MagicMock()
    resposta_falsa.status_code = 500

    with patch("app.main.requests.get", return_value=resposta_falsa):
        resposta = client.get("/pokeapi/pokemons")

    assert resposta.status_code == 404
    assert resposta.json()["detail"] == "Erro ao acessar a Poke API"


def test_buscar_pokemon_no_cache():
    dados_cache = {
        "name": "pikachu",
        "id": 25,
        "height": 4,
        "weight": 60,
        "types": ["electric"],
        "sprites": {
            "front_default": "https://example.com/front.png",
            "back_default": "https://example.com/back.png",
        },
    }

    with patch("app.main.redis_client.get", return_value=__import__("json").dumps(dados_cache)):
        with patch("app.main.requests.get") as requisicao:
            resposta = client.get("/pokeapi/pokemons/25")

    assert resposta.status_code == 200
    assert resposta.json()["name"] == "pikachu"
    requisicao.assert_not_called()