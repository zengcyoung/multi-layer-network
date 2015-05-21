#!/usr/bin/python3

import operator
import Network
import MessageSystem

def Init(qtMainWindow):
    global gQtMainWindow
    gQtMainWindow = qtMainWindow

class Candidate:
    def __init__(self, a_name = ""):
        self.name = a_name
        self.friendCount = 0
        
    def __str__(self):
        return "{0} => {1}".format(self.name, self.friendCount)
    
    def __repr__(self):
        return "name: {0}, friendCount: {1}".format(self.name, self.friendCount)

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
    global gQtMainWindow
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
    
    print("net1: {}".format(net1))
    print("net2: {}".format(net2))
    
    prevPending = []
    samePendingCount = 0
    while True:
        if prevPending == pending:
            samePendingCount += 1
            if samePendingCount == 10000:
                print("Over 10000 repeated pending!!!")
                break
        print("pending: {}".format(pending))
        gQtMainWindow.updateInterface()
        for user in pending:
            gQtMainWindow.updateInterface() 
            # 为用户创建词典
            if user not in candidate:
                candidate[user] = {}
                candidate[user]["subcandidate"] = {}
            # 将用户与2网络中的所有样本用户进行比较
            print("candidate: {}".format(candidate))
            for compareUser in sampleUserNet2:
                # 如果2网络的样本用户被选中过，则忽略
                print("net2Selected: {}".format(net2Selected))
                if compareUser in net2Selected:
                    continue
                # 遍历user的好友，
                # 如果他的好友和在2网络中的样本用户近似，
                # 把那个2网络中的样本用户加入候选人列表
                # 并且每当这个候选人多一个相同好友，
                # 好友计数器加1
                print("usingMap: {}".format(usingMap))
                for friend in net1[user]:
                    print("friend: {}".format(friend))
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
        print("candidate: {}".format(candidate))
        # 现在可以进行用户映射，不断去除candidate中重复的primary
        print("Deleting duplicated primary")
        while len(candidate) != len(selectedCandidate):
            # 选取candidate中的一个用户，将它与candidate中
            # 的其余用户的primary进行比较，如果没有重复
            # 则将它列入guessMap1To2，而且从candidate中删除
            # 如果有重复，则将它列入竞争队列
            print("selectedCandidate: {}".format(selectedCandidate))
            for user in candidate:
                print("{}'s candidate is being watched".format(user))
                # 如果用户被标记为删除，则跳过
                if user in selectedCandidate:
                    print("but {} is in the selectedCandidate".format(user))
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
                
                print("competeList: {}".format(competeList))

                # 存在竞争用户，开始比较谁的大
                sameCountCompetitor = {}
                if len(competeList) != 1:
                    greatestUser = user
                    greatestPrimary = candidate[user]["primary"].friendCount
                    for competitor in competeList:
                        if candidate[competitor]["primary"].friendCount > greatestPrimary:
                            greatestUser = competitor
                            greatestPrimary = candidate[competitor]["primary"].friendCount
                        # 如果好友数目一样，那么加入sameCountCompetitor列表
                        # 之后看谁的候选列表小就选谁，如果候选列表数目一样
                        # 忽略不再比较
                        if candidate[competitor]["primary"].friendCount == greatestPrimary:
                            if greatestPrimary not in sameCountCompetitor:
                                sameCountCompetitor[greatestPrimary] = []
                            sameCountCompetitor[greatestPrimary].append(competitor)
                    
                    leastCandidateUser = greatestUser
                    leastCandidateCount = candidate[leastCandidateUser]["primary"].friendCount
                    if len(sameCountCompetitor[greatestPrimary]) != 0:
                        for candidateCountCompetitor in sameCountCompetitor[greatestPrimary]:
                            if candidate[candidateCountCompetitor]["primary"].friendCount < leastCandidateCount:
                                candidate[candidateCountCompetitor]["primary"].friendCount = leastCandidateCount
                                leastCandidateUser = candidateCountCompetitor
                    
                    # 现在最大的相似好友数且候选人最少的用户已经选出来了，把他送入guessMap1To2，
                    # 并把它从candiate删除，其他的选取次要候选者
                    
                    guessMap1To2[leastCandidateUser] = candidate[leastCandidateUser]["primary"].name
                    net2Selected[candidate[leastCandidateUser]["primary"].name] = 1
                    selectedCandidate[leastCandidateUser] = True
                    
                    print("candidate competition is over")
                    print("{} is the winner with score {}".format(leastCandidateUser, leastCandidateCount))
                    print("guessMap1To2: {}".format(guessMap1To2))
                    
                    # 从竞争列表中删除赢家
                    for i in range(len(competeList)):
                        if competeList[i] == leastCandidateUser:
                            del(competeList[i])
                            break
                    
                    print("rest competitor: {}".format(competeList))

                    for restUser in competeList:
                        # 如果没有其他候选人了，送入nextRound
                        # 否则将list中的候选人作为primary
                        if len(candidate[restUser]["list"]) == 0:
                            nextRound.append(restUser)
                            selectedCandidate[restUser] = True
                        else:
                            candidate[restUser]["primary"] = candidate[restUser]["list"].pop(0)
                # 不存在竞争用户，直接送入guessMap1To2
                else:
                    print("{} doesn't have competitor".format(user))
                    guessMap1To2[user] = candidate[user]["primary"].name
                    net2Selected[candidate[user]["primary"].name] = 1
                    selectedCandidate[user] = True
                    print("guessMap1To2: {}".format(guessMap1To2))

        # 将guessMap1To2与usingMap合并
        # 并清空guessMap
        for newUser in guessMap1To2:
            usingMap[newUser] = guessMap1To2[newUser]
            resultMap[newUser] = guessMap1To2[newUser]
        
        print("usingMap: {}".format(usingMap))
        print("resultMap: {}".format(resultMap))
        
        # 如果nextRound清空了，则退出循环
        # 否则将nextRound赋值给pending并清空自身
        if len(nextRound) == 0:
            break
        prevPending = pending.copy()
        pending = nextRound.copy()
        nextRound.clear()

        guessMap1To2.clear()
        
        # 清空candidate和selectedCandidate
        candidate.clear()
        selectedCandidate.clear()

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

def CheckMatchRate(guessMap, trueMap):
    matchResult = {}
    matchResult["hit"] = 0
    matchResult["total"] = len(trueMap)
    
    for trueUser in trueMap:
        if trueUser in guessMap:
            if guessMap[trueUser] == trueMap[trueUser]:
                matchResult["hit"] = matchResult["hit"] + 1
    
    matchResult["rate"] = matchResult["hit"] / matchResult["total"]
    
    return matchResult

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
    
    matchResult = CheckMatchRate(result, networkDataSet["trueNodeMapping"])
    
    MessageSystem.Info(repr(result))
    MessageSystem.Info(repr(matchResult))