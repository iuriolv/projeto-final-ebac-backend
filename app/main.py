from fastapi import FastAPI, HTTPException
import requests
from pydantic import BaseModel
import json
import redis
import os

redis_client = redis.Redis(host=os.getenv("REDIS_HOST", "localhost"), port=int(os.getenv("REDIS_PORT", 6379)), decode_responses=True)

class Sprite(BaseModel):
    front_default: str | None
    back_default: str | None

class Pokemon(BaseModel):
    name: str
    id: int
    height: int
    weight: int
    types: list[str]
    sprites: Sprite

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/pokemons")
async def acessar_api(page: int = 1, limit: int = 20, ):

    offset = (page - 1) * limit

    url = f"https://pokeapi.co/api/v2/pokemon?limit={limit}&offset={offset}"

    response = requests.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Erro ao acessar a Poke API")


    dados = response.json()

    return {
        "pagina": page,
        "total": dados["count"],
        "limite": limit,
        "offset": offset,
        "next": dados["next"],
        "previous": dados["previous"],
        "Pokemons": dados["results"]
    }

@app.get("/pokemons/{id}", response_model=Pokemon)
async def acessar_pokemon_id(id: int):

    cache_key = f"Pokemon:{id}"

    cached_data = redis_client.get(cache_key)

    if cached_data:
        return json.loads(cached_data)

    url = f"https://pokeapi.co/api/v2/pokemon/{id}"

    response = requests.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Pokemon não encontrado")

    dados = response.json()

    resultado = {
        "name": dados["name"],
        "id": dados["id"],
        "height": dados["height"],
        "weight": dados["weight"],
        "types": [tipo["type"]["name"] for tipo in dados["types"]],
        "sprites": {
            "front_default": dados["sprites"]["front_default"],
            "back_default": dados["sprites"]["back_default"]
        }
    }

    redis_client.setex(cache_key, 300, json.dumps(resultado))

    return resultado