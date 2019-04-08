from django.shortcuts import render
from django.http import HttpResponse

from django.shortcuts import render
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .forms import UploadFileForm
from kms.models import *

import dropbox
import inspect, os
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP


print(inspect.getfile(inspect.currentframe())) # script filename (usually with path))
path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) # script directory
# Create your views here.

#0Asgs_ev8WAAAAAAAAAAC0-q3yhO457uLv2Po_XlSDe2wICZoevQ8CYabOgJr-Su


# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")

def upload_file(request):
    print(request.FILES)
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            #handle_uploaded_file(request.FILES['file'])
            print("valid form bayyyyyyyyby")

            client  = dropbox.Dropbox('0Asgs_ev8WAAAAAAAAAAC0-q3yhO457uLv2Po_XlSDe2wICZoevQ8CYabOgJr-Su')
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
    print(os.getcwd())

    
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

    session_key = get_random_bytes(16)

    print("\n\n-------- Session Key ---------\n")
    print(session_key.hex())
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
    publicKey = getUserPublicKey(userId)
    groupList = []
    for group in groups:
        groupList.append(group)
    context = {'groups':groupList,'publicKey':publicKey,'userId':userId}
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

def viewRequests(req):
    requests = Request.objects.all()
    requestList = []
    for request in requests:
        requestList.append(request)
    context = {"requests":requestList}
    return render(req, './admin.html', context)

def approveRequest(req,requestId):
    newRequest = getRequest(requestId)
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
    print("Querying Dictionary:")
    
    print("\n\n-------- Encrypted File Cypher Text ---------\n")
    print(request.POST.get('encryptedFile'))
    print("\n\n-------- Encrypted File Cypher Text ---------\n")
    if request.method == 'POST':
       
    #     #handle_uploaded_file(request.FILES['file'])
    #     print("valid form bayyyyyyyyby")

    #     client  = dropbox.Dropbox('0Asgs_ev8WAAAAAAAAAAC0-q3yhO457uLv2Po_XlSDe2wICZoevQ8CYabOgJr-Su')
    #     p = client.users_get_current_account()
    #     print(p.email)
    #     file = open("test.txt")

    
    #     bytes = request.FILES['myfile'].read()
    #     title = "/" +request.FILES['myfile'].name
    #     client.files_upload(bytes, title, mute = True)

        f= open(fileName,"w+")
        f.write(request.POST.get('encryptedFile'))
        f.close()

        
        client  = dropbox.Dropbox('0Asgs_ev8WAAAAAAAAAAC0-q3yhO457uLv2Po_XlSDe2wICZoevQ8CYabOgJr-Su')
        p = client.users_get_current_account()
        print(p.email)
        file = open("test.txt")

        f= open(fileName)
        bytes = f.read().encode()
        print(bytes)
        title = "/" +fileName
        client.files_upload(bytes, title, mute = True)

        
        return HttpResponse(request.POST.get('encryptedFile'))
    else:
        form = UploadFileForm()
    return render(request, './index.html', {'form': form})
