from math import e
from random import randint

import names

from utils.password_generator import generate_password


def get_names(tipo=None, quantity=3):
    listado = []
    for i in range(quantity):
        sexo = randint(1, 2)
        gender = {1: "female", 2: "male"}
        sexo = gender.get(sexo, 2)
        name = names.get_full_name(gender=sexo).lower().replace(" ", "")
        email = f"{name}@kgb.ru"
        password = generate_password()
        add = {
            "email": email,
            "username": email,
            "password": password,
            "is_staff": True,
            "is_active": True,
        }
        if tipo.lower() == "big_boss":
            add["is_superuser"] = True
        listado.append(add)

    return listado
