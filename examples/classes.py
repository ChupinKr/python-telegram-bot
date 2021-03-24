import queue
import requests
from instagrapi import Client as ClientInstApi
from instagrapi import types as typesApi
from datetime import datetime

instApi = ClientInstApi()
instApi.login("chupin.kr", "tomo4kazayka1")

clients = []


def getClientNumber(chatId):
    for i in range(0, len(clients)):
        if chatId == clients[i].chatId:
            return i
    return None

def getHtml(url):
    r = requests.get(url)
    return r

def getTargetNameAndCountUnreaded(update, isVk):
    result = []
    clientNum = getClientNumber(update.callback_query.message.chat_id)
    if (isVk):
        for stat in clients[clientNum].statVks:
            #if(stat.countUnreadedChanges > 0):
                result.append(stat.urlUser + " - " + str(stat.countUnreadedChanges))
    else:
        for stat in clients[clientNum].statInsts:
            #if(stat.countUnreadedChanges > 0):
                result.append(stat.urlUser + " - " + str(stat.countUnreadedChanges))
    return result

def getStatNumByUserUlr(client, userNum):
    num = 0
    if("Vk" in userNum):
        num = int(userNum.split("userCountUnreadedVk")[1])
        return client.statVks[num]
    else:
        num = int(userNum.split("userCountUnreadedInst")[1])
        return client.statInsts[num]

def getLastChangesByStat(stat):
    result = ""
    for lastChange in stat.lastChanges:
        if lastChange.lastFollowers != None:
            result += "Последние подписчики: " + "\n".join(lastChange.lastFollowers)
        if lastChange.lastUnfollowers != None:
            result += "\nПоследние отписавшиеся: " + "\n".join(lastChange.lastUnfollowers)
        if lastChange.lastFollowings != None:
            result += "\nПоследние подписки: " + "\n".join(lastChange.lastFollowings)
        if lastChange.lastUnfollowings != None:
            result += "\nПоследние отписки: " + "\n".join(lastChange.lastUnfollowings)
        if lastChange.lastPhotoDate != None:
            result += "\nПоследнее фото: " + lastChange.lastPhotoDate.post + " время публикации: " + lastChange.lastPhotoDate.time
        if lastChange.lastStoryDate != None:
            result += "\nПоследняя история: " + lastChange.lastStoryDate.post + " время публикации: " + lastChange.lastStoryDate.time
    return result

class Client:
    # конструктор
    def __init__(self, chatId):
        self.chatId = chatId  # устанавливаем имя
        self.vkIds = []  # устанавливаем отслеживаемые id vk
        self.instUrls = []  # устанавливаем отслеживаемые inst акки

        self.queueVK = queue.Queue()
        self.queueInst = queue.Queue()

        self.isCheckingVk = False
        self.isCheckingInst = False

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
        if("instagram.com" in self.lastMess):
            return self.lastMess.strip().split("?")[0]
        else:
            return self.lastMess

    #def addStatVk(self, userUrl):
    #    self.StatVk = StatVk(userUrl)

class StatInst:
    # конструктор
    def __init__(self, urlUser):
        self.urlUser = urlUser  # устанавливаем имя
        self.userId = instApi.user_id_from_username(urlUser.split("instagram.com/")[1].split("/")[0])  #устанавливаем имя
        self.followersIds = instApi.user_followers(self.userId)  #список подписчиков
        self.followingsIds = instApi.user_following(self.userId) #список подписок
        self.instLastPost = self.tryGetLastPost()
        self.instLastHist = self.tryGetLastHist()
        self.lastChanges = [] #тут должен быть массив
        #self.lastChanges.append(self.LastChangesInst(self))

        self.countUnreadedChanges = 0  # сначала можно будет прочитать изменения, потом они подтираются, в случае чего можно их сохранить в файл

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
            self.lastFollowers = None
            self.lastUnfollowers = None
            self.lastFollowings = None
            self.lastUnfollowings = None
            self.lastPhotoDate = None
            self.lastStoryDate = None

        def setNewFollowers(self):
            responce = instApi.user_followers(self.parent.getUserId(), 0, False)
            oldIds = self.parent.getFollowersIds()
            if list(set(responce) - set(oldIds)) != []:
                self.lastFollowers = self.listUserIdsToUrls(list(set(responce) - set(oldIds)))
                self.parent.setFollowersIds(responce)
                #listNewFollowersNicks = self.listUserIdsToUrls(list(set(responce) - set(oldIds)))
                return self.lastFollowers

        def setNewUnfollowers(self):
            responce = instApi.user_followers(self.parent.getUserId(), 0, False)
            oldIds = self.parent.getFollowersIds()
            if list(set(oldIds) - set(responce)) != []:
                self.lastUnfollowers = self.listUserIdsToUrls(list(set(oldIds) - set(responce)))
                self.parent.setFollowersIds(responce)
                #listNewUnfollowersNicks = self.listUserIdsToUrls(list(set(oldIds) - set(responce)))
                return self.lastUnfollowers


        def setNewFollowings(self):
            responce = instApi.user_following(self.parent.getUserId(), 0, False)
            oldIds = self.parent.getFollowingsIds()
            if list(set(responce) - set(oldIds)) != []:
                self.lastFollowings = self.listUserIdsToUrls(list(set(responce) - set(oldIds)))
                self.parent.setFollowingsIds(responce)
                #listNewFollowingsNicks = self.listUserIdsToUrls(list(set(responce) - set(oldIds)))
                return self.lastFollowings

        def setNewUnfollowings(self):
            responce = instApi.user_following(self.parent.getUserId(), 0, False)
            oldIds = self.parent.getFollowingsIds()
            if list(set(oldIds) - set(responce)) != []:
                self.lastUnfollowings = self.listUserIdsToUrls(list(set(oldIds) - set(responce)))
                self.parent.setFollowingsIds(responce)
                #listNewUnfollowingsNicks = self.listUserIdsToUrls(list(set(oldIds) - set(responce)))
                return self.lastUnfollowings

        def setNewLastPost(self):
            responce = self.parent.tryGetLastPost()
            oldLastPost = self.parent.getInstLastPost()
            if responce != oldLastPost:
                self.lastPhotoDate = ({"post" : "https://www.instagram.com/p/" + responce.code, "time": responce.taken_at})
                self.parent.setInstLastPostId(responce.code)
                return self.lastPhotoDate

        def setNewLastHistory(self):
            responce = self.parent.tryGetLastHist()
            oldLastPost = self.parent.getInstLastHist()
            if responce != oldLastPost:
                self.lastStoryDate = ({"post": responce.code, "time": responce.taken_at})
                self.parent.setInstLastPostId(responce.code)
                return self.lastStoryDate

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