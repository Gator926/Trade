from decimal import *


def retain_decimals(number: str, precision: str) -> str:
    number = str(number)
    if "e" in number:
        value = number[:number.index("e")]
        base = number[number.index("e")+2:]
        if "-" in number:
            number = Decimal(value[:number.index(".") + int(precision) + 1]) / (10 ** Decimal(base))
        elif "+" in number:
            number = Decimal(value[:number.index(".") + int(precision) + 1]) * (10 ** Decimal(base))
        return retain_decimals(str(number), precision)
    else:
        number = number[:number.index(".") + int(precision) + 1]
    return number


print(123)
