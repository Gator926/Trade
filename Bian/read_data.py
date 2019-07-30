import pymongo


def get_data():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["trade"]
    mycol = mydb["trade"]
    results = mycol.find({}, {'open_time': 1, "open": 1}).sort('open_time', pymongo.ASCENDING)
    return_data = []
    for each in results:
        return_data.append(each)
    return return_data


def draw_picture(data, money_list):
    import matplotlib.pyplot as plt

    open_time = []
    price = []
    double_price = []
    for each in data:
        open_time.append(each['open_time'])
        price.append(each['open'])
    # plt.figure(figsize=(100, 20))
    # plt.plot(open_time, price, label='Price')
    # plt.plot(open_time, money_list, label='Money')
    # plt.savefig('price.png')
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax1.plot(open_time, price, 'g-')
    ax2.plot(open_time, money, 'b--')
    plt.savefig('price.png')


def keep_balance_percentage(data):
    for index in range(101, 150, 1):
        threshold = index / 100
        dollar = 200
        bitcoin = 0
        cost = 0
        money_list = [50]
        for key, value in enumerate(data):
            if key == 0:
                rest = dollar - bitcoin * value['open']
                dollar -= rest / 2
                bitcoin += rest / 2 / value['open'] * 0.998
                cost += rest / 2 * 0.002
                # print(f"{value['open_time']}买入{25 / value['open'] * 0.998}个比特币,当前美元: {dollar}, "
                #       f"比特币: {bitcoin}, 合计: {dollar + bitcoin * value['open']}, 手续费{cost}")
            # 比特币高于阈值
            if dollar * threshold < bitcoin * value['open']:
                rest = bitcoin * value['open'] - dollar
                dollar += rest / 2 * 0.998
                bitcoin -= rest / 2 / value['open']
                cost += rest / 2 * 0.002
                # print(f"{value['open_time']}卖出{rest / 2 / value['open']}个比特币,当前美元: {dollar}, "
                #       f"比特币: {bitcoin}, 合计: {dollar + bitcoin * value['open']}, 手续费{cost}")
            elif bitcoin * value['open'] * threshold < dollar:
                rest = dollar - bitcoin * value['open']
                dollar -= rest / 2
                bitcoin += rest / 2 / value['open'] * 0.998
                cost += rest / 2 * 0.002
                # print(f"{value['open_time']}买入{rest / 2 / value['open'] * 0.998}个比特币,当前美元: {dollar}, "
                #       f"比特币: {bitcoin}, 合计: {dollar + bitcoin * value['open']}, 手续费{cost}")
            if money_list[-1] != int(dollar + bitcoin * data[key - 1]['open']):
                money_list.append(int(dollar + bitcoin * data[key - 1]['open']))
        # print(dollar, bitcoin)
        # print(money_list)
        print(f"阈值: {threshold}     合计: {dollar + bitcoin * data[key - 1]['open']}")


def keep_balance_number(data):
    for threshold in range(1, 100, 1):
        dollar = 50
        bitcoin = 0
        money_list = []
        for key, value in enumerate(data):
            if key == 0:
                bitcoin = 25 / value['open'] * 0.998
                dollar -= 25
            # 比特币高于阈值
            if dollar + threshold < bitcoin * value['open']:
                rest = bitcoin * value['open'] - dollar
                dollar += rest / 2 * 0.998
                bitcoin -= rest / 2 / value['open']
                # print(f"{value['open_time']}卖出{rest / 2 / value['open']}个比特币,当前美元: {dollar}, 比特币: {bitcoin}")
            elif bitcoin * value['open'] + threshold < dollar:
                rest = dollar - bitcoin * value['open']
                dollar -= rest / 2
                bitcoin += rest / 2 / value['open'] * 0.998
                # print(f"{value['open_time']}买入{rest / 2 / value['open'] * 0.998}个比特币,当前美元: {dollar}, 比特币: {bitcoin}")
            if money_list[-1] != int(dollar + bitcoin * data[key - 1]['open']):
                money_list.append(int(dollar + bitcoin * data[key - 1]['open']))
        # print(dollar, bitcoin)
        print(money_list)
        print(f"阈值: {threshold}     合计: {dollar + bitcoin * data[key - 1]['open']}")


data = get_data()
keep_balance_percentage(data)
# keep_balance_number(data)
# draw_picture(data, money)
