# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadDataset


def handle_uploaded_file(f):
    print(type(f))
    print(f)


def upload_file(request):
    print('TOTO')
    if request.method == 'POST':
        print('POST')
        form = UploadDataset(request.POST, request.FILES)
        if form.is_valid():
            print('HELLO')
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success/url/')
        else:
            print('NOT HELLO')
    else:
        form = UploadDataset()
    return render(request, 'upload.html', {'form': form})


