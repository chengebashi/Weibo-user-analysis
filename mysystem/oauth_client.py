#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import json
import urllib.parse
from urllib.request import urlparse


class OAuthQQ:
    access_token = ''
    def __init__(self, client_id, client_key, redirect_uri):
        self.client_id = client_id
        self.client_key = client_key
        self.redirect_uri = redirect_uri

    def get_auth_url(self):
        """获取授权页面的网址"""
        params = {'client_id':self.client_id,
                  'response_type': 'code',
                  'redirect_uri': self.redirect_uri,
                  'scope': 'get_user_info',
                  'state': 1}
        url = 'https://graph.qq.com/oauth2.0/authorize?%s' % urllib.parse.urlencode(params)
        print(url, 'url')
        return url

    def get_access_token(self, code):
        """根据code获取access_token"""
        params = {'grant_type': 'authorization_code',
                  'client_id': self.client_id,
                  'client_secret': self.client_key,
                  'code': code,
                  'redirect_uri': self.redirect_uri}    # 回调地址
        url = 'https://graph.qq.com/oauth2.0/token?%s' % urllib.parse.urlencode(params)

        # 访问该网址，获取access_token
        response = urllib.request.urlopen(url).read()
        result = urllib.parse.parse_qs(response, True)
        print(result, 'result')	
        access_token = str(result.get(b'access_token'))
        print(access_token, type(access_token))
        access_token = access_token[3:-2]
        print(access_token,'access')
        self.access_token = access_token
        return access_token

    def get_open_id(self):
        """获取QQ的OpenID"""
        params = {'access_token': self.access_token}
        url = 'https://graph.qq.com/oauth2.0/me?%s' % urllib.parse.urlencode(params)

        response = urllib.request.urlopen(url).read()
        response = response.decode()
        print(response,'response')
        v_str = str(response[9:-3])
        print(v_str, type(v_str))
        v_json = json.loads(v_str)
        openid = v_json['openid']
        self.openid = openid
        return openid

    def get_qq_info(self):
        """获取QQ用户的资料信息"""
        params = {'access_token': self.access_token,
                  'oauth_consumer_key': self.client_id,
                  'openid': self.openid}
        url = 'https://graph.qq.com/user/get_user_info?%s' % urllib.parse.urlencode(params)

        response = urllib.request.urlopen(url).read().decode()
        return json.loads(response)
