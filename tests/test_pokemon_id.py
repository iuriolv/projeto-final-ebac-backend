from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)


def test_pokemon_id():

    dados_pokemon = {
        "name": "pikachu",
        "id": 25,
        "height": 4,
        "weight": 60,
        "types": [
            {
                "type": {
                    "name": "electric"
                }
            }
        ],
        "sprites": {
            "front_default": "https://example.com/front.png",
            "back_default": "https://example.com/back.png"
        }
    }

    resposta_pokeapi = MagicMock()
    resposta_pokeapi.status_code = 200
    resposta_pokeapi.json.return_value = dados_pokemon

    with patch("app.main.redis_client.get", return_value=None):
        with patch("app.main.redis_client.setex"):
            with patch("app.main.requests.get", return_value=resposta_pokeapi):

                response = client.get("/pokemons/25")

    assert response.status_code == 200

    dados = response.json()

    assert dados["name"] == "pikachu"
    assert dados["id"] == 25
    assert dados["height"] == 4
    assert dados["weight"] == 60
    assert dados["types"] == ["electric"]

    assert "sprites" in dados
    assert "front_default" in dados["sprites"]
    assert "back_default" in dados["sprites"]