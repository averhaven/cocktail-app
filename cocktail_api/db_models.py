from mongoengine import Document, StringField, ListField, EmbeddedDocument, EmbeddedDocumentField


class Ingredient(EmbeddedDocument):
    amount = StringField(required=True)
    unit = StringField(required=True)
    liquor = StringField(required=True)

class Cocktail(Document):
    name = StringField(required=True)
    ingredients = ListField(EmbeddedDocumentField(Ingredient), required=True)
    method = StringField(required=True)
    garnish = StringField(default="N/A")