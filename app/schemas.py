from pydantic import BaseModel

class Pokemon(BaseModel):
    name: str
    height: int
    weight: int
    types: list[str]
    front_default: str | None = None
    back_default: str | None = None

class PokemonResponse(Pokemon):
    id: int

    class Config:
        from_attributes = True