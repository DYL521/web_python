# !/usr/bin/env python3
# -*- coding: utf-8 -*-  
"""  
 @desc:  
 @author: DYL  
 @contact: chng547835@163.com  
 @site: www.xxxx.com  
 @software: PyCharm  @since:python 3.5.2 on 2016/11/3.10:49  
 """
import uuid




class Session():
    '''
        handler：接收传递过来的self，就可以setcookie
    '''
    ## 保存session

    container = {

    }

    def __init__(self, handler):
        ## 1、获取浏览器上用户的cookie，若有不操作
        ##   否则给用户生成随机
        ##获取session
        nid = handler.get_cookie('session_id')
        print(Session.container)
        if nid:  ## 存在
            if nid in Session.container:  ## 是正确的nid
                pass
            else:  ## 不是正确的nid
                nid = str(uuid.uuid4())
                handler.set_cookie('session_id', nid)  ## 把session_id 给nid
                Session.container[nid] = {}  # 保存在本地

        else:  ## 不存在
            nid = str(uuid.uuid4())
            handler.set_cookie('session_id', nid)  ## 把session_id 给nid
            Session.container[nid] = {}  # 保存在本地

        ## nid 当前访问用户的随机字符串
        self.nid = nid
        ## 封装了所有用户信息
        self.handler = handler

    def set_value(self, key, value):
        print('key = ', key)
        print('value= ', value)
        ## 当前用户的随机字符串
        Session.container[self.nid][key] = value

    def get_value(self, key):
        ## 当前用户的随机字符串
        return Session.container[self.nid]. get(key)
