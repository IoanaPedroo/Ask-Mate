import random
import string
uppers = string.ascii_uppercase
lowers = string.ascii_lowercase
digits = string.digits


def generate_id(number_of_small_letters=4,
                number_of_capital_letters=2,
                number_of_digits=2,
                number_of_special_chars=2,
                allowed_special_chars=r"_+-!"):
    x = [random.choice(uppers) for _ in range(number_of_capital_letters)]
    x += [random.choice(lowers) for _ in range(number_of_small_letters)]
    x += [random.choice(allowed_special_chars) for _ in range(number_of_special_chars)]
    x += [random.choice(digits) for _ in range(number_of_digits)]
    random.shuffle(x)
    return ''.join(x)

