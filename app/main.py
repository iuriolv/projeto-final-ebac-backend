from fastapi import FastAPI, HTTPException
import requests
from pydantic import BaseModel
import redis

redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

class Sprite(BaseModel):
    front_default: str
    back_default: str

class Pokemon(BaseModel):
    name: str
    id: int
    height: int
    weight: int
    types: list
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
        raise HTTPException(status_code=response.status_code, detail="Erro ao acessar a Poke API")


    dados = response.json()

    return {
        "pagina": page,
        "total": dados["count"],
        "limite": limit,
        "offset": offset,
        "next": dados["next"],
        "previous": dados["previous"]
    }

@app.get("/pokemons/{id}")
async def acessar_pokemon_id(id: int):

    url = f"https://pokeapi.co/api/v2/pokemon/{id}"

    response = requests.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Pokemon não encontrado")

    return response.json()