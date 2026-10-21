from fastapi import FastAPI, HTTPException, Depends
import requests
from pydantic import BaseModel
import json
import redis
import os
from sqlalchemy.orm import Session
from app.database import Base, engine, get_db
from app.models import PokemonDB
from app.schemas import Pokemon, PokemonResponse, CriarPokemon

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

Base.metadata.create_all(bind=engine)

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/pokeapi/pokemons")
async def acessar_api(page: int = 1, limit: int = 20):

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

@app.get("/pokeapi/pokemons/{id}", response_model=Pokemon)
def acessar_pokemon_id(id: int, db: Session = Depends(get_db)):
    
    chave_cache = f"pokemon:{id}"

    try:
        pokemon_cache = redis_client.get(chave_cache)

        if pokemon_cache:
            return json.loads(pokemon_cache)

    except (redis.RedisError, json.JSONDecodeError):
        pass

    pokemon_local = (db.query(PokemonDB).filter(PokemonDB.id == id).first())

    if pokemon_local:
        resultado = {
            "name": pokemon_local.name,
            "id": pokemon_local.id,
            "height": pokemon_local.height,
            "weight": pokemon_local.weight,
            "types": pokemon_local.types,
            "sprites": {
                "front_default": pokemon_local.front_default,
                "back_default": pokemon_local.back_default,
            },
        }

        try:
            redis_client.set(chave_cache, json.dumps(resultado), ex=300)
        except redis.RedisError:
            pass

        return resultado

    url = f"https://pokeapi.co/api/v2/pokemon/{id}"

    try:
        response = requests.get(url, timeout=10)
    except requests.RequestException:
        raise HTTPException(status_code=503, detail="Não foi possível acessar a PokéAPI")

    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Pokemon não encontrado")

    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="Erro ao consultar a PokéAPI")

    dados = response.json()

    resultado = {
        "name": dados["name"],
        "id": dados["id"],
        "height": dados["height"],
        "weight": dados["weight"],
        "types": [
            tipo["type"]["name"]
            for tipo in dados["types"]
        ],
        "sprites": {
            "front_default": dados["sprites"]["front_default"],
            "back_default": dados["sprites"]["back_default"],
        },
    }

    novo_pokemon = PokemonDB(
        id=resultado["id"],
        name=resultado["name"],
        height=resultado["height"],
        weight=resultado["weight"],
        types=resultado["types"],
        front_default=resultado["sprites"]["front_default"],
        back_default=resultado["sprites"]["back_default"],
    )

    db.add(novo_pokemon)
    db.commit()
    db.refresh(novo_pokemon)

    try:
        redis_client.set(chave_cache, json.dumps(resultado), ex=300)
    except redis.RedisError:
        pass

    return resultado

@app.post("/pokemons", response_model=PokemonResponse)
def criar_pokemon(pokemon: CriarPokemon, db: Session = Depends(get_db)):

    if db.query(PokemonDB).filter(PokemonDB.name == pokemon.name).first():
        raise HTTPException(status_code=400, detail="Pokemon já existe no banco de dados")
    
    novo_pokemon = PokemonDB(**pokemon.model_dump())
    db.add(novo_pokemon)
    db.commit()
    db.refresh(novo_pokemon)

    return novo_pokemon


@app.get("/pokemons")
def listar_pokemons(page: int = 1, limit: int = 20, db: Session = Depends(get_db)):
    
    offset = (page - 1) * limit

    query = db.query(PokemonDB)
    total = query.count()

    pokemons = (query.offset(offset).limit(limit).all())

    return {
        "pagina": page,
        "total": total,
        "limite": limit,
        "offset": offset,
        "next": f"/pokemons?page={page + 1}&limit={limit}"
        if offset + limit < total else None,
        "previous": f"/pokemons?page={page - 1}&limit={limit}"
        if page > 1 else None,
        "Pokemons": [
            PokemonResponse.model_validate(pokemon).model_dump()
            for pokemon in pokemons
        ],
    }

@app.get("/pokemons/{id}", response_model=PokemonResponse)
def buscar_pokemon(id: int, db: Session = Depends(get_db)):
    pokemon = db.query(PokemonDB).filter(PokemonDB.id == id).first()

    if pokemon is None:
        raise HTTPException(status_code=404, detail="Pokemon não encontrado no banco de dados")

    return pokemon

@app.put("/pokemons/{id}", response_model=PokemonResponse)
def atualizar_pokemon(id: int, dados: CriarPokemon, db: Session = Depends(get_db)):
    pokemon = db.query(PokemonDB).filter(PokemonDB.id == id).first()

    if pokemon is None:
        raise HTTPException(status_code=404, detail="Pokemon não encontrado no banco de dados")

    for campo, valor in dados.model_dump().items():
        setattr(pokemon, campo, valor)

    db.commit()
    db.refresh(pokemon)

    try:
        redis_client.delete(f"pokemon:{id}")
    except redis.RedisError:
        pass

    return pokemon

@app.delete("/pokemons/{id}")
def excluir_pokemon(id: int, db: Session = Depends(get_db)):
    pokemon = db.query(PokemonDB).filter(PokemonDB.id == id).first()

    if pokemon is None:
        raise HTTPException(status_code=404, detail="Pokemon não encontrado no banco de dados")

    db.delete(pokemon)
    db.commit()

    return {"mensagem": "Pokemon excluído com sucesso"}