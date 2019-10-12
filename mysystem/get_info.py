#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@author: zzy
@file: get_info.py
@time: 2019/10/8 13:35
'''
from pymongo import MongoClient
import os
import json
import re
import time

conf = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"mongo_server.json")))

def get_user_info(id):
    '''
    函数功能：获取所需uid对应的信息，生成字典
    :param id: 微博uid
    :return:
    '''
    try:
        # 连接服务器
        host = conf["server_ip"]
        port = int(conf["server_port"])
        client = MongoClient(host, port)

        # 连接zzy数据库，账号密码认证
        sql_name = conf["mongo_name"]
        sql_user = conf["mongo_user"]
        sql_passwd = conf["mongo_passwd"]
        db = client[sql_name]
        db.authenticate(sql_user, sql_passwd)

        # 获取用户信息
        mycol = db[id]
        user_info = mycol.find({'微博昵称':re.compile('.*')})
        for i in user_info :
            biaoqian = list(i["高频词汇"].keys())
            i["标签"] = biaoqian[0:5] # 获取标签
            weibo_info = i

        # 获取用户6个月内,每个月的点赞总数
        wb_like = {} # 存放每月点赞数
        cur_month = int(time.strftime("%m",time.localtime(time.time())))
        cur_year = int(time.strftime('%Y',time.localtime(time.time())))
        last_year = str(cur_year - 1)
        if cur_month < 6:
            last_month = cur_month - 1
            if last_month <= 0:
                last_month = last_year + str(last_month + 12)
            else:
                last_month = last_year + '0' + str(last_month)
            two_month_ago = cur_month - 2
            if two_month_ago <=0:
                two_month_ago = last_year + str(two_month_ago + 12)
            else:
                two_month_ago = last_year + '0' + str(two_month_ago)
            three_month_ago = cur_month - 3
            if three_month_ago <= 0:
                three_month_ago = last_year + str(three_month_ago + 12)
            else:
                three_month_ago = last_year + '0' + str(three_month_ago)
            four_month_ago = cur_month -4
            if four_month_ago <=0:
                four_month_ago = last_year + str(four_month_ago + 12)
            else:
                four_month_ago = last_year + '0' + str(four_month_ago)
            five_month_ago = cur_month -5
            if five_month_ago <=0:
                five_month_ago = last_year + str(five_month_ago + 12)
            else:
                five_month_ago = last_year + '0' + str(five_month_ago)
        else:
            last_month = cur_month -1
            if last_month < 10:
                last_month = '0' + str(last_month)
            two_month_ago = cur_month -2
            if two_month_ago < 10:
                two_month_ago = '0' + str(two_month_ago)
            three_month_ago = cur_month -3
            if three_month_ago < 10:
                three_month_ago = '0' + str(three_month_ago)
            four_month_ago = cur_month -4
            if four_month_ago < 10:
                four_month_ago = '0' + str(four_month_ago)
            five_month_ago = cur_month -5
            if five_month_ago < 10:
                five_month_ago = '0' + str(five_month_ago)
            if cur_month < 10:
               cur_month = '0' + str(cur_month)
            else:
                cur_month = str(cur_month)

        # print(cur_month,last_month,two_month_ago,three_month_ago,four_month_ago,five_month_ago,last_year)
        # 获取当月点赞数
        cur_month_info = mycol.find({'发布时间':re.compile('^{}.*'.format(cur_month))})
        cur_month_like = 0
        for cur in cur_month_info:
            cur_month_like += int(cur["点赞数"])
            # print('当前点赞',cur_month)
        wb_like["cur_month_like"] = cur_month_like
        # 获取上月的点赞数
        last_month_info = mycol.find({'发布时间': re.compile('^{}.*'.format(last_month))})
        last_month_like = 0
        for last in last_month_info:
            last_month_like += int(last["点赞数"])
        wb_like["last_month_like"] = last_month_like
        # 上上月份点赞数

        two_month_ago_info = mycol.find({'发布时间':re.compile('^{}.*'.format(two_month_ago))})
        two_month_ago_like = 0
        for two in two_month_ago_info:
            two_month_ago_like += int(two["点赞数"])
        wb_like["two_month_ago_like"] = two_month_ago_like
        # 三个月前点赞数
        three_month_ago_info = mycol.find({'发布时间': re.compile('^{}.*'.format(three_month_ago))})
        three_month_ago_like = 0
        for three in three_month_ago_info:
            three_month_ago_like += int(three["点赞数"])
        wb_like["three_month_ago_like"] = three_month_ago_like
        # 四个月前点赞数
        four_month_ago_info = mycol.find({'发布时间':re.compile('^{}.*'.format(four_month_ago))})
        four_month_ago_like = 0
        for four in four_month_ago_info:
            four_month_ago_like += int(four["点赞数"])
        wb_like["four_month_ago_like"] = four_month_ago_like
        # 五个月前点赞数
        five_month_ago_info = mycol.find({'发布时间':re.compile('^{}.*'.format(five_month_ago))})
        five_month_ago_like = 0
        for five in five_month_ago_info:
            five_month_ago_like += int(five["点赞数"])
        wb_like["five_month_ago_like"] = five_month_ago_like
        weibo_info["每月点赞数"] = wb_like

        # 获取点赞数前十的微博内容
        top_10 = mycol.find({}, { '_id': 0,"微博内容": 1,'微博地址':1}).sort("点赞数",-1).limit(11)
        top_10 = [i for i in top_10]
        weibo_info["点赞前十微博内容"] = dict(zip([i for i in range(1,10)],[j for j in top_10]))
        # print(weibo_info)
        # client.close()
    except Exception as e:
        print(e)
    return weibo_info

def get_classify_info(which_col):
    '''
    函数功能：获取各个板块的用户信息，生成字典返回
    :return: 返回字典格式的信息
    '''
    try:
        # 连接服务器
        host = conf["server_ip"]
        port = int(conf["server_port"])
        client = MongoClient(host, port)

        # 连接zzy数据库，账号密码认证
        sql_name = conf["mongo_name"]
        sql_user = conf["mongo_user"]
        sql_passwd = conf["mongo_passwd"]
        db = client[sql_name]
        db.authenticate(sql_user, sql_passwd)



        # 获取对应分类的uid列表
        mycol = db[which_col]
        uids = mycol.find()
        uid_list = [i["uid"] for i in uids]

        # 获取每个uid对应的信息
        each_info = {}
        cnt = 1
        for uid in uid_list:
            mycol = db[uid]
            one_info = mycol.find({}, {"_id": 0, "微博昵称": 1, "微博头像地址": 1, "微博说明": 1,
                                       "粉丝数": 1})
            # print(one_info)
            for i in one_info:
                if i:
                    i['uid'] = uid
                    # print(i)
                    if not i.get("微博说明"):
                        i["微博说明"] = "此人很懒，什么也没有留下。。。。"
                    each_info[str(cnt)] = i
                    cnt += 1
        # print('each_info', each_info)
    except Exception as e:
        print(e)
    return each_info

def get_search_info(search_name):
    '''
    函数功能：根据用户输入的用户名，查找出所有和此用户名相近的uid信息，以
    {'1':{微博主人头像地址，微博主人昵称，微博个人说明 ,微博主人uid,粉丝数 },'2':{...}...}
    :param search_name:
    :return:
    '''

    try:
        # 连接服务器
        host = conf["server_ip"]
        port = int(conf["server_port"])
        client = MongoClient(host, port)

        # 连接zzy数据库，账号密码认证
        sql_name = conf["mongo_name"]
        sql_user = conf["mongo_user"]
        sql_passwd = conf["mongo_passwd"]
        db = client[sql_name]
        db.authenticate(sql_user, sql_passwd)



        # 先从电影数据库中查找出对应的uid加入列表
        mycol = db["movie_uid"]
        match_uids = []
        movie_set_info = mycol.find({"name":re.compile("{}".format(search_name))})
        # print(movie_set_info)
        for movie_info in movie_set_info:
            # print(movie_info,type(movie_info))
            match_uids.append(movie_info["uid"])
        # print(match_uids)


        # 获取每个uid对应的信息
        each_info = {}
        cnt = 1
        for uid in match_uids:
            mycol = db[uid]
            one_info = mycol.find({}, {"_id": 0, "微博昵称": 1, "微博头像地址": 1, "微博说明": 1,
                                       "粉丝数": 1})
            # print(one_info)
            for i in one_info:
                if i:
                    i['uid'] = uid
                    # print(i)
                    if not i.get("微博说明"):
                        i["微博说明"] = "此人很懒，什么也没有留下。。。。"
                    each_info[str(cnt)] = i
                    cnt += 1
        # print('each_info', each_info)
    except Exception as e:
        print("异常",e)
    return each_info


def save_favorite_info(open_id,name):
    '''
    函数功能：保存用户收藏信息
     格式：{
            open_id: *,
            match_info:{
                    uid:{微博主人头像地址:*，微博主人昵称:*，微博个人说明:* ,uid:*,粉丝数:*}
                    uid:{}
                    }
            }
    :param open_id:用户open_id
    :param uid:博主uid
    :return: 保存成功，返回true
    '''
    try:
        # 连接服务器
        host = conf["server_ip"]
        port = int(conf["server_port"])
        client = MongoClient(host, port)

        # 连接zzy数据库，账号密码认证
        sql_name = conf["mongo_name"]
        sql_user = conf["mongo_user"]
        sql_passwd = conf["mongo_passwd"]
        db = client[sql_name]
        db.authenticate(sql_user, sql_passwd)
        # 根据name查询出对应的uid
        sports_uid = db["sports_uid"]
        sports = sports_uid.find_one({"name":name})
        if sports:
            uid = sports.get("uid")

        music_uid = db["music_uid"]
        music = music_uid.find_one({"name":name})
        if music:
            uid = music.get("uid")

        game_uid = db["music_uid"]
        game = game_uid.find_one({"name":name})
        if game:
            uid = game.get("uid")

        active_uid = db["active_uid"]
        active = active_uid.find_one({"name":name})
        if active:
            uid = active.get("uid")

        movie_uid = db["movie_uid"]
        movie = movie_uid.find_one({"name":name})
        if movie:
            uid = movie.get("uid")

        # 查询出用户收藏uid的信息
        print("uid",uid,type(uid))
        mycol = db[uid]
        favorite_info = mycol.find({},{"_id":0,"微博昵称":1,"微博头像地址":1,"微博说明":1,"粉丝数":1})
        # favorite_info = mycol.find({"微博昵称":re.compile(".*")})
        for i in favorite_info:

            if i:
                i["uid"] = uid
                print("i", i)
                data = {}
                data[uid] = i
                data["open_id"] = open_id

                # 将信息保存至favorite_uid表
                mycol = db["favorite_uid"]
                favorite_user = mycol.find_one({"open_id":open_id})
                print("favorite_user",favorite_user)
                if favorite_user:

                    mycol.update_one({"open_id":open_id},{"$set":{uid:data[uid]}})
                else:
                    mycol.insert_one(data)
                return True
    except Exception as e:
        print("异常",e)

def get_favorite_info(open_id):
    '''
    函数功能：查询对应open_id收藏的博客信息
    格式：{
            ‘0’:{微博主人头像地址:*，微博主人昵称:*，微博个人说明:* ,uid:*,粉丝数:*}
            ‘1’:{}
        }
    :return:返回数据格式：
    '''
    try:
        # 连接服务器
        host = conf["server_ip"]
        port = int(conf["server_port"])
        client = MongoClient(host, port)

        # 连接zzy数据库，账号密码认证
        sql_name = conf["mongo_name"]
        sql_user = conf["mongo_user"]
        sql_passwd = conf["mongo_passwd"]
        db = client[sql_name]
        db.authenticate(sql_user, sql_passwd)
        mycol = db["favorite_uid"] # 用户收藏表

        favorite_info = mycol.find_one({"open_id":open_id})
        # print(favorite_info)
        if favorite_info:
            favorite_info.pop("_id")
            favorite_info.pop("open_id")
            favorite_info = favorite_info.values()
            # print(favorite_info,type(favorite_info))
            favorite_info_list = []
            for i in favorite_info:
                favorite_info_list.append(i)
            # print("favorite_info_list",favorite_info_list)
            data = {}
            for i in range(len(favorite_info_list)):
                data["{}".format(i)] = favorite_info_list[i]
        # print(data)
            return data
        else:
            return {}
    except Exception as e:
            print("异常",e)




def save_user_id(open_id,username):
    '''
    函数功能：将用户的open_id，和username存入user_id表中
    格式：{
        open_id:*,
        username:*
    }
    :param open_id:用户登录秘钥值
    :param username:用户登录昵称
    :return:
    '''
    try:
        # 连接服务器
        host = conf["server_ip"]
        port = int(conf["server_port"])
        client = MongoClient(host, port)

        # 连接zzy数据库，账号密码认证
        sql_name = conf["mongo_name"]
        sql_user = conf["mongo_user"]
        sql_passwd = conf["mongo_passwd"]
        db = client[sql_name]
        db.authenticate(sql_user, sql_passwd)
        mycol = db["user_id"] # 用户信息集合

        user_info = {}
        user_info["open_id"] = open_id
        user_info["username"] = username
        user_id = mycol.find_one({}, {"open_id":re.compile("{}".format(open_id))})
        if user_id:
            mycol.update_one({"username":username},{"$set":user_info})
        else:
            mycol.insert_one(user_info)
        return True
    except Exception as e:
        print("异常",e)


# if __name__ == '__main__':
#     # id = '1192329374'
#     # get_user_info(id)
#     get_classify_info("movie_uid")