from django.shortcuts import render
from django.http import HttpResponse

from django.shortcuts import render
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
# from django.forms import UploadFileForm
from kms.models import *

import dropbox
import inspect, os
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import json

from django.conf import settings


print(inspect.getfile(inspect.currentframe())) # script filename (usually with path))
path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) # script directory
# Create your views here.



# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")

def upload_file(request):
    print(request.FILES)
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
         
            #handle_uploaded_file(request.FILES['file']
            client  = dropbox.Dropbox(settings.DROPBOX_API_KEY);
            p = client.users_get_current_account()
            print(p.email)
            file = open("test.txt")

         
            bytes = request.FILES['myfile'].read()
            title = "/" +request.FILES['myfile'].name
            client.files_upload(bytes, title, mute = True)


            return HttpResponse("Successful file upload!")
    else:
        form = UploadFileForm()
    return render(request, './index.html', {'form': form})




def handle_uploaded_file(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def index(request):
    context = {}
    return render(request, './index.html',context)

def acceptKey(request):
    print("incoming post request")

    
    #request is like a dictionary which we can query using .get()
    #.get the file that the client submitted 
    file = request.FILES.get('key')
    inputKey = file.readlines()
    # read in blob from client post request and parse public RSA key as a python RSA key 
    
    keyPem = ""
    for line in inputKey:
        keyPem = keyPem+str(line.decode("utf-8"))
     
    print(keyPem)
   
    print("client key parsed")
    existingUser = getUser(keyPem)
    print(existingUser)
    if(existingUser == None):
        print("Making New User")
        u = User()
        u.publicKey = keyPem
        u.save()

    clientPubKey = RSA.import_key(keyPem)

    user = getUser(keyPem)
    data = user.userId
    response = HttpResponse(data,content_type='application/json')
    
    response.status_code = 200
    return HttpResponse(response)

def newUser(request):
    print("adding a new user..")
  
    #request is like a dictionary which we can query using .get()
    #.get the file that the client submitted 
    file = request.FILES.get('key')
    inputKey = file.readlines()
    # read in blob from client post request and parse public RSA key as a python RSA key 
    
    keyPem = ""
    for line in inputKey:
        keyPem = keyPem+str(line.decode("utf-8"))
     
    u = User()
    u.publicKey = keyPem
    u.save()
    print("new user added!")
   
   
    data = u.userId
    response = HttpResponse(data,content_type='application/json')
    
    response.status_code = 200
    return HttpResponse(response)





def getGroups(request,userId):
    groups = Group.objects.all()
    #will make fancier adding styles for your groups
    #specificGroups= getGroups(publicKey)
    specificGroups= getUserGroups(userId)
    
    publicKey = getUserPublicKey(userId)
    memberList = []
    groupList = []
    contained = []
    for group in groups:
        groupList.append(group)
        for spec in specificGroups:
            if(spec.groupName == group.groupName):
                contained.append(True)
        contained.append(False)
    print("contained")
    print(contained)
    context = {'groups':groupList,'publicKey':publicKey,'userId':userId,'contained':contained, 'specificGroups':specificGroups}
    return render(request, './dashboard.html', context)


def fetchGroupInfo(request,userId,groupId):
    files = getContents(groupId)
    publicKey = getUserPublicKey(userId)
    groupMember = isInGroup(groupId,userId)
    print("Group ID = ")
    print(groupId)
    context = {'files':files,'publicKey':publicKey,'userId':userId,'groupMember':groupMember,"groupName":getGroupName(groupId),"groupID":groupId}
    return render(request, './group.html', context)


def createRequest(request,userId,groupId):
    publicKey = getUserPublicKey(userId)
    groupName = getGroupName(groupId)
    r = Request()
    r.publicKey = publicKey
    r.groupID = groupId
    r.groupName = groupName
    r.save()
    print("Request created")
    data = "success"
    response = HttpResponse(data,content_type='application/json')
    
    response.status_code = 200
    return HttpResponse(response)

@login_required
def viewRequests(req):
    requests = Request.objects.all()
    requestList = []
    for request in requests:
        requestList.append(request)
    context = {"requests":requestList}
    return render(req, './admin.html', context)

def approveRequest(req,requestId):
    newRequest = getRequest(requestId)
    userPK = newRequest.publicKey
    user = getUser(userPK)
    invalidRequest = isInGroup(newRequest.groupID,user.userId)
    if(invalidRequest == False):
        member = GroupMembers()
        member.publicKey = newRequest.publicKey
        member.groupID = newRequest.groupID
        member.groupName = newRequest.groupName
        member.save()
    newRequest.delete()
    data = "success"
    response = HttpResponse(data,content_type='application/json')
    response.status_code = 200
    return HttpResponse(response)


def returnSessionKey(request,userId,groupId):
    print("incoming key request")
    
   #session_key = bytes(getSessionKey(groupId))
    session_key = bytes(bytearray.fromhex(getSessionKey(groupId)))
    print(session_key)
    #request is like a dictionary which we can query using .get()
    #.get the file that the client submitted 
    file = request.FILES.get('key')
    inputKey = file.readlines()
    # read in blob from client post request and parse public RSA key as a python RSA key 
    
    keyPem = ""
    for line in inputKey:
        keyPem = keyPem+str(line.decode("utf-8"))
     
    print(keyPem)
   
    print("client key parsed")
    
    clientPubKey = RSA.import_key(keyPem)

    

    print("\n\n-------- Session Key ---------\n")
    print(str(session_key, "unicode-escape"))
    print("\n-------- Session Key ---------\n\n")

    # Encrypt the session key with the public RSA key
    cipher_rsa = PKCS1_OAEP.new(clientPubKey)
    secretSession = cipher_rsa.encrypt(session_key)

    print("\n\n-------- Encrypted Secret ---------\n")
    print(secretSession.hex())
    print("\n-------- Encrypted Secret ---------\n\n")
    data = secretSession.hex()
    response = HttpResponse(data,content_type='application/json')
    
    response.status_code = 200
    return HttpResponse(response)


def encryptedFileUpload(request,userId,groupId,fileName):
 
    
    # check incoming request is indeed a POST request 
    if request.method == 'POST':
        # print out the encrypted cypher text (for debugging)
        print("\n\n-------- Encrypted File Cypher Text ---------\n")
        print(request.POST.get('encryptedFile'))
        print("\n\n-------- Encrypted File Cypher Text ---------\n")
        
        # files will be stored on dropbox as .txt files containing the cypher text so it is 
        # necessary to strip the actual extension off although this is retained in DB for 
        # locating the original file on the drive
        fileExtensionIndex = fileName.find('.')
        title = fileName[:fileExtensionIndex]+".txt"
        # open a text file in the python server and write the encrypted text to it. save that file (.close())
        f= open(title,"w+")
        f.write(request.POST.get('encryptedFile'))
        f.close()
        # set up dropbox API authentication credentials 
        client  = dropbox.Dropbox(settings.DROPBOX_API_KEY)
        p = client.users_get_current_account()
        # open file , read the bytes from that file and prepare to send to dropbox
        f= open(title)
        bytes = f.read().encode()
        title = "/" +fileName[:fileExtensionIndex]+".txt"
        #command to upload files to drop box
        client.files_upload(bytes, title, mute = True)
        # keep a record of the file submission and what group it was for in the DB
        c = Content()
        c.groupId = groupId
        c.fileName = fileName
        c.save()
        # return successful response to the client
        response = HttpResponse(data,content_type='application/json')
        response.status_code = 200
        return HttpResponse(response)   
    else:
        form = UploadFileForm()
    return render(request, './index.html', {})


def downloadResource(request,userId,groupId,resourceId):

    c = getContent(resourceId)
    fileName = c.fileName
    fileExtensionIndex = fileName.find('.')
    title = fileName[:fileExtensionIndex]+".txt"

    

    client  = dropbox.Dropbox(settings.DROPBOX_API_KEY)
    p = client.users_get_current_account()
    print(p.email)
    metadata, res  = client.files_download('/'+title)
    print(metadata)
    print(res)
    data = b""
    for i in res:
        data  = data + i
    print(data)
    retObj = {'data':data}

    response = HttpResponse(data.decode("utf-8"),content_type='application/json')
    response.status_code = 200
    return HttpResponse(response)


def downloadEncryptedResource(request,userId,groupId,resourceId):
    # read the entry about that resouce that I had in the SQLite DB
    # This will allow me to fetch the correct resource from dropbox.com
    c = getContent(resourceId)
    # get specific info about the file from the database entry
    fileName = c.fileName
    fileExtensionIndex = fileName.find('.')
    title = fileName[:fileExtensionIndex]+".txt"
    # configure dropbox credentials
    client  = dropbox.Dropbox(settings.DROPBOX_API_KEY)
    p = client.users_get_current_account()
    # download the encrypted file off dropbox
    metadata, res  = client.files_download('/'+title)
    #write the data to a byte string from the dropbox response object
    data = b""
    for i in res:
        data  = data + i
    # return the data with a 200 success code
    retObj = {'data':data}
    response = HttpResponse(data.decode("utf-8"),content_type='application/json')
    response.status_code = 200
    return HttpResponse(response)