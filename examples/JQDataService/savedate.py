import os
import csv
from datetime import datetime, time

from vnpy.trader.constant import Exchange
from vnpy.trader.database import database_manager
from vnpy.trader.object import TickData


def run_load_csv():
    """
    遍历同一文件夹内所有csv文件，并且载入到数据库中
    """
    for file in os.listdir("."):
        if not file.endswith(".csv"):
            continue

        print("载入文件：", file)
        csv_load(file)


def csv_load(file):
    """
    读取csv文件内容，并写入到数据库中
    """
    with open(file, "r") as f:
        reader = csv.DictReader(f)

        ticks = []
        start = None
        count = 0

        for item in reader:

            # generate datetime
            # date = item["交易日"]
            # second = item["最后修改时间"]
            # millisecond = item["最后修改毫秒"]
            #
            # standard_time = date + " " + second + "." + millisecond
            # dt = datetime.strptime(standard_time, "%Y%m%d %H:%M:%S.%f")
            dt = item["datetime"]

            # # filter
            # if dt.time() > time(15, 1) and dt.time() < time(20, 59):
            #     continue

            tick = TickData(
                symbol="c2005",
                datetime=dt,
                exchange=Exchange.DCE,
                last_price=float(item["DCE.c2005.last_price"]),
                volume=float(item["DCE.c2005.volume"]),
                bid_price_1=float(item["DCE.c2005.ask_price1"]),
                bid_volume_1=float(item["DCE.c2005.ask_volume1"]),
                ask_price_1=float(item["DCE.c2005.bid_price1"]),
                ask_volume_1=float(item["DCE.c2005.bid_volume1"]),
                gateway_name="DB",
            )
            ticks.append(tick)

            # do some statistics
            count += 1
            if not start:
                start = tick.datetime

        end = tick.datetime
        database_manager.save_tick_data(ticks,"c2005")

        print("插入数据", start, "-", end, "总数量：", count)


if __name__ == "__main__":
    run_load_csv()