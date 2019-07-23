import pymongo
from sphinx.util import requests

my_client = pymongo.MongoClient("mongodb://localhost:27017/")
my_db = my_client["trade"]
my_col = my_db["trade"]
BASE_URL = 'https://api.binance.com'


def max_min_open_time():
    tmp_max_time = list(my_col.find({}, {'open_time': 1}, sort=[("open_time", -1)], limit=1))
    tmp_min_time = list(my_col.find({}, {'open_time': 1}, sort=[("open_time", 1)], limit=1))
    return tmp_max_time[0]['open_time'], tmp_min_time[0]['open_time']


def check_exist(check_time):
    result = my_col.count({"open_time": check_time})
    if result == 1:
        return True
    elif result == 0:
        return False
    else:
        return "Error"


def get_data(check_time):
    check_time = int(check_time)
    url = BASE_URL + '/api/v1/klines' + '?symbol=BTCUSDT&interval=1m&limit=' + str(1) + '&startTime=' + str(
        check_time) + '&endTime=' + str(check_time)
    # print(url)
    resp = requests.get(url)
    data = resp.json()
    if len(data) > 0:
        print(data)
    print(data)


if __name__ == '__main__':
    max_time, min_time = max_min_open_time()
    current_time = min_time
    while current_time < max_time:
        print(current_time)
        if check_exist(current_time) is False:
            get_data(current_time)
        current_time += 60 * 1000
