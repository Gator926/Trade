from decimal import *


def retain_decimals(number: str, precision: str) -> str:
    """
    保留小数位数代码
    :param number:    数字
    :param precision: 保留小数点后几位
    :return:

    int(float(precision)) 是为了解决'6.0'无法直接转为为int类型, 是否为产生其他的问题, 有待观察
    """
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
        number = number[:number.index(".") + int(float(precision)) + 1]
    return number
