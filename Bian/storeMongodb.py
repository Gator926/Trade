import pymongo
import os
import pandas as pd


def get_file_name(path):
    os_listdir = os.listdir(path)
    return os_listdir


def read_csv(path):
    df = pd.read_csv(path)
    number = df.shape[0]
    dict_country = df.T.to_dict('list')
    print(df.shape[0])
    result = []
    for index in range(number):
        dict = {"open_time": dict_country[index][0], "open": dict_country[index][1], "high": dict_country[index][2],
                "low": dict_country[index][3], "close": dict_country[index][4], "volume": dict_country[index][5],
                "close_time": dict_country[index][6], "quote_volume": dict_country[index][7],
                "trades": dict_country[index][8], "taker_base_volue": dict_country[index][9],
                "taker_quote_volume": dict_country[index][10], "ignore": dict_country[index][11]}
        result.append(dict)
    return result


def count(number):
    number += len(data)
    return number


def save(data):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["trade"]
    mycol = mydb["trade"]
    try:
        mycol.insert_many(data)
    except Exception as E:
        print(E)


def delete():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["trade"]
    mycol = mydb["trade"]
    mycol.delete_many({})


if __name__ == '__main__':
    path = "D:\\工作\\999_Code\\Trade\\Bian\\data"
    number = 0

    file_names = get_file_name(path)
    for key, value in enumerate(file_names):
        full_path = path + "\\" + value
        data = read_csv(full_path)
        # save(data)
        number = count(number)
        print(key, str(994 - key), value, str(number))
