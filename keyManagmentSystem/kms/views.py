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

import dropbox
import inspect, os
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