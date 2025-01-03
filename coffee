from fastapi import FastAPI
from typing import List, Optional

app = FastAPI()


class CoffeeTTK:
    def __init__(self, name: str, ingredients: List[str], preparation: str, serving_size: str, id: int = 0):
        self.name = name
        self.ingredients = ingredients
        self.preparation = preparation
        self.serving_size = serving_size
        self.id = id


class User:
    def __init__(self, name: str, email: str, id: int = 0):
        self.name = name
        self.email = email
        self.id = id
        self.borrowed_drinks = []

coffeettk = []
users = []

base_recipes = [

    CoffeeTTK(
        name = "Espresso"
        ingredients = ["coffe beans 19gr", "water 40ml"]
        preparation = "Working at a 1:2 ratio, serve with a glass of wate."
        serving_size = "40ml"
    ),

    CoffeeTTK(
        name = "Americano"
        ingredients = ["espresso 19gr", "water 150ml"]
        preparation = "Add hot water to espresso, suggest diluting with cold water or adding ice."
        serving_size = "180ml"
    ),

    CoffeeTTK(
        name = "Cuppucino"
        ingredients = ["espresso 19gr", "milk 280ml"]
        preparation = "We add foamed milk to the espresso and draw latte art."
        serving_size = "350ml"
    ), 

    CoffeeTTK(
        name = "Latte"
        ingredients = ["espresso 10gr", "milk 280ml"]
        preparation = "We add foamed milk to the espresso and draw latte art."
        serving_size = "350ml"
    ),

    CoffeeTTK(
        name = "Flat White"
        ingredients = ["espresso 19gr", "milk 180ml"]
        preparation = "Pour thin milk foam into espresso, drawing latte art. "
        serving_size = "250ml"
    ),

        CoffeeTTK(
        name = "Raspberry cocoa with marshmallows"
        ingredients = ["cocoa 30gr", "milk 280ml", "marshmallow 15gr", "dried raspberriies 1gr"]
        preparation = "Add cocoa to a large pitcher, whisk. Decorate the top with marshmallows and dried raspberries."
        serving_size = "350ml"
    ),
       
        CoffeeTTK(
        name = "Chocolate mint cappuccino"
        ingredients = ["espresso 19gr", "mint syrup 10ml", "cocoa 10gr", "milk 280ml"]
        preparation = "Stir 10g cocoa into espresso, pour 280ml foamed milk with 10ml mint syrup on top."
        serving_size = "350ml"
    ),
        
        CoffeeTTK(
        name = "Raf nut condensed milk"
        ingredients = ["espresso 10gr", "condensed milk 30gr", "syrup walnut 10gr", "cream 280gr"]
        preparation = "Stir condensed milk and nut syrup into espresso, add cream 280g and whip."
        serving_size = "350ml"
    ),
        CoffeeTTK(
        name = "Americano with Tiger Vermouth"
        ingredients = ["espresso 19gr", "hot water 230ml", "honey 20gr", "bush jam 10gr", "concentrate Tiger Vermouth 30gr"]
        preparation = "In a cup add Tiger Vermouth concentrate, honey, 3 cones, pour hot water, stir and top with espresso."
        serving_size = "350ml"
    ),

        CoffeeTTK(
        name = "Pumpkin matcha"
        ingredients = ["matcha 2gr", "pumpkin syrup 20ml", "dried pumpkin 3gr", "milk 280gr"]
        preparation = "In 280gm milk, whisk 20ml pumpkin syrup, pour the stirred matcha 2gm in a dot or strip and draw a sprig on top. Decorate the top with a couple of pieces of dried pumpkin."
        serving_size = "350ml"
    )
]
coffeettk.extend(base_recipes)


@app.get("/coffeettk/")
def get_all_coffeettk():
    return coffeettk

@app.get("/coffeettk/{ttkname}")
def get_coffeettk_by_name(ttkname: str):
    for ttk in coffeettk:
        if ttk.name.lower() == ttkname.lower():
            return ttk
    return {"error": "Recipe not found"}

@app.get("/coffeettk/add")
def add_coffeettk(name: str, ingredients: str, preparation: str, serving_size: str):
    ingredients_list = ingredients.split(',')
    new_coffeettk = CoffeeTTK(name, ingredients_list, preparation, serving_size)
    coffeettk.append(new_coffeettk)
    return {"message": "Recipe added successfully", "recipe": new_coffeettk}

@app.get("/coffeettk/update/{ttkname}")
def update_coffeettk(ttkname: str, ingredients: str, preparation: str, serving_size: str):
    for ttk in coffeettk:
        if ttk.name.lower() == ttkname.lower():
            ttk.ingredients = ingredients.split(',')
            ttk.
preparation = preparation
            ttk.serving_size = serving_size
            return {"message": "Recipe updated successfully", "recipe": ttk}
    return {"error": "Recipe not found"}

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
                "serving_size": ttk.serving_size
            }
    return {"error": "Recipe not found"}

@app.get("/coffeettk/filter")
def filter_coffeettk(ingredient: Optional[str] = None):
    if ingredient:
        filtered = [ttk for ttk in coffeettk if ingredient.lower() in [i.lower() for i in ttk.ingredients]]
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
