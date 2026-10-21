from unittest.mock import patch, MagicMock

def test_pokemon_id(client):
    dados_pokemon = {
        "name": "pikachu",
        "id": 25,
        "height": 4,
        "weight": 60,
        "types": [
            {"type": {"name": "electric"}}
        ],
        "sprites": {
            "front_default": "https://example.com/front.png",
            "back_default": "https://example.com/back.png",
        },
    }

    resposta_pokeapi = MagicMock()
    resposta_pokeapi.status_code = 200
    resposta_pokeapi.json.return_value = dados_pokemon

    with (
        patch("app.main.redis_client.get", return_value=None),
        patch("app.main.redis_client.set"),
        patch(
            "app.main.requests.get",
            return_value=resposta_pokeapi,
        ) as requisicao,
    ):
        resposta = client.get("/pokeapi/pokemons/25")

    assert resposta.status_code == 200

    dados = resposta.json()

    assert dados["name"] == "pikachu"
    assert dados["id"] == 25
    assert dados["height"] == 4
    assert dados["weight"] == 60
    assert dados["types"] == ["electric"]

    assert dados["sprites"]["front_default"] == "https://example.com/front.png"
    assert dados["sprites"]["back_default"] == "https://example.com/back.png"

    requisicao.assert_called_once()

    resposta_local = client.get("/pokemons/25")

    assert resposta_local.status_code == 200
    assert resposta_local.json()["name"] == "pikachu"