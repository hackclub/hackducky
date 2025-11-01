import random

LOWERCASE_LETTERS = "abcdefghijklmnopqrstuvwxyz"
UPPERCASE_LETTERS =	"ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
NUMBERS =	"0123456789"
SPECIALS =	"!@#$%^&*()"
CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"

def random_lower():
    return random.choice(LOWERCASE_LETTERS)

def random_upper():
    return random.choice(UPPERCASE_LETTERS)

def random_letter():
    return random.choice(LETTERS)

def random_number():
    return random.choice(NUMBERS)


def random_special():
    return random.choice(SPECIALS)


def random_char():
    return random.choice(CHARS)

RANDOM_KEYSTROKES = {
        "RANDOM_LOWERCASE_LETTER": random_lower,
        "RANDOM_UPPERCASE_LETTER": random_upper,
        "RANDOM_LETTER": random_letter,
        "RANDOM_NUMBER": random_number,
        "RANDOM_SPECIAL": random_special,
        "RANDOM_CHAR": random_char,
}