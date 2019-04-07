from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
     # marking/submit/projectid
    path('submit', views.upload_file, name='submit'),
]