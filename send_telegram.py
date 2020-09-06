#!/usr/bin/env python
# coding: utf-8

import telebot;
bot = telebot.TeleBot('xxxxxxx:xxxxxxxxxxxxxxxxx');

chat_id = 'xxxxxxxxx'

# Обработчик текстовых сообщений к боту. 
@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    #print(message.chat.id) - чтобы узнать id чата

    if message.text == "/start":
        bot.send_message(chat_id, "Привет, я бот отчетов по логам. Чтобы продолжить введи команду '/help'")
    
    elif message.text == "/help":
        bot.send_message(chat_id, "Доступны следующие команды:")
        bot.send_message(chat_id, "/top_unit - топ посещаемых разделов \n/top_urls – топ посещаемых страниц\n/all_status_code – распределение страниц по коду ответа\n/YandexBot_for_day - распределение YandexBot по дням\n/YandexBot_lenta_200 -  посещение YandexBot раздела (200-ок) по дням")
        
    elif message.text == '/top_unit':
        doc = open('unit_data.txt', 'rb')
        bot.send_document(chat_id, doc)
        
    elif message.text == '/top_urls':
        doc = open('request_url_data.txt', 'rb')
        bot.send_document(chat_id, doc)   
        
    elif message.text == '/all_status_code':
        doc = open('status_code_data.txt', 'rb')
        bot.send_document(chat_id, doc)   
        
    elif message.text == "/YandexBot_for_day":
        bot.send_message(chat_id, "Подожди. Отчет формируется")
        
        with open("YandexBot_for_day.png", "rb") as file:
            data = file.read()
        bot.send_photo(chat_id, photo=data)
        
    elif message.text == "/YandexBot_lenta_200":
        bot.send_message(chat_id, "Подожди. Отчет формируется")
        
        with open("YandexBot_lenta_200.png", "rb") as file:
            data = file.read()
        bot.send_photo(chat_id, photo=data)
        
      
    else:
        bot.send_message(message.chat.id, "Я тебя не понимаю. Напиши /help.")


bot.polling(none_stop=True, interval=0)



