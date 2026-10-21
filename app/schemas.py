from pydantic import BaseModel, ConfigDict

class Pokemon(BaseModel):
    name: str
    height: int
    weight: int
    types: list[str]
    front_default: str | None = None
    back_default: str | None = None

class CriarPokemon(BaseModel):
    name: str
    height: int
    weight: int
    types: list[str]
    front_default: str | None = None
    back_default: str | None = None

class PokemonResponse(Pokemon):
    id: int
    model_config = ConfigDict(from_attributes=True)