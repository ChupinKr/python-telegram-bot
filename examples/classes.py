import queue
import requests
from instagrapi import Client as ClientInstApi
from instagrapi import types as typesApi
from datetime import datetime

instApi = ClientInstApi()
instApi.login("dmitry.di83", "testdima0001")

clients = []


def getClientNumber(chatId):
    for i in range(0, len(clients)):
        if chatId == clients[i].chatId:
            return i
    return None

def getHtml(url):
    r = requests.get(url)
    return r

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

        self.followersBots = []

        self.lastMess = ""

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

    def setLastMess(self, mess):
        self.lastMess = mess

    def getLastMess(self):
        return self.lastMess

    #def addStatVk(self, userUrl):
    #    self.StatVk = StatVk(userUrl)

class StatInst:
    # конструктор
    def __init__(self, urlUser):
        self.urlUser = urlUser  # устанавливаем имя
        self.userId = instApi.user_id_from_username(urlUser.split("instagram.com/")[1].split("/")[0])  # устанавливаем имя
        self.followersIds = instApi.user_followers(self.userId)  # список подписчиков
        self.followingsIds = instApi.user_following(self.userId)# список подписок
        self.instLastPost = self.tryGetLastPost()
        self.instLastHist = self.tryGetLastHist()
        self.lastChanges = self.LastChangesInst(self)

    def tryGetLastPost(self):
        resp = instApi.user_medias(self.userId,1)
        if len(resp) > 0:
            return resp[0].code
        return []

    def tryGetLastHist(self):
        resp = instApi.user_stories(self.userId)
        if len(resp) > 0:
            return resp[len(instApi.user_stories(self.userId)) - 1].code
        return []

    def getUserId(self):
        return self.userId

    def getFollowersIds(self):
        return self.followersIds

    def getFollowingsIds(self):
        return self.followingsIds

    def getInstLastPost(self):
        return self.instLastPost

    def getInstLastHist(self):
        return self.instLastHist

    def setFollowersIds(self, followersIds):
        self.followersIds = followersIds

    def setFollowingsIds(self, followingsIds):
        self.followingsIds = followingsIds

    def setInstLastPostId(self, instPost):
        self.instLastPost.append(instPost)

    def setInstLastHistId(self, instHist):
        self.instLastHist.append(instHist)


    class LastChangesInst:
        # конструктор
        def __init__(self, parent):
            self.parent = parent
            self.lastFollowers = []
            self.lastUnfollowers = []
            self.lastFollowings = []
            self.lasUnfollowings = []
            self.lastPhotoDate = []
            self.lastStoryDate = []

        def setNewFollowers(self):
            responce = instApi.user_followers(self.parent.getUserId(), 0, False)
            oldIds = self.parent.getFollowersIds()
            if list(set(responce) - set(oldIds)) != []:
                self.lastFollowers.append(list(set(responce) - set(oldIds)))
                self.parent.setFollowersIds(responce)
                listNewFollowersNicks = self.listUserIdsToUrls(list(set(responce) - set(oldIds)))
                return "На " + self.parent.urlUser + " подписались: \n" + '\n'.join(listNewFollowersNicks)

        def setNewUnfollowers(self):
            responce = instApi.user_followers(self.parent.getUserId(), 0, False)
            oldIds = self.parent.getFollowersIds()
            if list(set(oldIds) - set(responce)) != []:
                self.lastUnfollowers.append(list(set(oldIds) - set(responce)))
                self.parent.setFollowersIds(responce)
                listNewUnfollowersNicks = self.listUserIdsToUrls(list(set(oldIds) - set(responce)))
                return "От " + self.parent.urlUser + " отписались: \n" + '\n'.join(listNewUnfollowersNicks)


        def setNewFollowings(self):
            responce = instApi.user_following(self.parent.getUserId(), 0, False)
            oldIds = self.parent.getFollowingsIds()
            if list(set(responce) - set(oldIds)) != []:
                self.lastFollowings.append(list(set(responce) - set(oldIds)))
                self.parent.setFollowingsIds(responce)
                listNewFollowingsNicks = self.listUserIdsToUrls(list(set(responce) - set(oldIds)))
                return self.parent.urlUser + " подписался на: \n" + '\n'.join(listNewFollowingsNicks)

        def setNewUnfollowings(self):
            responce = instApi.user_following(self.parent.getUserId(), 0, False)
            oldIds = self.parent.getFollowingsIds()
            if list(set(oldIds) - set(responce)) != []:
                self.lasUnfollowings.append(list(set(oldIds) - set(responce)))
                self.parent.setFollowingsIds(responce)
                listNewUnfollowingsNicks = self.listUserIdsToUrls(list(set(oldIds) - set(responce)))
                return self.parent.urlUser + " отписался от : \n" + '\n'.join(listNewUnfollowingsNicks)

        def setNewLastPost(self):
            responce = self.parent.tryGetLastPost()
            oldLastPost = self.parent.getInstLastPost()
            if responce != oldLastPost:
                self.lastPhotoDate.append({"post" : responce.code, "time": responce.taken_at})
                self.parent.setInstLastPostId(responce.code)
                return "Пользователь " + self.parent.urlUser + " добавил пост: \n" + "https://www.instagram.com/p/" + responce

        def setNewLastHistory(self):
            responce = self.parent.tryGetLastHist()
            oldLastPost = self.parent.getInstLastHist()
            if responce != oldLastPost:
                self.lastStoryDate.append({"post": responce.code, "time": responce.taken_at})
                self.parent.setInstLastPostId(responce.code)
                return "Пользователь " + self.parent.urlUser + " добавил новую историю: \n"

        def listUserIdsToUrls(self, listIds):
            listResult = []
            for userID in listIds:
                listResult.append("https://www.instagram.com/" + instApi.username_from_user_id(userID))
            return listResult



def checkClientExist(chatId):
    for client in clients:
        if chatId == client.chatId:
            return True
    clients.append(Client(chatId))
    return False

def main():
    print()
if __name__ == '__main__':
    main()