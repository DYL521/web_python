#!/usr/bin/env python3  
# -*- coding: utf-8 -*-  
"""  
 @desc:  
 @author: DYL
 @contact: chng547835@163.com  
 @site: www.xxxx.com  
 @software: PyCharm  @since:python 3.5.2 on 2016/11/3.10:49  
 """
# !/usr/bin/env python
# -*- coding:utf-8 -*-
from bottle import template, Bottle, static_file, request, redirect
from bottle import jinja2_template ## 使用jinjia2的模板引擎 --- django的模板引擎类似于jianjia2
###
import bottle

'''
Bottle :只有1个文件
'''
## 3、模板配置路径配置
bottle.TEMPLATE_PATH.append('./templates/')

root = Bottle()


## 1、装饰器-- 实现路由系统
@root.route('/hello/')
def index():
    # return "Hello World"
    # return templates('<b>Hello {{name}}</b>!', name="Alex")
    return template('index.html')


# 支持提交的方式
@root.route('/login/', method=['POST', 'GET'])
def login():
    print(request.method)

    if request.method == 'GET':
        return template('login.html')
    else:
        ## 表单数据存放的位置 -- request.forms
        v = request.forms  ## GET和POST都有
        v = request.body  ## post发送的请求-- 在请求体里面
        v = request.query  ## get 发送的请求
        ## 所有的框架
        u = request.forms.get('user')
        p = request.forms.get('passwd')
        print(u, p)

        return redirect('/index/')  ## 页面跳转


@root.route('/index/', method=['POST', 'GET'])
def index():
    user_list = [
        {'id': 1, 'name': 'root', 'age': 18},
        {'id': 1, 'name': 'root', 'age': 18},
        {'id': 1, 'name': 'root', 'age': 18},
        {'id': 1, 'name': 'root', 'age': 18},
        {'id': 1, 'name': 'root', 'age': 18},
        {'id': 1, 'name': 'root', 'age': 18},
    ]

    return template('index.html', user_list=user_list)


##2、 静态文件路由
@root.route('/static/<path:path>')
def callback(path):
    return static_file(path, root='static')


root.run(host='localhost', port=8080)

'''
    web框架路由系统主要有三种：
    1、django ---- url 对应一个函数
    2、flask、bottle-- 装饰器
    3、反射实现路由系统-- 没有函数
        url=[
			  ('/?P<controller>\w+/?P<action>\w+/')
			]
'''
