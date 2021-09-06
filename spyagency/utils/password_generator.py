import random
import string


def generate_password():
    """This function generate password aleatory"""
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    num = string.digits
    symbols = string.punctuation

    alls = f"{lower}{upper}{num}{symbols}"
    temp = random.sample(alls, 12)
    password = "".join(temp)
    return password
