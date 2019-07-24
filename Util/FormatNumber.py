def retain_decimals(number, precision):
    number = str(number)
    number = number[:number.index(".") + int(precision) + 1]
    return number
