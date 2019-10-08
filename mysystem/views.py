from django.http import HttpResponse, FileResponse
import redis
import os
import json
from django.shortcuts import render
from . import settings

def index(request):
    return render(request, "index.html")

def huge(request):
    content = {'name':'胡歌'}
    return render(request, 'huge.html',{'data':content})

def entertainment(request):
    return render(request, 'entertainment.html')

def music(request):
    return render(request, 'music.html')

def sport(request):
    return render(request, 'sport.html')

def game(request):
    return render(request, 'game.html')