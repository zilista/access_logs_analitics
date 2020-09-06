#!/usr/bin/env python
# coding: utf-8

from requests_html import HTMLSession
from bs4 import BeautifulSoup
import re
from datetime import datetime
import pandas as pd
import os
import gzip


session = HTMLSession()

## 1. Получаем ссылки на лог файлы и их даты дней хранимых логов.
req = session.get('xx.xx.xx.xx/logs/')
a_hrefs = req.html.xpath('//a/text()')
logs_list = req.html.xpath('//pre/a/following::text()[2]')
date_list = req.html.xpath('//pre/a/following::text()[3]')


## 2. Достаем список дат
data_list_clear = []

for item in date_list:
    data_list_clear.append(re.findall(r'\s\s*(\d{1,2}-\D{1,3}-\d{4}).*', item)[0])


## 3. Сопоставляем логи с датами
logs_date_all = dict(zip(logs_list, data_list_clear))


## 4. Отфилтруем только access логи
logs_date_author24_access = {}
for log_name, date in logs_date_all.items():
    if log_name.startswith('author24.access'):
        logs_date_author24_access[log_name] = date


## 5. Формируем список логов на скачивание. Берем за последние 7 дней
current_date = datetime.now()

logs_for_download = []

for log, date in logs_date_author24_access.items():
    date_log = datetime.strptime(date, '%d-%b-%Y') #f'{date}'
    delta = current_date - date_log
    if delta.days <=7:
        logs_for_download.append(log)


## 6. Место куда будем складывать архивы. Предварительно чистим старые архивы
dir_path = '/home/v.medvedev/Logs/all_logs/'
get_file_list = os.listdir(dir_path)

def clear_dir(dir_path):
    for file in get_file_list:
        if 'ipynb_chec' not in file:
            os.remove(dir_path + '/' + file)

clear_dir(dir_path)


def save_logs(log):
    try:

        with session as s:
            load = s.get('xx.xx.xx.xx/logs/'+log, stream=True)
            
            with open('/home/v.medvedev/Logs/all_logs/'+log, "wb") as save_command:
                for chunk in load.iter_content(chunk_size=1024, decode_unicode=False):
                    if chunk:
                        save_command.write(chunk)
                        save_command.flush()
                        
    except Exception as e:
        print(e)
        pass


for log in logs_for_download:
    save_logs(log)



## 7. Распаковка архивов
def gunzip(source_filepath, dest_filepath, block_size=65536):
    with gzip.open(source_filepath, 'rb') as s_file, open(dest_filepath, 'wb') as d_file:
        while True:
            block = s_file.read(block_size)
            if not block:
                break
            else:
                d_file.write(block)


get_file_list = os.listdir(dir_path)


for log in get_file_list:
    if log.split('.')[-1] == 'gz' and 'ipynb_chec' not in log:
        gunzip(dir_path + '/' + log, dir_path + '/'+ log.split(".gz")[0])