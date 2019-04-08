from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
     # marking/submit/projectid
    path('submit', views.upload_file, name='submit'),
    path('pubkey/', views.acceptKey, name='submit'),
    path('addUser/', views.newUser, name='submit'),
    path('groups/<userId>/', views.getGroups, name='submit'),
    path('groups/<userId>/getGroup/<groupId>', views.getGroups, name='submit'),
]