import json
import csv
import time
import re
from datetime import datetime
import urllib.request
from itertools import groupby


def GetNowTime():#获取当前时间并以年月日时间方式显示
    return time.strftime("%y%m%d%H", time.localtime(time.time()))


def data_writer(row):
    """
    数据写入csv文件
    """
    time = GetNowTime()
    fname1 = time + ".csv"
    print(fname1)
    with open(fname1, 'a', encoding='utf-8', newline='') as f:
        csv_out = csv.writer(f)
        csv_out.writerow(['Project', 'company', 'Inserted Size', 'Deleted Size', 'commits'])
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
#            data = response.read()
#            datas = re.search('\[[\s\S]*\]', data)
#            eval(datas.group())
#            s = json.loads(datas, encoding='utf-8')
            data = response.read().split('[')
            data.pop(0)
            data = '['.join(data)[0:-1]
            s = json.loads(data, encoding='utf-8')
            for item in s:
                realtime = str_to_date(item['updated'].split(' ')[0])
                if realtime > end_time:
                    print('此时间不再爬取范围，请稍等------------------------------------------', realtime)
                    continue
                elif start_time <= realtime:
                    if item['branch'] == "master":
                        email = item['owner']['email']

                        company = email.split('@')[1]
                        print(company)
                        companys = company.split('.')[0]
                        print(type(companys))
                        # companys = ".".join(email.split('@')[-1].split(".")[0:-1])
                        print(companys)
                        print(item['project'].split('/')[0])
                        print(item['_number'])
                        row.append((item['project'].split('/')[0], companys,
                                    item['insertions'],
                                    item['deletions']))
                        # print()
                    print('正在爬数据----------------------------', realtime)


                elif start_time > realtime:
                    print('马上结束了即将写数据-----------------------------------------------')
                    return row

            i += 25

        except Exception as e: 
            print('over')
            print(e)
            break



# return row


def clean_data(row):
    """
    清洗数据
    """
    print('row----------------------------:', row)
    row.sort()
    data_list = [{key: list(value_iter)} for key, value_iter in
                 groupby(row, lambda data: data[0])]
    datas = []
    for data in data_list:
        for key, values in data.items():
            name_groups = [list(value_iter) for key, value_iter in groupby(values, lambda data: data[1])]
            print(name_groups)
            for name_group in name_groups:
                insertions = sum([value[2] for value in name_group])
                deletions = sum([value[3] for value in name_group])
                commits = len(name_group)
                datas.append((name_group[0][0], name_group[0][1], insertions, deletions, commits))

    return datas


if __name__ == '__main__':
#    url_base = 'https://gerrit.acumos.org/r/changes/?q=status:merged&n=25&O=81&S='
    
    url_base = 'https://gerrit.onap.org/r/changes/?q=status:merged&n=25&O=81&S='
    start_time = str_to_date(input("start time(2018-10-9):"))
    end_time = str_to_date(input("end_time(2018-10-9):"))
    row_data = spider(url_base)
    data = clean_data(row_data)
    data_writer(data)
