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
        csv_out.writerow(['owner', 'Inserted Size', 'Deleted Size', 'date', date+"_commits"])
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
                        name = item['owner']['name']
                        insertions = item['insertions']
                        deletions = item['deletions']
                        row.append((name, insertions, deletions, date))
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
    row.sort()
    # data_list: 按name对数据进行排序
    data_list = [{key: list(value_iter)} for key, value_iter in
                 groupby(row, lambda data: data[0])]
    datas = []

    for data in data_list:
        for key, values in data.items():
            # eg: data --> ('Fu Jinhua', 0, 0, '2019-04-22') value[3] 获取时间
            if date_arg == 'day':
                func = lambda value: str_to_date(value[3]).day
            elif date_arg == 'week':
                func = lambda value: str_to_date(value[3]).isocalendar()[1]
                # func = lambda value: str(str_to_date(value[3]).year) + '-' + str(
                #     str_to_date(value[3]).isocalendar()[1])
            elif date_arg == 'month':
                func = lambda value: str_to_date(value[3]).month
            date_datas = group_date(key, data, date_arg, func)
            datas.extend(date_datas)
            # date_sorted = sorted(data[key], key=lambda value: value[3], reverse=True)
            # date_groups = [list(value_iter) for key, value_iter in groupby(date_sorted, lambda data: data[3])]
            # for date_group in date_groups:
            #     name = date_group[0][0]
            #     date = date_group[0][3]
            #     insertions = sum([value[1] for value in date_group])
            #     deletions = sum([value[2] for value in date_group])
            #     day_commits = len(date_group)
            #     out_day_data = (name, insertions, deletions, date, day_commits)
            #     datas.append(out_day_data)
    # for data in data_list:
    #     for key, values in data.items():
    #         name_groups = [list(value_iter) for key, value_iter in groupby(values, lambda data: data[1])]
    #         for name_group in name_groups:
    #             insertions = sum([value[1] for value in name_group])
    #             deletions = sum([value[2] for value in name_group])
    #             commits = len(name_group)
    #             datas.append((name_group[0][0], insertions, deletions, name_group[0][2], commits))

    return datas


def group_date(key, data, date_arg, func):
    """
    按照day、week、month 进行排序
    """
    date_sorted = sorted(data[key], key=func, reverse=True)
    date_groups = [list(value_iter) for key, value_iter in groupby(date_sorted, func)]

    date_datas = []
    for date_group in date_groups:
        get_date = str_to_date(date_group[0][3])
        if date_arg == 'day':
            date = get_date
        elif date_arg == 'week':
#            date = get_date.isocalendar()[1]
            date = get_date.strftime('%Y-%U')
            #date = get_date
        elif date_arg == 'month':
            date = get_date.strftime('%Y-%m')

        name = date_group[0][0]
        insertions = sum([value[1] for value in date_group])
        deletions = sum([value[2] for value in date_group])
        day_commits = len(date_group)
        out_day_data = (name, insertions, deletions, date, day_commits)
        date_datas.append(out_day_data)
    return date_datas


if __name__ == '__main__':
#    url_base = 'https://gerrit.onap.org/r/changes/?q=status:merged&n=25&O=81&S='
    url_base = 'https://gerrit.acumos.org/r/changes/?q=status:merged&n=25&O=81&S='
    start_time = str_to_date(input("start time(2018-10-9):"))
    end_time = str_to_date(input("end_time(2018-10-9):"))
#    start_time = str_to_date("2019-4-20")
#    end_time = str_to_date("2019-4-22")
    date_arg = input("please input time parameters：(eg: month、day、week)")
    row_data = spider(url_base)
    data = clean_data(row_data, date_arg)
    data_writer(data, date_arg)
