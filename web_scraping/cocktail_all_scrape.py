import re
import json
from bs4 import BeautifulSoup
from dataclasses import dataclass

with open("web_scraping/cocktails_all.html") as fp:
    soup = BeautifulSoup(fp, 'html.parser')

@dataclass
class Ingredient:
    amount: str
    unit: str
    liquor: str

@dataclass
class Cocktail:
    """class for describing a cocktail"""
    name: str
    ingredients: list[Ingredient]
    method: str
    garnish: str

def get_data(soup) -> list[tuple]:
    cocktail_data = []
    for data in soup.find_all('article',class_=re.compile("post-")):
        name = data.h3.a.text
        cocktail_recipe = data.p.text
        cocktail_data.append((name, cocktail_recipe))
    return cocktail_data

def get_cocktails(cocktail_data: list[tuple]) -> list[Cocktail]:
    cocktails = []
    for name, cocktail_recipe in cocktail_data:
        name = " ".join(name.split())
        ingredients = get_ingredients(cocktail_recipe)
        method, garnish = get_method_garnish(cocktail_recipe)
        cocktail = Cocktail(name, ingredients, method, garnish)
        cocktails.append(cocktail)
    return cocktails

def get_ingredients(cocktail_recipe: str) -> list[Ingredient]:
    ingredients = []
    ingredients_i = re.search("INGREDIENTS", cocktail_recipe).span()
    method_i = re.search("METHOD", cocktail_recipe).span()
    ingredients_t = cocktail_recipe[ingredients_i[1]:method_i[0]].replace("\n"," ")
    for m in re.finditer(r"(\d+|\d+\.\d+)\s(\w+)\s(\D+)", ingredients_t):
        amount, unit = m.group(1,2)
        liquor = " ".join(m.group(3).split())
        ingredient = Ingredient(amount, unit, liquor)
        ingredients.append(ingredient)
    return ingredients

def get_method_garnish(cocktail_recipe: str) -> tuple[str]:
    method = ""
    garnish = ""
    method_i = re.search("METHOD", cocktail_recipe).span()
    garnish_m = re.search("GARNISH", cocktail_recipe)
    history_m = re.search("HISTORY", cocktail_recipe)
    if garnish_m:
        method = " ".join(cocktail_recipe[method_i[1]:garnish_m.span()[0]].split())
        if history_m:
            garnish = " ".join(cocktail_recipe[garnish_m.span()[1]:history_m.span()[0]].split())
        else:
            garnish = " ".join(cocktail_recipe[garnish_m.span()[1]:].split())
    else:
        method = " ".join(cocktail_recipe[method_i[1]:].split())
        garnish = "N/A"
    return (method, garnish)

cocktails = get_cocktails(get_data(soup))
print(len(cocktails))

#with open("web_scraping/cocktails.json","w") as fp:
#    json.dump(get_cocktails(get_data(soup)),fp, default=lambda o: o.__dict__)