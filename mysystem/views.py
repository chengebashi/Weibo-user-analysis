from django.http import HttpResponse, FileResponse
import redis
import os
from django.shortcuts import render
from . import settings

def index(request):
    return render(request, "index.html")