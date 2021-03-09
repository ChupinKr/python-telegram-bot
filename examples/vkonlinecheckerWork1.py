#!/usr/bin/env python
# pylint: disable=W0613, C0116
# type: ignore[union-attr]
# This program is dedicated to the public domain under the CC0 license.

#import gevent.monkey
#import daemon
from bs4 import BeautifulSoup
from instagrapi import Client as ClientInstApi
from instagrapi import types as typesApi

instApi = ClientInstApi()
instApi.login("dmitry.di83", "testdima0001")

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

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging

logger = logging.getLogger(__name__)
vkIds = []
token='8f7b3067c107b5e658eb0b9c06ac2ba6c135a97e13ceb0a8af99650870fceb5efe365f3bba70e09545c93'
checker = threading.Thread()
clients = []


queueVK = queue.Queue()
queueAvito = queue.Queue()


class Client:
    # конструктор
    def __init__(self, chatId):
        self.chatId = chatId  # устанавливаем имя
        self.vkIds = []  # устанавливаем отслеживаемые id vk
        self.instUrls = []  # устанавливаем отслеживаемые inst акки

        self.queueVK = queue.Queue()
        self.queueInst = queue.Queue()

        self.statInsts = []
        self.statVks = []

    def addVkId(self, vkId):
        self.vkIds.append(vkId)

    def addInst(self, instUrl):
        self.instUrls.append(instUrl)

    def getClientInfo(self):
        result = ""
        if self.vkIds:
            result += "Отслеживаемые вк: " + ", ".join(self.vkIds) + "\n"
        if self.instUrls:
            result += "Отслеживаемые инсты: " + ", ".join(self.instUrls) + "\n"
        if not self.vkIds and not self.instUrls:
            return "У вас нет отслеживаемых аккаунтов"
        return result


    def addStatInst(self, userUrl):
        self.statInsts.append(StatInst(userUrl))

    #def addStatVk(self, userUrl):
    #    self.StatVk = StatVk(userUrl)

class StatInst:
    # конструктор
    def __init__(self, urlUser):
        self.urlUser = urlUser  # устанавливаем имя
        self.userId = instApi.user_id_from_username(urlUser.split("https://www.instagram.com/")[1].split("/")[0])  # устанавливаем имя
        self.followersIds = self.getUserFollowersIds()  # список подписчиков
        self.followingsIds = self.getUserFollowersIds() # список подписок
        self.instLastPost = self.getInstLastPost()
        self.instLastHist = self.getInstLastHist()
        self.lastChanges = LastChangesInst()


    def getInstLastPost(self, instPost):
        self.instLastPost.append(instPost)

    def getInstLastHist(self, instHist):
        self.instLastHist.append(instHist)

    def getUserFollowersIds(self):
        followers = []
        responce = instApi.user_followers("15434397953")
        for follower in responce:
            followers.append(follower)
        return followers

    def getUserFollowingsIds(self):
        followers = []
        responce = instApi.user_followings("15434397953")
        for follower in responce:
            followers.append(follower)
        return followers

class LastChangesInst:
    # конструктор
    def __init__(self, instId):
        self.lastFollowers = []
        self.lastUnfollowers = []
        self.lastFollowing = []
        self.lastFollowing = []
        self.lastPhotoDate = []
        self.lastStoryDate = []

    def getNewFollowers(self, instId):
        responce = instApi.user_followers(instId)

def checkClientExist(chatId):
    for client in clients:
        if chatId == client.chatId:
            return True
    clients.append(Client(chatId))
    return False

def getClientNumber(chatId):
    for i in range(0, len(clients)):
        if chatId == clients[i].chatId:
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
    checkClientExist(update.message.chat_id)
    clientNum = getClientNumber(update.message.chat_id)
    if 'https://vk.com/' in update.message.text:
        clients[clientNum].addVkId(update.message.text.split(" ")[1])
        update.message.reply_text('Ссылка на пользователя добавлена в список для отслеживания')

def stop_vk_command(update: Update, context: CallbackContext) -> None:
    """Echo the user message. """
    queueVK.put(0)

def clear_vk_command(update: Update, context: CallbackContext) -> None:
    """Echo the user message. """
    vkIds.clear()





def getInfoInstAcc(instUrl):
    data = {}
    html = getHtml(instUrl)
    soup = BeautifulSoup(html.text, "html.parser")
    meta = soup.find("meta", property="og:description")
    s = meta.attrs['content'].split("-")[0].split(" ")
    data['Followers'] = s[0]
    data['Following'] = s[2]
    lastPhoto = html.content.decode("utf-8").split("shortcode\":\"")[1].split("\",\"dimensions")[0]
    data['LastPhoto'] = lastPhoto
    return data

