from fastapi import FastAPI, HTTPException
from typing import List, Optional

app = FastAPI()


class CoffeeTTK:
    def __init__(self, id, name, ingredients, preparation, serving_size):
        self.id = id
        self.coffe_name = name
        self.ingredients = ingredients
        self.preparation = preparation
        self.serving_size = serving_size


class User:
    def __init__(self, name: str, email: str, id: int = 0):
        self.name = name
        self.email = email
        self.id = id
        self.borrowed_drinks = []


coffeettk = []
users = []


class CoffeeRep:
    def __init__(self):
        self.coffee = []
        self.coffee.append(
            CoffeeTTK(
                0,
                "Espresso",
                ["coffe beans 19gr", "water 40ml"],
                "Working at a 1:2 ratio, serve with a glass of water.",
                "40ml",
            )
        )
        self.coffee.append(
            CoffeeTTK(
                1,
                "Americano",
                ["espresso 19gr", "water 150ml"],
                "Add hot water to espresso, suggest diluting with cold water or adding ice.",
                "180ml",
            )
        )
        self.coffee.append(
            CoffeeTTK(
                2,
                "Cappucino",
                ["espresso 19gr", "milk 280ml"],
                "We add foamed milk to the espresso and draw latte art.",
                "350ml",
            )
        )
        self.coffee.append(
            CoffeeTTK(
                3,
                "Latte",
                ["espresso 10gr", "milk 280ml"],
                "We add foamed milk to the espresso and draw latte art.",
                "350ml",
            )
        )
        self.coffee.append(
            CoffeeTTK(
                4,
                "Flat White",
                ["espresso 19gr", "milk 180ml"],
                "Pour thin milk foam into espresso, drawing latte art.",
                "250ml",
            )
        )
        self.coffee.append(
            CoffeeTTK(
                5,
                "Raspberry cocoa with marshmallows",
                [
                    "cocoa 30gr",
                    "milk 280ml",
                    "marshmallow 15gr",
                    "dried raspberriies 1gr",
                ],
                "Add cocoa to a large pitcher, whisk. Decorate the top with marshmallows and dried raspberries.",
                "350ml",
            )
        )
        self.coffee.append(
            CoffeeTTK(
                6,
                "Chocolate mint cappuccino",
                ["espresso 19gr", "mint syrup 10ml", "cocoa 10gr", "milk 280ml"],
                "Stir 10g cocoa into espresso, pour 280ml foamed milk with 10ml mint syrup on top.",
                "350ml",
            )
        )
        self.coffee.append(
            CoffeeTTK(
                7,
                "Raf nut condensed milk",
                [
                    "espresso 10gr",
                    "condensed milk 30gr",
                    "syrup walnut 10gr",
                    "cream 280gr",
                ],
                "Stir condensed milk and nut syrup into espresso, add cream 280g and whip.",
                "350ml",
            )
        )
        self.coffee.append(
            CoffeeTTK(
                8,
                "Americano with Tiger Vermouth",
                [
                    "espresso 19gr",
                    "hot water 230ml",
                    "honey 20gr",
                    "bush jam 10gr",
                    "concentrate Tiger Vermouth 30gr",
                ],
                "In a cup add Tiger Vermouth concentrate, honey, 3 cones, pour hot water, stir and top with espresso.",
                "350ml",
            )
        )
        self.coffee.append(
            CoffeeTTK(
                9,
                "Pumpkin matcha",
                ["matcha 2gr", "pumpkin syrup 20ml", "dried pumpkin 3gr", "milk 280gr"],
                "In 280gm milk, whisk 20ml pumpkin syrup, pour the stirred matcha 2gm in a dot or strip and draw a sprig on top. Decorate the top with a couple of pieces of dried pumpkin.",
                "350ml",
            )
        )

coffee_rep = CoffeeRep()

@app.get("/coffeerep/", tags=["Кофе"], summary="Всё кофе", description="Возвращает весь кофе в api")
def get_coffee():
    return coffee_rep.coffee



@app.get("/coffeerep/{drink_id}", tags=["Кофе"], summary="Вытащить кофе по id", description="Позволяет вытащить конкретной кофе по введеному id")
def get_coffee_by_id(drink_id: int):
    for coffee in coffee_rep.coffee:
        if coffee.id == drink_id:
            return {
                "id": coffee.id,
                "coffee_name": coffee.coffe_name,
                "ingredients": coffee.ingredients,
                "preparation": coffee.preparation,
                "serving_size": coffee.serving_size,
            }
    raise HTTPException(status_code=404, detail="Drink not found")


@app.post("/coffeerep/", tags=["Кофе"], summary="Добавить кофе", description="Позволяет добавить в api кастомный кофе, почти автоматизация)")
def add_coffeettk(name: str, ingredients: str, preparation: str, serving_size: str):
    ingredients_list = ingredients.split(", ")
    if coffee_rep.coffee:
        new_id = max([coffee.id for coffee in coffee_rep.coffee]) + 1
    else:
        new_id = 0
    new_coffee = CoffeeTTK(new_id, name, ingredients_list, preparation, serving_size)
    coffee_rep.coffee.append(new_coffee)
    return {"message": "Recipe added successfully", "recipe": vars(new_coffee)}

@app.put("/coffeerep/{drink_id}", tags=["Кофе"], summary="Изменить имеющийся кофе", description="Позволяет изменить свойства существующего кофе в API")
def change_coffeettk(
    drink_id: int,
    name: Optional[str] = None,
    ingredients: Optional[str] = None,
    preparation: Optional[str] = None,
    serving_size: Optional[str] = None
):
    for coffee in coffee_rep.coffee:
        if coffee.id == drink_id:
            if name is not None:
                coffee.coffe_name = name
            if ingredients is not None:
                coffee.ingredients = ingredients.split(", ")
            if preparation is not None:
                coffee.preparation = preparation
            if serving_size is not None:
                coffee.serving_size = serving_size
            return {"message": "Recipe updated successfully", "recipe": vars(coffee)}
    raise HTTPException(status_code=404, detail="Drink not found")

@app.delete("/cofeerep/{drink_id}", tags=["Кофе"], summary="Удалить кофе из api", description="Тут точно нужно описание?")
def delete_coffeettk(
    drink_id: int
):
    for coffee in coffee_rep.coffee:
        if coffee.id == drink_id:
            coffee.coffe_name = None
            coffee.ingredients = None
            coffee.preparation = None
            coffee.serving_size = None
            return {"message": "Recipe deleted successfully", "recipe": vars(coffee)}
    raise HTTPException(status_code=404, detail="Drink not found")