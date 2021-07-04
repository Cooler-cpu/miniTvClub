import random
import string


def token_generator(size=32, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))