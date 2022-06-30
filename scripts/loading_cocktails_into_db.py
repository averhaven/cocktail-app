from cocktail_api.db_models import Ingredient, Cocktail
from mongoengine import connect
import json

connect("cocktail_db", host="127.0.0.1", port=27017)

def main():
    with open("./web_scraping/cocktails.json", encoding='utf8') as fp:
        cocktails = json.load(fp)
        for cocktail in cocktails:
            create_cocktail_db(cocktail)


def create_cocktail_db(cocktail):
    db_ingredients = [Ingredient(amount=ingredient["amount"], unit=ingredient["unit"],
                                 liquor=ingredient["liquor"]) for ingredient in cocktail["ingredients"]]
    db_cocktail = Cocktail(name=cocktail["name"], ingredients=db_ingredients,
                           method=cocktail["method"], garnish=cocktail["garnish"])
    db_cocktail.save()


if __name__ == "__main__":
    main()
