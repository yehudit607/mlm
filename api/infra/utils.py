import random


def generate_random(
    size=100,
    allowed_chars="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
) -> str:
    return "".join(random.choice(allowed_chars) for i in range(size))


