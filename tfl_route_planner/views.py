from django.shortcuts import render


def index(request):
    return render(request, 'index.html', {})


def licences(request):
    return render(request, 'licences.html')
