from django.http import HttpResponse, FileResponse
import redis
import os
import json
from django.shortcuts import render
from . import settings

def index(request):
    return render(request, "index.html")

def base(request,user_id):
    '''
    参数：微博昵称，微博主页地址，微博博主性别，个人说明，标签，排名前九的微博内容，{关键字类别：出现次数}，
    最近半年微博热度(每个月所对应的微博点赞总数，{月份：数量，})，词云绝对地址
    :param request:
    :param user_name:
    :return:
    '''
    content = {'name':'胡歌'}
    return render(request, 'base.html', {'data':content})

def entertainment(request):
    '''
    参数：微博主人头像地址，微博主人昵称，微博个人说明 （20人）
    :param request:
    :return:
    '''
    content = {'name':[],'head_addr':[],'faction':[]}
    return render(request, 'entertainment.html', {'content':content})

def music(request):
    '''
        参数：微博主人头像地址，微博主人昵称，微博个人说明 ,微博主人uid（20人）
        :param request:
        :return:
    '''
    content = {'name': [], 'head_addr': [], 'faction': []}
    return render(request, 'music.html', {'content':content})

def sport(request):
    '''
        参数：微博主人头像地址，微博主人昵称，微博个人说明,微博主人uid （20人）
        :param request:
        :return:
    '''
    content = {'name': [], 'head_addr': [], 'faction': []}
    return render(request, 'sport.html', {'content':content})

def game(request):
    '''
        参数：主人头像地址，微博主人昵称，微博个人说明,微博主人uid （20人）
        :param request:
        :return:
    '''
    content = {'name': [], 'head_addr': [], 'faction': []}
    return render(request, 'game.html', {'content':content})


def active(request):
    '''
            参数：主人头像地址，微博主人昵称，微博个人说明 ,微博主人uid（20人）
            :param request:
            :return:
        '''
    content = {'name': [], 'head_addr': [], 'faction': []}
    return render(request, 'active.html', {'content': content})