import json
import csv
import time
from datetime import datetime
import urllib.request
from itertools import groupby


def GetNowTime():  # 获取当前时间并以年月日时间方式显示
    return time.strftime("%y%m%d%H", time.localtime(time.time()))


def data_writer(row, date):
    """
    数据写入csv文件
    """
    time = GetNowTime()
    fname1 = time + ".csv"
    print(fname1)
    with open(fname1, 'a', encoding='utf-8', newline='') as f:
        csv_out = csv.writer(f)
        csv_out.writerow(['Inserted Size', 'Deleted Size', 'date', 'weeks', date+"_commits"])
        for data in row:
            csv_out.writerow(data)


def str_to_date(str_date):
    """
    字符串转为时间格式
    """
    date_obj = datetime.strptime(str_date, '%Y-%m-%d').date()
    return date_obj


def spider(url_base):
    """
    爬虫
    """

    print(start_time, end_time)
    row = []

    i = 0
    while True:
        try:

            response = urllib.request.urlopen(url_base + str(i))
            page = (int(i) / 25) + 1
            print("第%s页--------------------------------------------------------------------" % page)
            s = json.loads(response.read()[4:-1], encoding='utf-8')
            for item in s:
                date = item['updated'].split(' ')[0]
                realtime = str_to_date(date)
                if realtime > end_time:
                    print('此时间不再爬取范围，请稍等------------------------------------------', realtime)
                    continue
                elif start_time <= realtime:
                    if item['branch'] == "master":
                        # name = item['owner']['name']
                        insertions = item['insertions']
                        deletions = item['deletions']
                        row.append((insertions, deletions, date))
                    print('正在爬数据----------------------------', realtime)


                elif start_time > realtime:
                    print('马上结束了即将写数据-----------------------------------------------')
                    return row

            i += 25

        except:
            print('over')
            break


# return row


def clean_data(row, date_arg):
    """
    清洗数据
    """
    datas = []

    if date_arg == 'day':
        func = lambda value: str_to_date(value[2])
    elif date_arg == 'week':
        func = lambda value: str(str_to_date(value[2]).year)+'-'+str(str_to_date(value[2]).isocalendar()[1])
    elif date_arg == 'month':
        func = lambda value: str_to_date(value[2]).strftime('%Y-%m')
    date_datas = group_date(row, date_arg, func)
    datas.extend(date_datas)

    return datas


def group_date(data, date_arg, func):
    """
    按照day、week、month 进行排序
    """
    date_sorted = sorted(data, key=func, reverse=True)
    date_groups = [{key: list(value_iter)} for key, value_iter in groupby(date_sorted, func)]

    date_datas = []
    for date_group_dict in date_groups:
        for date, date_group in date_group_dict.items():
            date_time = ''
            get_date = str_to_date(date_group[0][2])
            if date_arg == 'day':
                date_time = date
            elif date_arg == 'week':
                str(date).split("-")
                date_time = str(date).split("-")[0]
                weeks = str(date).split("-")[1]
                print(type(date_time))

            elif date_arg == 'month':
                date_time = str(date)

            # name = date_group[0][0]
            insertions = sum([value[0] for value in date_group])
            deletions = sum([value[1] for value in date_group])
            day_commits = len(date_group)
            out_day_data = (insertions, deletions, date_time, weeks, day_commits)
            date_datas.append(out_day_data)
    return date_datas


if __name__ == '__main__':
    url_base = 'https://gerrit.acumos.org/r/changes/?q=status:merged&n=25&O=81&S='
    start_time = str_to_date(input("start time(2018-10-9):"))
    end_time = str_to_date(input("end_time(2018-10-9):"))
    # start_time = str_to_date("2019-04-18")
    # end_time = str_to_date("2019-04-22")
    date_arg = input("please input time parameters：(eg: month、day、week)")
    row_data = spider(url_base)
    data = clean_data(row_data, date_arg)
    data_writer(data, date_arg)