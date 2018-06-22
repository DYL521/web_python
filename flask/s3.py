#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @desc:
 @author: DYL
 @contact: chng547835@163.com
 @site: www.xxxx.com
 @software: PyCharm  @since:python 3.5.2 on 2016/11/3.10:49
 """

from flask import Flask, render_template, request, \
    make_response, redirect, url_for, session

app = Flask(__name__)


@app.route("/index/")
def hello():
    print('.....')
    return 'okoko'


## 执行自己定义的方法-- flask就不会进入到自带的函数内部
def my_wsgi_app(environ, start_response):
    print('my_wsgi_app')
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [bytes('<h1>Hello, web!</h1>')]

# 可以执行我们想要的方法--- 定制其他的功能
class Foo:
    def __init__(self,w):
        self.w = w

    def __call__(self, environ, start_response):
        ### 自己的行为1
        obj =  self.w(environ,start_response)
        ### 自己的行为2
        return obj




if __name__ == "__main__":
    # app.wsgi_app()  ## 请求入口 --- wsgi先执行！---里面加载中间件

    ##app.wsgi_app = my_wsgi_app  ## 执行自己定义的函数

    '''
        创建一个新的对象，把当前的app.wsgi_app 传入，作为本身的一个成员，保存起来
        执行完__call__方法后，返回该成员并传递相应的参数
        整个过程中，不会影响任何Flask的执行！！
    '''
    app.wsgi_app = Foo(app.wsgi_app)
    app.run()

'''
    Meaasge :基于Session实现的。。取一次就删除掉-- 页面的错误提示
'''
