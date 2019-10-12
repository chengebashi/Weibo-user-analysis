from django.http import HttpResponse, FileResponse, HttpResponseRedirect, JsonResponse
import os,time
import json
from django.shortcuts import render, redirect
from . import settings
from . import get_info
from .oauth_client import OAuthQQ

def index(request):
    open_id = request.session.get('qq_id')
    logining_name = request.session.get('nickname')
    logining_head = request.session.get('figureurl')
    content = {'nick_name': logining_name, 'head_img': logining_head, 'login_id':open_id}
    return render(request, "index.html", content)

def login(request):
    oauth_qq = OAuthQQ(settings.QQ_APP_ID, settings.QQ_KEY, settings.QQ_RECALL_URL)
    # 获取 得到Authorization Code的地址
    url = oauth_qq.get_auth_url()
    # 重定向到授权页面
    return HttpResponseRedirect(url)

def logout(request):
    mark = request.GET.get('logout')
    content = {}
    if mark:
        request.session.flush()
        content['response'] = 0
    else:
        content['response'] = 1
    response =  JsonResponse({"response": content['response']})
    return response

def qq_check(request):
    """登录之后，会跳转到这里。需要判断code和state"""
    request_code = request.GET.get('code')
    oauth_qq = OAuthQQ(settings.QQ_APP_ID, settings.QQ_KEY, settings.QQ_RECALL_URL)
    access_token = oauth_qq.get_access_token(request_code)
    time.sleep(0.05)
    open_id = oauth_qq.get_open_id()
    #open_id入库
    infos = oauth_qq.get_qq_info()  # 获取用户信息
    request.session['qq_id'] = open_id
    qq_name = infos.get('nickname')
    get_info.save_user_id(open_id, qq_name)  #信息入库
    qq_head = infos.get('figureurl_1')
    request.session['nickname'] = qq_name
    request.session['figureurl'] = qq_head
    return redirect('/')

def base(request,user_id):
    '''
    参数：微博昵称，微博主页地址，微博博主性别，个人说明，标签，排名前九的微博内容，{关键字类别：出现次数}，
    最近半年微博热度(每个月所对应的微博点赞总数，{月份：数量，})，词云绝对地址
    :param request:
    :param user_name:
    :return:
    '''
    content = get_info.get_user_info(user_id)
    if content:
        path = content.get('picture_path')
        content['picture_path'] = path[-14:]
        content.pop('_id')
        open_id = request.session.get('qq_id')
        logining_name = request.session.get('nickname')
        logining_head = request.session.get('figureurl')
        if logining_name and logining_head:
            content['nick_name'] = logining_name
            content['head_img'] = logining_head
            content['login_id'] = open_id
        content['login_id'] = 'D2F055D24EF2720B7B5F889FDF510BA5'
        print(content, 'content')
        return render(request, 'base.html', {'data':content})

def entertainment(request):
    '''
    参数：微博主人头像地址，微博主人昵称，微博个人说明 ,微博主人uid（20人）,粉丝数
    :param request:
    :return:
    '''
    content = get_info.get_classify_info("movie_uid")
    open_id = request.session.get('qq_id')
    logining_name = request.session.get('nickname')
    logining_head = request.session.get('figureurl')
    if logining_name and logining_head:
        content['nick_name'] = logining_name
        content['head_img'] = logining_head
        content['login_id'] = open_id
    return render(request, 'entertainment.html', {'content':content})

def music(request):
    '''
        参数：微博主人头像地址，微博主人昵称，微博个人说明 ,微博主人uid（20人）,粉丝数
        :param request:
        :return:
    '''
    content = get_info.get_classify_info("music_uid")
    open_id = request.session.get('qq_id')
    logining_name = request.session.get('nickname')
    logining_head = request.session.get('figureurl')
    if logining_name and logining_head:
        content['nick_name'] = logining_name
        content['head_img'] = logining_head
        content['login_id'] = open_id
    return render(request, 'music.html', {'content':content})

def sport(request):
    '''
        参数：微博主人头像地址，微博主人昵称，微博个人说明,微博主人uid （20人）
        :param request:
        :return:
    '''
    content = get_info.get_classify_info("sports_uid")
    open_id = request.session.get('qq_id')
    logining_name = request.session.get('nickname')
    logining_head = request.session.get('figureurl')
    if logining_name and logining_head:
        content['nick_name'] = logining_name
        content['head_img'] = logining_head
        content['login_id'] = open_id
    return render(request, 'sport.html', {'content':content})

def game(request):
    '''
        参数：主人头像地址，微博主人昵称，微博个人说明,微博主人uid （20人）
        :param request:
        :return:
    '''
    content = get_info.get_classify_info("game_uid")
    open_id = request.session.get('qq_id')
    logining_name = request.session.get('nickname')
    logining_head = request.session.get('figureurl')
    if logining_name and logining_head:
        content['nick_name'] = logining_name
        content['head_img'] = logining_head
        content['login_id'] = open_id
    return render(request, 'game.html', {'content':content})


def active(request):
    '''
            参数：主人头像地址，微博主人昵称，微博个人说明 ,微博主人uid（20人）
            :param request:
            :return:
        '''
    content = get_info.get_classify_info("active_uid")
    open_id = request.session.get('qq_id')
    logining_name = request.session.get('nickname')
    logining_head = request.session.get('figureurl')
    if logining_name and logining_head:
        content['nick_name'] = logining_name
        content['head_img'] = logining_head
        content['login_id'] = open_id
    return render(request, 'active.html', {'content': content})

def self_like(request,open_id):
    '''
    传入参数：open_id,返回该用户收藏的所有明星
    :param request:
    :param open_id:
    :return:
    '''
    content = get_info.get_favorite_info(open_id)
    open_id = request.session.get('qq_id')
    logining_name = request.session.get('nickname')
    logining_head = request.session.get('figureurl')
    if logining_name and logining_head:
        content['nick_name'] = logining_name
        content['head_img'] = logining_head
        content['login_id'] = open_id
    return render(request, 'slef_like.html', {'content':content})


def user_search(request):
    '''
    用户输入所要搜索的名字，查询数据库中对应的uid,将对应uid的信息返回前端，
    接口：若查询到有结果{'result':'1','1':{微博主人头像地址，微博主人昵称，微博个人说明 ,微博主人uid,粉丝数 },'2':{...}...}
        若查询到无结果{’result‘:'0'}
    :param request:
    :param search_name:前端传递过来的查询的名字
    :return:返回接口信息
    '''
    search_name = request.POST.get("search")
    content = get_info.get_search_info(search_name)
    if content:
        content["result"] = 1
    else:
        content["result"] = 0
    open_id = request.session.get('qq_id')
    logining_name = request.session.get('nickname')
    logining_head = request.session.get('figureurl')
    if logining_name and logining_head:
        content['nick_name'] = logining_name
        content['head_img'] = logining_head
        content['login_id'] = open_id
    return render(request, 'search.html',{'content':content})


def collection(request):
    '''
    收藏喜欢的明星
    参数：open_id, weibo_name
    :param request:
    :return:
    '''
    open_id = request.GET.get('open_id')
    weibo_name = request.GET.get('weibo_name')
    #写入数据库
    ret = get_info.save_favorite_info(open_id, weibo_name)
    if ret:
        response = JsonResponse({"response": 0})
    else:
        response = JsonResponse({"response": 1})
    return response
