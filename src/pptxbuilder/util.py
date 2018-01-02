import string
import random


def random_alphanum(length):
    chars = string.ascii_letters + string.digits + '-_'

    return ''.join((random.choice(chars)) for x in range(length))
