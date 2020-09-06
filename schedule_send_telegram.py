#!/usr/bin/env python
# coding: utf-8

import telebot;
import schedule
import time

bot = telebot.TeleBot('xxxxxxx:xxxxxxxxxxxxxxxxxxxxx');
 
chat_id = '-xxxxxxx'
             
# Отчеты для отправки
def send_all_status_code():
    doc = open('status_code_data.txt', 'rb')
    bot.send_document(chat_id, doc) 

def send_YandexBot_for_day():
    with open("YandexBot_for_day.png", "rb") as file:
        data = file.read()
        bot.send_photo(chat_id, photo=data)

def send_text():
    bot.send_message(chat_id, 'Отправка отчетов по расписанию')


# Отправка по расписанию
schedule.every().day.at('07:00').do(send_text)    
schedule.every().day.at('07:00').do(send_all_status_code)
schedule.every().day.at('07:00').do(send_YandexBot_for_day)


while True:
    schedule.run_pending()
    time.sleep(60)
    
    


