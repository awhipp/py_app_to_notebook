import random

def generate_random_number():
    return random.randint(0, 1000)

def generate_random_string(length:int):
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=length))
