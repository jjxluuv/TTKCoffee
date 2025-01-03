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

@app.get("/coffeerep/")
def get_coffee():
    return coffee_rep.coffee



@app.get("/coffeerep/{drink_id}")
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


@app.post("/coffeerep/add")
def add_coffeettk(name: str, ingredients: str, preparation: str, serving_size: str):
    ingredients_list = ingredients.split(",")
    new_id = len(coffeettk)
    new_coffeettk = CoffeeTTK(new_id, name, ingredients_list, preparation, serving_size)
    coffeettk.append(new_coffeettk)
    return {"message": "Recipe added successfully", "recipe": new_coffeettk}



@app.get("/coffeettk/delete/{ttkname}")
def delete_coffeettk(ttkname: str):
    for ttk in coffeettk:
        if ttk.name.lower() == ttkname.lower():
            coffeettk.remove(ttk)
            return {"message": "Recipe deleted successfully"}
    return {"error": "Recipe not found"}


@app.get("/coffeettk/info/{ttkname}")
def get_info_coffeettk(ttkname: str):
    for ttk in coffeettk:
        if ttk.name.lower() == ttkname.lower():
            return {
                "name": ttk.name,
                "ingredients": ttk.ingredients,
                "preparation": ttk.preparation,
                "serving_size": ttk.serving_size,
            }
    return {"error": "Recipe not found"}


@app.get("/coffeettk/filter")
def filter_coffeettk(ingredient: Optional[str] = None):
    if ingredient:
        filtered = [
            ttk
            for ttk in coffeettk
            if ingredient.lower() in [i.lower() for i in ttk.ingredients]
        ]
        return filtered
    return coffeettk


@app.get("/users/")
def get_all_users():
    return users


@app.get("/users/add")
def add_user(name: str, email: str):
    new_user = User(name, email)
    users.append(new_user)
    return {"message": "Coffee lover added successfully", "user": new_user}


@app.get("/users/{user_id}/borrow/{ttkname}")
def borrow_drink(user_id: int, ttkname: str):
    user = next((u for u in users if u.id == user_id), None)
    if not user:
        return {"error": "Coffee lover not found"}
    drink = next((d for d in coffeettk if d.name.lower() == ttkname.lower()), None)
    if not drink:
        return {"error": "Drink not found"}
    user.borrowed_drinks.append(drink)
    return {"message": f"{user.name} borrowed {drink.name}"}
