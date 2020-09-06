#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import os
import re
import pandas as pd
import matplotlib
import csv
import apache_log_parser
from datetime import datetime


# 1. Объединяем файлы и формируем распарсенный csv
# Получаем список файлов .log
filelist = os.listdir('/home/v.medvedev/Logs/all_logs/')
all_files = []

for file in filelist:
    if '.gz' not in file and 'ipynb' not in file:
        file_path = '/home/v.medvedev/Logs/all_logs/' + file
        all_files.append(file_path)
        all_files_str = ' '.join(all_files)


# склеиваем получившиеся файлы
os.system('cat '+ all_files_str +' > /home/v.medvedev/Logs/all_log.log')


# Создаем файл log.csv и записываем в него строку заголовка с названим столбцов.
csv_file = open('/home/v.medvedev/Logs/log.csv', 'w')
data = [['remote_host', 'server_name2', 'query_string', 'time_received_isoformat', 'request_method', 'request_url', 'request_http_ver', 'request_url_scheme', 'request_url_query', 'status', 'response_bytes_clf', 'request_header_user_agent', 'request_header_user_agent__browser__family', 'request_header_user_agent__browser__version_string', 'request_header_user_agent__os__family', 'request_header_user_agent__os__version_string', 'request_header_user_agent__is_mobile']]
with csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(data)
csv_file.close()


# "Читаем построчно access.log, парсим строку и записываем разобранные данные в csv"
with open('/home/v.medvedev/Logs/all_log.log') as file:
    for line in file:
        line = line.strip()
        line_parser = apache_log_parser.make_parser("%h %V %q %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"")
        try:
            log_line_data = line_parser(line)
        except Exception as e0:
            print(e0)
            pass
        
        #Пишем в файл нужные данные
        try:
            data = [[log_line_data['remote_host'], log_line_data['server_name2'], log_line_data['query_string'], log_line_data['time_received_isoformat'], log_line_data['request_method'], log_line_data['request_url'], log_line_data['request_http_ver'], log_line_data['request_url_scheme'], log_line_data['request_url_query'], log_line_data['status'], log_line_data['response_bytes_clf'], log_line_data['request_header_user_agent'], log_line_data['request_header_user_agent__browser__family'], log_line_data['request_header_user_agent__browser__version_string'], log_line_data['request_header_user_agent__os__family'], log_line_data['request_header_user_agent__os__version_string'], log_line_data['request_header_user_agent__is_mobile']]]
            csv_file = open('/home/v.medvedev/Logs/log.csv', 'a')
            with csv_file:
                writer = csv.writer(csv_file)
                writer.writerows(data)
                
        except Exception as e:
            print(e)
            

# 2. Строим отчеты
data = pd.read_csv('/home/v.medvedev/Logs/log.csv')

data['date'] = data['time_received_isoformat'].str.split('T').str[0]
data['time_received_isoformat'] = pd.to_datetime(data['time_received_isoformat'])
data['date'] = pd.to_datetime(data['date'])

data['unit'] = data['request_url'].str.split('/').str[1]

# Отчет по топ-30 посещаемых разделов без разбивки на ботов
data['unit'].value_counts().reset_index()[:30].to_csv('/home/v.medvedev/Logs/unit_data.txt', index=False)

# Отчет по топ-30 посещаемых страниц без разбивки на ботов
data['request_url'].value_counts().reset_index()[:30].to_csv('/home/v.medvedev/Logs/request_url_data.txt', index=False)

# Общее распределение статус кодов
data['status'].value_counts().reset_index()[:30].to_csv('/home/v.medvedev/Logs/status_code_data.txt', index=False)

# Посещение всего сайта по дням YandexBot
data[data['request_header_user_agent__browser__family']=='YandexBot'].groupby('date')['date'].count().plot(kind="line", legend = False,  subplots=True, title = 'YandexBot_for_day')[0].get_figure().savefig("/home/v.medvedev/Logs/YandexBot_for_day.png")

# Общее распределение статус кодов по выбранному списку ботов
data[data['request_header_user_agent__browser__family'].isin(['YandexBot', 'Mail.RU_Bot', 'Yandex Browser', 'bingbot', 'Googlebot', 'Chrome', 'Chrome Mobile', 'AhrefsBot'])].assign(dummy = 1).groupby(
  ['request_header_user_agent__browser__family','status']
).size().to_frame().unstack().plot(kind='bar',stacked=True, figsize=(15, 10), title = 'Распределение статус кодов по ботам').get_figure().savefig("/home/v.medvedev/Logs/status_code_bots.png")

# Распределение статус кодов 4xx-5xx YandexBot за весь период
data[(data['status']>400)& (data['request_header_user_agent__browser__family'].isin(['YandexBot']))].assign(dummy = 1).groupby(
  ['date','status']
).size().to_frame().unstack().plot(kind='bar',stacked=True, figsize=(15, 10), title = 'Распределение статус кодов 4xx-5xx YandexBot за весь период').get_figure().savefig("/home/v.medvedev/Logs/status_code_4_5xx_yandex.png")