from sqlalchemy import Column, Integer, String, JSON
from app.database import Base

class PokemonDB(Base):
    __tablename__ = "pokemons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    height = Column(Integer, nullable=False)
    weight = Column(Integer, nullable=False)
    types = Column(JSON, nullable=False)
    front_default = Column(String, nullable=True)
    back_default = Column(String, nullable=True)