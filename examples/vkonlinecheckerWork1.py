#!/usr/bin/env python
# pylint: disable=W0613, C0116
# type: ignore[union-attr]
# This program is dedicated to the public domain under the CC0 license.

#import gevent.monkey
#import daemon
import commands as comm
from commands import cls
import pytz
from bs4 import BeautifulSoup
from instagrapi import Client as ClientInstApi
from instagrapi import types as typesApi
from datetime import datetime

#instApi = ClientInstApi()
#instApi.login("dmitry.di83", "testdima0001")


import os
os.getcwd()
import sys
sys.path.append('C:\\Users\\User\\Documents\\GitHub\\python-telegram-bot\\')
import requests
import logging
import threading
import queue
import urllib.request
import json

from time import sleep
#import telebot

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging

logger = logging.getLogger(__name__)
vkIds = []
token='8f7b3067c107b5e658eb0b9c06ac2ba6c135a97e13ceb0a8af99650870fceb5efe365f3bba70e09545c93'
checker = threading.Thread()



queueVK = queue.Queue()
queueAvito = queue.Queue()






def getClientNumber(chatId):
    for i in range(0, len(cls.clients)):
        if chatId == cls.clients[i].chatId:
            return i
    return None

def getHtml(url):
    r = requests.get(url)
    return r





def checkVk(url):
    f = urllib.request.urlopen(url)
    return (json.load(f))

def userIdCompress(userIds):
    result = ""
    for id in userIds:
        result += userIds.split('https://vk.com/')[1]
    return result

def checkOnlineVk(queueVK, update: Update):
    trackedUsers = []
    status = 0
    isCheck = 0
    while True:
        sleep(1)
        try:
            isCheck = queueVK.get(timeout=1)
            if isCheck == 0:
                break
        except queueVK.Empty:
            pass
        #https://vk.com/achtovsezaniato
        fullUrl = 'https://api.vk.com/method/users.get?user_ids=' + \
                  userIdCompress(vkIds) + \
                  '&access_token=' +\
                  token + \
                  '&fields=online&v=5.126'
        json = checkVk(fullUrl)

        isOnline = int(json["response"][0]["online"])
        try:
            isOnlineMobile = int(json["response"][0]["online_mobile"])
        except:
            isOnlineMobile = 0
        try:
            mobileApp = int(json["response"][0]["online_app"])
        except:
            mobileApp = 0

        newStatus = isOnline
        if newStatus != status:
            status = newStatus
            if status == 1:
                if isOnlineMobile == 1:
                    update.message.reply_text("Пользователь " + vkIds[0] + " зашел в систему с телефона через приложение https://vk.com/app" + str(mobileApp))
                else:
                    update.message.reply_text(
                        "Пользователь " + vkIds[0] + " зашел в систему через компьютер")
            else:
                update.message.reply_text("Пользователь " + vkIds[0] + " вышел из системы")

def start_vk_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    if not vkIds:
        update.message.reply_text('Воспользуйтесь командой /add_vk для добавления отслеживаемых аккаунтов')
    else:
        threading.Thread(target=checkOnlineVk, args=[queueVK, update]).start()
        queueVK.put(1)

def add_vk_command(update: Update, context: CallbackContext) -> None:
    """Echo the user message. """
    cls.checkClientExist(update.message.chat_id)
    clientNum = getClientNumber(update.message.chat_id)
    if 'https://vk.com/' in update.message.text:
        cls.clients[clientNum].addVkId(update.message.text.split(" ")[1])
        update.message.reply_text('Ссылка на пользователя добавлена в список для отслеживания')

def stop_vk_command(update: Update, context: CallbackContext) -> None:
    """Echo the user message. """
    queueVK.put(0)

def clear_vk_command(update: Update, context: CallbackContext) -> None:
    """Echo the user message. """
    vkIds.clear()





#обавление статистики за конкретным отслеживаемым юзером и получение его номера у клиента
def getNumInstStatExist(accName, client):
    for statNum in range(0, len(client.statInsts)):
        if accName == client.statInsts[statNum].urlUser:
            return statNum
    client.addStatInst(accName)
    return len(client.statInsts) - 1


#def updateStatInst(accName, update: Update, client, data, statNum):



def checkLastInstInfo(queueInst, update: Update, client: cls.Client):
    while True:
        sleep(1)
        try:
            isCheck = queueInst.get(timeout=1)
            if isCheck == 0:
                break
        except:
            pass
        #для каждого отслеживаемого акка проверяем
        for instUrl in client.instUrls:
            #созаем/получаем номер статистики для этого отслеживаемого акка
            statNum = getNumInstStatExist(instUrl, client)
            #обновляем данные изменений по каждому аккаунту
            renewalStat(update, statNum, client)
            sleep(20)

def renewalStat(update: Update, statNum, client):
    output = ""
    output = client.statInsts[statNum].lastChanges.setNewFollowers()
    if output != None:
        update.message.reply_text(output)
    output = client.statInsts[statNum].lastChanges.setNewUnfollowers()
    if output != None:
        update.message.reply_text(output)
    output = client.statInsts[statNum].lastChanges.setNewFollowings()
    if output != None:
        update.message.reply_text(output)
    output = client.statInsts[statNum].lastChanges.setNewUnfollowings()
    if output != None:
        update.message.reply_text(output)
    output = client.statInsts[statNum].lastChanges.setNewLastPost()
    if output != None:
        update.message.reply_text(output)
    output = client.statInsts[statNum].lastChanges.setNewLastHistory()
    if output != None:
        update.message.reply_text(output)

