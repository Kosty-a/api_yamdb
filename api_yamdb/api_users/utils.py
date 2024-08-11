import random


def generate_confirmation_code():
    '''Функция генерирует confirmation_code.'''

    return str(random.randint(1000, 9999))
