import time


def millisecond_timestamp_to_date(timestamp: int, str_format: str = "%Y-%m-%d"):
    """
    毫秒时间戳转日期
    :param timestamp:
    :param str_format:
    :return:
    """
    timestamp = int(timestamp) / 1000
    local_time = time.localtime(timestamp)
    time_str = time.strftime(str_format, local_time)
    return time_str