def getNumInstStatExist(accName, client):
    for statNum in range(0, len(client.statInsts)):
        if accName == client.statInsts[statNum].urlUser:
            return statNum
    client.addStatInst(accName)
    return len(client.statInsts) - 1


#def updateStatInst(accName, update: Update, client, data, statNum):


def addNewStatInst(client, data, statNum):
    client.statInsts[statNum].instLastCountFollowers = data.get('Followers')
    client.statInsts[statNum].instLastCountFollowings = data.get('Followings')
    client.statInsts[statNum].addInstLastPost(data.get('LastPhoto'))

def checkLastInstInfo(queueInst, update: Update, client: Client):
    while True:
        sleep(1)
        try:
            isCheck = queueInst.get(timeout=1)
            if isCheck == 0:
                break
        except:
            pass
        for instUrl in client.instUrls:
            sleep(10)
            data = getInfoInstAcc(instUrl)
            statNum = getNumInstStatExist(instUrl, client)
            #если новый отслеживаемый акк
            if(client.statInsts[statNum].instLastCountFollowers == -1):
                client.statInsts[statNum].instLastCountFollowers = data.get('Followers')
                client.statInsts[statNum].instLastCountFollowings = data.get('Followings')
                client.statInsts[statNum].addInstLastPost(data.get('LastPhoto'))
            # если уже есть история отслеживания
            #else:

        print(1)

def add_inst_command(update: Update, context: CallbackContext) -> None:
    """Echo the user message. """
    checkClientExist(update.message.chat_id)
    clientNum = getClientNumber(update.message.chat_id)

    if 'https://www.instagram.com/' in update.message.text:
        instUrl = update.message.text.split(" ")[1]
        if update.message.text.split(" ")[1] in clients[clientNum].instUrls:
            clients[clientNum].addInst(instUrl)
            update.message.reply_text('Ссылка на пользователя добавлена в список отслеживаемых')
        else:
            update.message.reply_text('В списке отслеживаемых уже есть данный пользователь')
    else:
        update.message.reply_text('Не могу понять. \nОтправьте полную ссылку на страницу пользователя в формате https://www.instagram.com/*ник пользователя*')


def start_inst_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    clientNum = getClientNumber(update.message.chat_id)
    if not clients[clientNum].instUrls:
        update.message.reply_text('Воспользуйтесь командой "/add_inst *ссылка на пользователя*"  для добавления отслеживаемых аккаунтов')
    else:
        threading.Thread(target=checkLastInstInfo, args=[clients[clientNum].queueInst, update, clients[clientNum]]).start()
        clients[clientNum].queueInst.put(1)



# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    if (checkClientExist(update.message.chat_id)):
        update.message.reply_text('Здравствуйте, мы вас помним, список доступных команд:')
    else:
        update.message.reply_text('Добро пожаловать, это сервис по поиску и слежке, список доступных команд:')

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Пока функция не активна')

def info_command(update: Update, context: CallbackContext) -> None:
    """Echo the user message. """
    clientNum = getClientNumber(update.message.chat_id)
    update.message.reply_text(clients[clientNum].getClientInfo())

def useCommands(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text('Пожалуйста, воспользуйтесь командами')

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1517729956:AAEo8WdIFETkzKx-EGCmAVh3QT1GWvzbNis", use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))

    dispatcher.add_handler(CommandHandler("add_inst", add_inst_command))
    dispatcher.add_handler(CommandHandler("start_inst", start_inst_command))
    #dispatcher.add_handler(CommandHandler("stop_inst", stop_inst_command))
    #dispatcher.add_handler(CommandHandler("clear_inst", clear_inst_command))

    dispatcher.add_handler(CommandHandler("start_vk", start_vk_command))
    dispatcher.add_handler(CommandHandler("add_vk", add_vk_command))
    dispatcher.add_handler(CommandHandler("stop_vk", stop_vk_command))
    dispatcher.add_handler(CommandHandler("clear_vk", clear_vk_command))

    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("info", info_command))



    # on noncommand i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, useCommands))

    # Start the Bot
    updater.start_polling()

    updater.idle()



if __name__ == '__main__':
    list1 = [u'Вася', u'Петя', u'Маша', u'Саша']
    list2 = [u'Вася', u'Петя']
    list3 = list(set(list1) - set(list2))
    print(list3)

    #main()
