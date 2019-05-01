from django.db import models
from django import forms
from Crypto.Random import get_random_bytes

# Create your models here.
class GroupMembers(models.Model):
    publicKey = models.CharField(max_length=3000)
    groupID = models.CharField(max_length=500)
    groupName = models.CharField(max_length=500)

class Group(models.Model):
    groupID = models.AutoField(primary_key=True)
    groupName = models.CharField(max_length=500)
    sessionKey = models.CharField(max_length=500)


class User(models.Model):
    publicKey = models.CharField(max_length=3000)
    userId = models.AutoField(primary_key=True)

    def print(self):
        print("User : "+str(self.userId))
        print("")
        print(self.publicKey)

class Request(models.Model):
    publicKey = models.CharField(max_length=3000)
    groupID = models.CharField(max_length=500)
    groupName = models.CharField(max_length=500)
    requestId = models.AutoField(primary_key=True)


class Content(models.Model):
    fileName = models.CharField(max_length=3000)
    fileId = models.AutoField(primary_key=True)
    groupId = models.IntegerField()





#------ Group API ------------



def isInGroup(groupId,userId):
    set = GroupMembers.objects.filter(groupID = groupId)
    publicKey = getUserPublicKey(userId)
    for member in set:
        if(member.publicKey == publicKey):
            return True
    return False



def getGroup(groupID):
    set = Group.objects.filter(groupID = groupID)
    for i in set:
        return i
    return None

def getSessionKey(groupID):
    set = Group.objects.filter(groupID = groupID)
    for group in set:
        return group.sessionKey

def getGroupName(groupId):
    set = Group.objects.filter(groupID = groupId)
    resultSet = []
    for i in set:
        resultSet.append(i)
    return resultSet[0].groupName

def printGroups():
    set = Group.objects.all()
    for group in set:
        print("Group ID : "+str(group.groupID))
        print("Name :"+group.groupName)
        print(group.sessionKey)
        print("\n")

def makeGroup(name):
    g = Group()
    session_key = get_random_bytes(16).hex()
    g.sessionKey = session_key
    g.groupName = name
    g.save()


def deleteGroup(groupID):
    set = GroupMembers.objects.filter(groupID = groupID)
    for member in set:
        member.delete()
    groups = Group.objects.filter(groupID = groupID)
    for group in groups:
        group.delete()

#------ Group API ------------
#------ Group  Member API ------------


def printGroupMembers(groupId):
    set = GroupMembers.objects.filter(groupID = groupId)
    i=0
    for member in set:
        user = getUser(member.publicKey)
        i = i+1
        print("Member : "+str(i))
        print("userID :"+str(user.userId))
        print("pubKey :" + str(user.publicKey))



def removeUserFromGroup(groupId, userId):
    publicKey = getUserPublicKey(userId)
    set = GroupMembers.objects.filter(groupID = groupId)
    for i in set:
        user = getUser(i.publicKey)
        if user.userId == userId:
            i.delete()


#------ Group  Member sAPI ------------  
#------ User API ------------

def getUserPublicKey(userId):
    uSet = User.objects.filter(userId = userId)
    listUsers = []
    for i in uSet:
        listUsers.append(i)
    return listUsers[0].publicKey


def deleteUsers():
    set = User.objects.all()
    for user in set:
        user.delete() 

def printAllUsers():
    set = User.objects.all()
    for user in set:
        user.print()

def getUser(publicKey):
    set = User.objects.all()
    
    for i in set:
        if(i.publicKey == publicKey):
            return i
    return None


def getUserGroups(userId):
    pk = getUserPublicKey(userId)
    set = GroupMembers.objects.filter(publicKey = pk)
    groupList = []
    for group in set:
        mGroup = getGroup(group.groupID)
        groupList.append(mGroup)
    return groupList



def userExists(publicKey):
    userSet = User.objects.filter(publicKey = publicKey)
    userList = []
    for i in userSet:
        userList.append(i)
    user = userList[0]
    if(user==None):
        return False
    return True


def getGroups(publicKey):
    userSet = User.objects.filter(publicKey = publicKey)
    userList = []
    for i in userSet:
        userList.append(i)
    user = userList[0]
    
    set = Group.objects.get()
    groupList= []
    for group in set:
        if(group.publicKey == user.publicKey):
            groupList.append(group)

#------ User API ------------

    



def getContent(resourceId):
    set = Content.objects.filter(fileId = resourceId)
    for el in set:
        return el

def getContents(groupId):
    set = Content.objects.filter(groupId = groupId)
    returnSet = []
    for content in set:
        returnSet.append(content)
    return returnSet


def getRequest(requestId):
    set = Request.objects.filter(requestId = requestId)
    returnSet = []
    for el in set:
        returnSet.append(el)
    return returnSet[0]



#------ Request API ------------

def removeRequest(requestId):
    set = Request.objects.filter(requestId = requestId)
    returnSet = []
    for el in set:
        el.delete()