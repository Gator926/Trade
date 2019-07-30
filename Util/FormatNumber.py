# TODO :'2.650657248570439e-05'在类似于这种科学计数法的情况下，保留小数点会出错
def retain_decimals(number: str, precision: str) -> str:
    number = str(number)
    number = number[:number.index(".") + int(precision) + 1]
    return number
