from pydantic import BaseModel

class Ingredient(BaseModel):
    amount: str
    unit: str
    liquor: str

class Cocktail(BaseModel):
    name: str
    ingredients: list[Ingredient]
    method: str
    garnish: str = "N/A"

class CocktailInDB(Cocktail):
    _id: dict