from sys import exit
from re import match
from cs50 import get_string


def main():
    card = get_string("Number: ")
    # calculates if card is valid
    is_valid = validate(card)

    if is_valid == False:
        exit("INVALID")

    # gets card brand
    brand = get_brand(card)
    print(brand)


def validate(card):
    if len(card) < 13:
        return False

    sum = 0

    # navigates every other digit starting from second-to-last to first
    for i in range(len(card) - 2, -1, -2):
        result = int(card[i]) * 2
        for entry in str(result):
            sum += int(entry)

    # navigates every other digit starting from last digit to first
    for j in range(len(card) - 1, -1, -2):
        sum += int(card[j])

    if sum % 10 == 0:
        return True

    return False


def get_brand(card):
    if match("5+[1-5]", card):
        return "MASTERCARD"

    if match("3+[4|7]", card):
        return "AMEX"

    if card[0] == "4":
        return "VISA"


if __name__ == '__main__':
    main()
