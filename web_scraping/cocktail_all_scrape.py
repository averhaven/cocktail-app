import re
import json
from bs4 import BeautifulSoup
from dataclasses import dataclass, asdict


@dataclass
class Ingredient:
    amount: str
    unit: str
    liquor: str

    def to_dict(self):
        return asdict(self)

@dataclass
class Cocktail:
    """class for describing a cocktail"""
    name: str
    ingredients: list[Ingredient]
    method: str
    garnish: str

    def to_dict(self):
        ingredients_to_dict = [ingredient.to_dict() for ingredient in self.ingredients]
        return {"name":self.name, "ingredients": ingredients_to_dict, "method": self.method, "garnish": self.garnish}

def main():
    with open("web_scraping/cocktails_all.html") as fp:
        soup = BeautifulSoup(fp, 'html.parser')
    
    with open("web_scraping/cocktails.json","w") as fp:
        cocktail_text = read_cocktail_recipe_raw_texts(soup)
        cocktails = parse_cocktails(cocktail_text)
        cocktails_to_dict = [cocktail.to_dict() for cocktail in cocktails]
        json.dump(cocktails_to_dict,fp)

def read_cocktail_recipe_raw_texts(soup) -> list[tuple[str,str]]:
    cocktail_data = []
    for data in soup.find_all('article',id=re.compile("post-")):
        name = data.h3.a.text
        cocktail_recipe = data.p.text
        cocktail_data.append((name, cocktail_recipe))
    return cocktail_data

def parse_cocktails(cocktail_data: list[tuple[str,str]]) -> list[Cocktail]:
    cocktails = []
    for name, cocktail_recipe in cocktail_data:
        name = " ".join(name.split())
        ingredients = parse_ingredients(cocktail_recipe)
        method, garnish = parse_method_garnish(cocktail_recipe)
        cocktail = Cocktail(name, ingredients, method, garnish)
        cocktails.append(cocktail)
    return cocktails

def parse_ingredients(cocktail_recipe: str) -> list[Ingredient]:
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

def parse_method_garnish(cocktail_recipe: str) -> tuple[str]:
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

if __name__ == "__main__":
    main()