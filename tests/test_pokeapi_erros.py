from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_listagem_pokeapi_com_erro():
    resposta_falsa = MagicMock()
    resposta_falsa.status_code = 500

    with (
        patch("app.main.redis_client.get", return_value=None),
        patch("app.main.redis_client.set"),
        patch("app.main.requests.get", return_value=resposta_falsa),
    ):
        resposta = client.get("/pokeapi/pokemons")

    assert resposta.status_code == 502
    assert resposta.json()["detail"] == "Erro ao acessar a PokéAPI"

def test_buscar_pokemon_no_cache(client):
    dados = {
        "name": "pikachu",
        "height": 4,
        "weight": 60,
        "types": ["electric"],
        "front_default": "https://example.com/front.png",
        "back_default": "https://example.com/back.png",
    }

    cadastro = client.post("/pokemons", json=dados)
    assert cadastro.status_code == 200

    pokemon_id = cadastro.json()["id"]

    with patch("app.main.requests.get") as requisicao:
        resposta = client.get(f"/pokeapi/pokemons/{pokemon_id}")

    assert resposta.status_code == 200
    assert resposta.json()["name"] == "pikachu"
    requisicao.assert_not_called()