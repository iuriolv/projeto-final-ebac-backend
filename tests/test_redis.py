import json
from unittest.mock import patch, MagicMock

def test_pokemon_encontrado_no_redis(client):
    pokemon = {
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

    with (
        patch(
            "app.main.redis_client.get",
            return_value=json.dumps(pokemon),
        ) as redis_get,
        patch("app.main.redis_client.set") as redis_set,
        patch("app.main.requests.get") as pokeapi_get,
    ):
        resposta = client.get("/pokeapi/pokemons/25")

    assert resposta.status_code == 200
    assert resposta.json() == pokemon

    redis_get.assert_called_once_with("pokemon:25")
    redis_set.assert_not_called()
    pokeapi_get.assert_not_called()

def test_pokemon_local_preenche_redis(client):
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

    with (
        patch(
            "app.main.redis_client.get",
            return_value=None,
        ) as redis_get,
        patch("app.main.redis_client.set") as redis_set,
        patch("app.main.requests.get") as pokeapi_get,
    ):
        resposta = client.get(f"/pokeapi/pokemons/{pokemon_id}")

    assert resposta.status_code == 200
    assert resposta.json()["name"] == "pikachu"

    redis_get.assert_called_once_with(f"pokemon:{pokemon_id}")
    pokeapi_get.assert_not_called()

    redis_set.assert_called_once()
    argumentos = redis_set.call_args

    assert argumentos.args[0] == f"pokemon:{pokemon_id}"
    assert argumentos.kwargs["ex"] == 300

    dados_cache = json.loads(argumentos.args[1])
    assert dados_cache["name"] == "pikachu"
    assert dados_cache["id"] == pokemon_id

def test_pokemon_nao_encontrado_no_cache_nem_no_banco(client):
    dados_pokemon = {
        "name": "charizard",
        "id": 6,
        "height": 17,
        "weight": 905,
        "types": [
            {"type": {"name": "fire"}},
            {"type": {"name": "flying"}},
        ],
        "sprites": {
            "front_default": "https://example.com/charizard.png",
            "back_default": "https://example.com/charizard-back.png",
        },
    }

    resposta_pokeapi = MagicMock()
    resposta_pokeapi.status_code = 200
    resposta_pokeapi.json.return_value = dados_pokemon

    with (
        patch("app.main.redis_client.get", return_value=None),
        patch("app.main.redis_client.set") as redis_set,
        patch(
            "app.main.requests.get",
            return_value=resposta_pokeapi,
        ) as requisicao,
    ):
        resposta = client.get("/pokeapi/pokemons/6")

    assert resposta.status_code == 200
    dados = resposta.json()
    assert dados["name"] == "charizard"
    assert dados["id"] == 6
    assert dados["types"] == ["fire", "flying"]

    requisicao.assert_called_once_with(
        "https://pokeapi.co/api/v2/pokemon/6",
        timeout=10,
    )

    redis_set.assert_called_once()
    argumentos = redis_set.call_args
    assert argumentos.args[0] == "pokemon:6"
    assert argumentos.kwargs["ex"] == 300

    dados_cache = json.loads(argumentos.args[1])
    assert dados_cache["name"] == "charizard"
    assert dados_cache["id"] == 6

    resposta_local = client.get("/pokemons/6")
    assert resposta_local.status_code == 200
    assert resposta_local.json()["name"] == "charizard"