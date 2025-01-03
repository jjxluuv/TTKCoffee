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
    def __init__(self, id, name, email, bought_drinks, blacklist):
        self.id = id
        self.name = name
        self.email = email
        self.bought_drinks = bought_drinks
        self.blacklist = blacklist


class UserRep:
    def __init__(self):
        self.user = []
        self.user.append(
            User(0, "Ваня", "ваня@mail.ru", None, None)
        )
        self.user.append(
            User(1, "Лох", "Лох@mail.ru", None, None)
        )
        self.user.append(
            User(2, "штрих", "штрих@mail.ru", None, None)
        )
        self.user.append(
            User(3, "штемпяра", "штемпяра@mail.ru", None, None)
        )


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

user_rep = UserRep()
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

@app.get("/users/", tags=["Клиенты"], summary=["Посмотреть всю базу клиентов"], description="Для кого я это вообще пишу...")
def get_users():
    return user_rep.user

@app.post("/users/", tags=["Клиенты"], summary=["Добавить нового слоняру"], description="Добро пожаловать в бойцовский клуб")
def add_user(name: str, email: str, bought_drinks: Optional[str] = None, blacklist: Optional[str] = None):
    if user_rep.user:
        new_id = max([user.id for user in user_rep.user]) + 1
    else:
        new_id = 0
    new_user = User(new_id, name, email, bought_drinks, blacklist)
    user_rep.user.append(new_user)
    return {"message": "New customer added successfully", "users": vars(new_user)}

@app.post("/users/{user_id}/buy/{drink_id}", tags=["Клиенты"], summary="Добавить покупку клиентом", description="Тут был Ян!")
def add_buying(user_id: int, drink_id: int):
    user = next((user for user in user_rep.user if user.id == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    coffee = next((coffee for coffee in coffee_rep.coffee if coffee.id == drink_id), None)
    if coffee is None:
        raise HTTPException(status_code=404, detail="Drink not found")
    
    if user.bought_drinks is None:
        user.bought_drinks = []
    
    user.bought_drinks.append(coffee.coffe_name)
    return {
        "message": f"User {user.name} bought {coffee.coffe_name}",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "bought_drinks": user.bought_drinks,
        },
    }

@app.post("/users/{user_id}/rage/{drink_id}", tags=["Клиенты"], summary="Пользователь отказывается от напитка", description="Добавляет пользователя в черный список (blacklist).")
def add_returning(user_id: int, drink_id: int):
    user = next((user for user in user_rep.user if user.id == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.bought_drinks is None or drink_id >= len(coffee_rep.coffee) or coffee_rep.coffee[drink_id].coffe_name not in user.bought_drinks:
        raise HTTPException(status_code=400, detail="Drink not in user's purchases")
    
    user.blacklist = True

    return {
        "message": f"User {user.name} has been added to the blacklist for rejecting {coffee_rep.coffee[drink_id].coffe_name}.",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "bought_drinks": user.bought_drinks,
            "blacklist": user.blacklist,
        },
    }

@app.get("/users/{user_id}", tags=["Клиенты"], summary="Вытащить конкретного пользователя", description="Передаю привет маме семена! Я ее рот ебал!")
def get_user_by_id(user_id: int):
    user = next((user for user in user_rep.user if user.id == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "bought_drinks": user.bought_drinks,
        "blacklist": user.blacklist,
    }
