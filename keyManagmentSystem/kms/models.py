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

def printGroups():
    set = Group.objects.all()
    for group in set:
        print("Name :"+group.name)
        print(group.sessionKey)

def makeGroup(name):
    g = Group()
    session_key = get_random_bytes(16)
    g.sessionKey = get_random_bytes(16)
    g.groupName = name
    g.save()

class User(models.Model):
    publicKey = models.CharField(max_length=3000)
    userId = models.AutoField(primary_key=True)

    def print(self):
        print("User : "+str(self.userId))
        print("")
        print(self.publicKey)

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
    return User.objects.filter(publicKey = publicKey)

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

def userExists(publicKey):
    userSet = User.objects.filter(publicKey = publicKey)
    userList = []
    for i in userSet:
        userList.append(i)
    user = userList[0]
    if(user==None):
        return False
    return True


class File(models.Model):
    title = models.CharField(max_length=500)
    groupID = models.CharField(max_length=500)
    

class Request(models.Model):
    publicKey = models.CharField(max_length=3000)
    groupID = models.CharField(max_length=500)
    groupName = models.CharField(max_length=500)

class Content(models.Model):
    fileName = models.CharField(max_length=3000)
    fileId = models.AutoField(primary_key=True)
    groupId = models.IntegerField()

def getContents(groupId):
    set = Content.objects.filter(groupId = groupId)
    returnSet = []
    for content in set:
        returnSet.append(content)
    return returnSet