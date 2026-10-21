def test_crud_pokemon(client):
    dados = {
        "name": "pikachu",
        "height": 4,
        "weight": 60,
        "types": ["electric"],
        "front_default": None,
        "back_default": None,
    }

    resposta = client.post("/pokemons", json=dados)
    print(resposta.json())
    assert resposta.status_code == 200

    pokemon = resposta.json()
    pokemon_id = pokemon["id"]
    assert pokemon["name"] == "pikachu"

    resposta = client.get("/pokemons")
    assert resposta.status_code == 200
    assert len(resposta.json()["Pokemons"]) == 1

    resposta = client.get(f"/pokemons/{pokemon_id}")
    assert resposta.status_code == 200
    assert resposta.json()["name"] == "pikachu"

    dados_atualizados = {
        **dados,
        "name": "pikachu-atualizado",
    }

    resposta = client.put(
        f"/pokemons/{pokemon_id}", json=dados_atualizados)
    print(resposta.json())
    assert resposta.status_code == 200
    assert resposta.json()["name"] == "pikachu-atualizado"

    resposta = client.delete(f"/pokemons/{pokemon_id}")
    print(resposta.json())
    assert resposta.status_code == 200

    resposta = client.get(f"/pokemons/{pokemon_id}")
    assert resposta.status_code == 404

def test_criar_pokemon_duplicado(client):
    dados = {
        "name": "bulbasaur",
        "height": 7,
        "weight": 69,
        "types": ["grass", "poison"],
        "front_default": None,
        "back_default": None,
    }

    primeira_resposta = client.post("/pokemons", json=dados)
    segunda_resposta = client.post("/pokemons", json=dados)

    assert primeira_resposta.status_code == 200
    assert segunda_resposta.status_code == 400

def test_buscar_pokemon_inexistente(client):
    resposta = client.get("/pokemons/99999")

    assert resposta.status_code == 404

def test_atualizar_pokemon_inexistente(client):
    dados = {
        "name": "pokemon-inexistente",
        "height": 5,
        "weight": 50,
        "types": ["normal"],
        "front_default": None,
        "back_default": None,
    }

    resposta = client.put("/pokemons/99999", json=dados)

    assert resposta.status_code == 404

def test_excluir_pokemon_inexistente(client):
    resposta = client.delete("/pokemons/9999")

    assert resposta.status_code == 404