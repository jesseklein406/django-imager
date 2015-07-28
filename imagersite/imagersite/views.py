from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render


def index(request):
    context = {'name': 'bob'}
    return render(request, 'index.html', context)
