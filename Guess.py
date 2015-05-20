#!/usr/bin/python3

import operator
import Network

def Init(qtMainWindow):
    global gQtMainWindow
    gQtMainWindow = qtMainWindow

class Candidate:
    def __init__(self, a_name = ""):
        self.name = a_name
        self.friendCount = 0

    def AddCount(self):
        self.friendCount = self.friendCount + 1

def AddPending(net, mapping, userList, pending, nextRound, knownRate):
    for user in userList:
        numExistFriend = 0
        for userFriend in net[user]:
            if userFriend in mapping:
                numExistFriend = numExistFriend + 1
        if numExistFriend / len(net[user]) > knownRate:
            pending.append(user)
        else:
            nextRound.append(user)

def UserLink(net1, net2, origMap,
        sampleUserNet1, sampleUserNet2):
    knownFriendRate = 0.6
    pending = []
    nextRound = []
    guessMap1To2 = {}
    usingMap = origMap.copy()
    candidate = {}
    net2Selected = {}
    resultMap = {}
    
    AddPending(net1, origMap, sampleUserNet1, pending, nextRound,
            knownFriendRate)

    while True:
        for user in pending:
            # 为用户创建词典
            if user not in candidate:
                candidate[user] = {}
                candidate[user]["subcandidate"] = {}
            # 将用户与2网络中的所有样本用户进行比较
            for compareUser in sampleUserNet2:
                # 如果2网络的样本用户被选中过，则忽略
                if compareUser in net2Selected:
                    continue
                # 遍历user的好友，
                # 如果他的好友和在2网络中的样本用户近似，
                # 把那个2网络中的样本用户加入候选人列表
                # 并且每当这个候选人多一个相同好友，
                # 好友计数器加1
                for friend in net1[user]:
                    if friend in usingMap:
                        if usingMap[friend] in net2[compareUser]:
                            if not compareUser in candidate[user]["subcandidate"]:
                                        compareCandidate = Candidate(compareUser)
                                        candidate[user]["subcandidate"][compareUser] = compareCandidate
                            candidate[user]["subcandidate"][compareUser].AddCount()

            # 如果user没有候选配对，把他放入
            # nextRound中
            if len(candidate[user]["subcandidate"]) == 0:
                nextRound.append(user)
                del(candidate[user])
                continue

            # 从候选中选出好友计数最大的用户
            candidate[user]["list"] = []
            for a_candidate in candidate[user]["subcandidate"]:
                candidate[user]["list"].append(candidate[user]["subcandidate"][a_candidate])

            candidate[user]["list"].sort(key=operator.attrgetter('friendCount'))
            candidate[user]["primary"] = candidate[user]["list"].pop(0)
        
        selectedCandidate = {}
        # 现在可以进行用户映射，不断去除candidate中重复的primary
        while len(candidate) != len(selectedCandidate):
            # 选取candidate中的一个用户，将它与candidate中
            # 的其余用户的primary进行比较，如果没有重复
            # 则将它列入guessMap1To2，而且从candidate中删除
            # 如果有重复，则将它列入竞争队列
            for user in candidate:
                # 如果用户被标记为删除，则跳过
                if user in selectedCandidate:
                    continue
                # 竞争队列
                competeList = [user]
                for cmpUser in candidate:
                    # 如果等于自身，则跳过
                    if user == cmpUser:
                        continue
                    # 如果用户被标记为删除，则跳过
                    if cmpUser in selectedCandidate:
                        continue
                    # 如果cmpUser的primary和user的primary相同
                    # 说明第一映射发生竞争，加入竞争列表
                    if candidate[user]["primary"].name == candidate[cmpUser]["primary"].name:
                        competeList.append(cmpUser)

                # 存在竞争用户，开始比较谁的大
                if len(competeList) != 1:
                    greatestUser = user
                    greatestPrimary = candidate[user]["primary"].friendCount
                    for competitor in competeList:
                        if candidate[competitor]["primary"].friendCount > greatestPrimary:
                            greatestUser = competitor
                            greatestPrimary = candidate[competitor]["primary"].friendCount
                    # 现在最大的已经选出来了，把他送入guessMap1To2，
                    # 并把它从candiate删除，其他的选取次要候选者
                    guessMap1To2[greatestUser] = candidate[greatestUser]["primary"].name
                    net2Selected[candidate[greatestUser]["primary"].name] = 1
                    selectedCandidate[greatestUser] = True
                    del(competeList[greatestUser])

                    for restUser in competeList:
                        # 如果没有其他候选人了，送入nextRound
                        # 否则将list中的候选人作为primary
                        if len(candidate[restUser]["list"]) == 0:
                            nextRound.append(restUser)
                            del(candidate[restUser])
                        else:
                            candidate[restUser]["primary"] = candidate[restUser]["list"].pop(0)
                # 不存在竞争用户，直接送入guessMap1To2
                else:
                    guessMap1To2[user] = candidate[user]["primary"].name
                    net2Selected[candidate[user]["primary"].name] = 1
                    selectedCandidate[user] = True

        # 如果nextRound清空了，则退出循环
        # 否则将nextRound赋值给pending并清空自身
        if len(nextRound) == 0:
            break
        pending = nextRound.copy()
        nextRound.clear()

        # 将guessMap1To2与usingMap合并
        # 并清空guessMap
        for newUser in guessMap1To2:
            usingMap[newUser] = guessMap1To2[newUser]
            resultMap[newUser] = guessMap1To2[newUser]

        guessMap1To2.clear()

    return resultMap

def LoadSampleList(sampleListPath):
    sampleUserTable = {}
    
    sampleUserTable["first"] = []
    sampleUserTable["second"] = []
    
    with open(sampleListPath["first"]) as file1:
        for user1 in file1:
            sampleUserTable["first"].append(user1.strip())
    
    with open(sampleListPath["second"]) as file2:
        for user2 in file2:
            sampleUserTable["second"].append(user2.strip())
    
    return sampleUserTable

def DoUserLink(filePath, sampleListPath, delimiter = ','):
    networkDataSet = Network.LoadNetworkData(filePath, delimiter)
    sampleUserTable = LoadSampleList(sampleListPath)
    
    result = UserLink(
        networkDataSet["firstNetEdgeList"],
        networkDataSet["secondNetEdgeList"],
        networkDataSet["nodeMapping"],
        sampleUserTable["first"],
        sampleUserTable["second"]
    )
    
    MessageSystem.Info(str(result))