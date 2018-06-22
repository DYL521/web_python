#!/usr/bin/env python3  
# -*- coding: utf-8 -*-  
"""  
 @desc:  
 @author: DYL  
 @contact: chng547835@163.com  
 @site: www.xxxx.com  
 @software: PyCharm  @since:python 3.5.2 on 2016/11/3.10:49  
 """

import tornado.ioloop
import tornado.web


## 处理函数没有返回值
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")  ##


class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        # 6、额外的响应内容
        # self.get_cookie('k1','v1')
        # self.set_cookie('k1','v1')

        ## 5、得到请求参数
        v = self.get_argument('p')  ## get post都在这里
        print(v)

        ##4、返回页面--字符串（或者页面字符串） + 模板引擎--与django有点不同
        # self.write("Hello, world2") ## 返回字符串
        # self.render('login.html',k1='v1',k2=v2) ## 返回页面字符串
        self.render('login.html', **{'k1': 'v1', 'k2': [1, 2, 3, 4, 5], 'k3': {'name': 'root', 'age': 18}})  ## 返回页面字符串
        ## 7、重定向
        # self.redirect('/index/')

    def post(self):
        v = self.get_argument('user')
        print(v)
        self.redirect('http://www.baidu.com')
'''
模板里面自定制方法：simaple_tag 和filter
在 tornado 叫：
'''

import uimodules as md
import uimethods as mt
## 8、配置文件
settings = {
    'static_path':'static', ## 静态文件
    'static_url_prefix':'/sss/', ## url请求的前缀 -- html 只需要放前缀就可以了 :<link rel="stylesheet" href="/sss/commons.css">
    'template_path':'templates', ##模板路径
    'ui_methods': mt,  ## 注册模板函数，前端就可以用这个方法了
    'ui_modules': md,  ## 注册模板类，可以返回页面啥的
}

## 1、路由系统，生成路由规则
application = tornado.web.Application([
    (r"/index", MainHandler),
    (r"/login", LoginHandler),
],**settings) ## 传入配置文件

if __name__ == "__main__":
    ## 2、创建socket对象,将socket对象添加到select或者epoll中
    application.listen(8888)
    ## 3、将select或者epoll开始死循环 while True: 监听文件句柄
    tornado.ioloop.IOLoop.instance().start()

    '''
        client第一次来访问，把FD（文件句柄）添加到epoll或者select中，socket监听到-- 匹配路由--->返回数据
    '''
