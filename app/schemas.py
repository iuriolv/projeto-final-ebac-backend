from pydantic import BaseModel

class PokemonCreate(BaseModel):
    name: str
    height: int
    weight: int
    types: list[str]
    front_default: str | None = None
    back_default: str | None = None

class PokemonResponse(PokemonCreate):
    id: int

    class Config:
        from_attributes = True