#TODO better documentation add docstrings

from typing import Union
from mongoengine import DoesNotExist, connect
from fastapi import HTTPException, APIRouter
import json
from cocktail_api import db_models, schema

router = APIRouter()

#TODO:move it to main
connect("cocktail_db", host="mongodb", port=27017)

@router.get("/cocktails/", response_model=list[schema.Cocktail])
def read_cocktails(liquor: Union[str, None] = None):
    """Retrieve list of cocktails

    Parameters:

    liquor:
        filter cocktails containing only this particular liquor. Supported values:
        gin, whiskey, etc...
    """
    if liquor:
        cocktails = get_cocktails_by_liquor(liquor=liquor)
    else:
        cocktails = get_cocktails()
    return cocktails
#TODO: type hints
def get_cocktails():
    result = db_models.Cocktail.objects.to_json()
    cocktails = [schema.CocktailInDB(**cocktail) for cocktail in json.loads(result)]
    return cocktails

def get_cocktails_by_liquor(liquor: str):
    result = db_models.Cocktail.objects(ingredients__liquor=liquor).to_json()
    cocktails = [schema.CocktailInDB(**cocktail) for cocktail in json.loads(result)]
    return cocktails
#TODO: id instead of name
@router.get("/cocktails/{name}", response_model=schema.Cocktail)
def read_cocktail(name: str):
    cocktail = get_cocktail(name=name)
    return cocktail

#TODO raise 404 exception
def get_cocktail(name: str):
    try:
        result = db_models.Cocktail.objects.get(name=name).to_json()
    except DoesNotExist:
        return None
    cocktail = schema.CocktailInDB(**json.loads(result))
    return cocktail
    
@router.post("/cocktails/", response_model=schema.Cocktail)
def create_cocktail(cocktail: schema.Cocktail):
    db_cocktail = get_cocktail(name=cocktail.name)
    if db_cocktail:
        raise HTTPException(status_code=400, detail="Cocktail is already registered")
    create_cocktail_db(cocktail=cocktail)
    return cocktail

def create_cocktail_db(cocktail: schema.Cocktail):
    db_ingredients = [db_models.Ingredient(amount=ingredient.amount,unit=ingredient.unit,liquor=ingredient.liquor) for ingredient in cocktail.ingredients]
    db_cocktail = db_models.Cocktail(name=cocktail.name,ingredients=db_ingredients,method=cocktail.method,garnish=cocktail.garnish)
    db_cocktail.save()