def add_inst_command(update: Update, context: CallbackContext) -> None:
    """Echo the user message. """
    cls.checkClientExist(update.message.chat_id)
    clientNum = getClientNumber(update.message.chat_id)

    if 'instagram.com/' in update.message.text:
        instUrl = update.message.text.split(" ")[1]
        if update.message.text.split(" ")[1] not in cls.clients[clientNum].instUrls:
            cls.clients[clientNum].addInst(instUrl)
            update.message.reply_text('Ссылка на пользователя добавлена в список отслеживаемых')
        else:
            update.message.reply_text('В списке отслеживаемых уже есть данный пользователь')
    else:
        update.message.reply_text('Не могу понять. \nОтправьте полную ссылку на страницу пользователя в формате https://www.instagram.com/*ник пользователя*')


def start_inst_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    clientNum = getClientNumber(update.message.chat_id)
    if not cls.clients[clientNum].instUrls:
        update.message.reply_text('Воспользуйтесь командой "/add_inst *ссылка на пользователя*"  для добавления отслеживаемых аккаунтов')
    else:
        update.message.reply_text('Запущено отслеживание выбранных аккаунтов, ожидаем изменений...')
        threading.Thread(target=checkLastInstInfo, args=[cls.clients[clientNum].queueInst, update, cls.clients[clientNum]]).start()
        cls.clients[clientNum].queueInst.put(1)

def stop_inst_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    clientNum = getClientNumber(update.message.chat_id)
    update.message.reply_text('Отслеживание остановлено')
    cls.clients[clientNum].queueInst.put(0)

def clear_inst_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    clientNum = getClientNumber(update.message.chat_id)
    cls.clients[clientNum].instUrls = []
    update.message.reply_text('Список отслеживаемых очищен')
    cls.clients[clientNum].queueInst.put(0)






# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.

from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import sqlite3
from sqlite3 import Error

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection





def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Пока функция не активна')

def info_command(update: Update, context: CallbackContext) -> None:
    """Echo the user message. """
    clientNum = getClientNumber(update.message.chat_id)
    update.message.reply_text(cls.clients[clientNum].getClientInfo())








def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1517729956:AAEo8WdIFETkzKx-EGCmAVh3QT1GWvzbNis", use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    updater.dispatcher.add_handler(CommandHandler('start', comm.start))
    updater.dispatcher.add_handler(CallbackQueryHandler(comm.main_menu, pattern='main'))
    updater.dispatcher.add_handler(CallbackQueryHandler(comm.profile_menu, pattern='profile'))
    updater.dispatcher.add_handler(CallbackQueryHandler(comm.buySubscription_menu, pattern='buySubscription'))
    updater.dispatcher.add_handler(CallbackQueryHandler(comm.tracking_menu, pattern='tracking'))
    updater.dispatcher.add_handler(CallbackQueryHandler(comm.tracking_list, pattern='allTrackingList'))
    updater.dispatcher.add_handler(CallbackQueryHandler(comm.tracking_vk_menu, pattern='vkTracking'))
    updater.dispatcher.add_handler(CallbackQueryHandler(comm.tracking_inst_menu, pattern='instTracking'))
    updater.dispatcher.add_handler(CallbackQueryHandler(comm.analysis_menu, pattern='analysis'))
    updater.dispatcher.add_handler(CallbackQueryHandler(comm.analysis_vk_menu, pattern='vkAnalysis'))
    updater.dispatcher.add_handler(CallbackQueryHandler(comm.analysis_inst_menu, pattern='instAnalysis'))
    updater.dispatcher.add_handler(CallbackQueryHandler(comm.tracking_vk_add_menu, pattern='vkAddTracking'))
    updater.dispatcher.add_handler(CallbackQueryHandler(comm.tracking_vk_del_menu, pattern='vkDelTracking'))
    updater.dispatcher.add_handler(CallbackQueryHandler(comm.tracking_vk_clear_menu, pattern='vkClearTracking'))
    updater.dispatcher.add_handler(CallbackQueryHandler(comm.tracking_vk_stop_menu, pattern='vkStopTracking'))
    updater.dispatcher.add_handler(CallbackQueryHandler(comm.tracking_vk_start_menu, pattern='vkStartTracking'))
    updater.dispatcher.add_handler(CallbackQueryHandler(comm.tracking_inst_add_menu, pattern='instAddTracking'))
    updater.dispatcher.add_handler(CallbackQueryHandler(comm.tracking_inst_del_menu, pattern='instDelTracking'))
    updater.dispatcher.add_handler(CallbackQueryHandler(comm.tracking_inst_clear_menu, pattern='instClearTracking'))
    updater.dispatcher.add_handler(CallbackQueryHandler(comm.tracking_inst_stop_menu, pattern='instStopTracking'))
    updater.dispatcher.add_handler(CallbackQueryHandler(comm.tracking_inst_start_menu, pattern='instStartTracking'))

    dispatcher.add_handler(CommandHandler("add_inst", add_inst_command))
    dispatcher.add_handler(CommandHandler("start_inst", start_inst_command))
    dispatcher.add_handler(CommandHandler("stop_inst", stop_inst_command))
    dispatcher.add_handler(CommandHandler("clear_inst", clear_inst_command))

    dispatcher.add_handler(CommandHandler("start_vk", start_vk_command))
    dispatcher.add_handler(CommandHandler("add_vk", add_vk_command))
    dispatcher.add_handler(CommandHandler("stop_vk", stop_vk_command))
    dispatcher.add_handler(CommandHandler("clear_vk", clear_vk_command))

    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("info", info_command))

    updater.dispatcher.add_handler(CallbackQueryHandler(comm.analysis_start, pattern='add_analysis'))
    updater.dispatcher.add_handler(CallbackQueryHandler(comm.tracking_start, pattern='add_tracking'))

    # on noncommand i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, comm.useCommands))

    # Start the Bot
    updater.start_polling()

    updater.idle()



if __name__ == '__main__':
    main()
