from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
     # marking/submit/projectid
    path('submit', views.upload_file, name='submit'),
    path('pubkey/', views.acceptKey, name='submit'),
    path('addUser/', views.newUser, name='submit'),
    path('groups/<userId>/', views.getGroups, name='submit'),
    path('groups/<userId>/getGroup/<groupId>', views.fetchGroupInfo, name='submit'),
    path('groups/<userId>/getGroup/<groupId>/uploadKey/', views.returnSessionKey, name='submit'),
    path('groups/<userId>/getGroup/<groupId>/encryptedFileUpload/<fileName>',views.encryptedFileUpload,name ='submit'),
    path('groups/<userId>/getGroup/<groupId>/download/<resourceId>',views.downloadResource,name ='submit'),
    path('groups/<userId>/requestAccess/<groupId>', views.createRequest, name='submit'),
    path('admin', views.viewRequests, name='submit'),
    path('approve/<requestId>', views.approveRequest, name='submit'),
    
    
]