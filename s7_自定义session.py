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


class BaseHandler(object):
    ## 继承这个类的类都会执行这个方法！
    def initialize(self):  ## 这是一个钩子函数
        ## 1、获取浏览器上用户的cookie，若有不操作
        ##   否则给用户生成随机
        ##   self.ssss = 'b' ## 继承的类都可以使用它
        from session import Session

        self.session = Session(self)  # Session对象

        super(BaseHandler, self).initialize()


class IndexHandler(BaseHandler, tornado.web.RequestHandler):
    # ## 在执行get或者post 之前都会执行这个方法
    # def initialize(self): ## 这是一个钩子函数
    #     print('I')
    #     pass

    def get(self):
        if self.session.get_value('is_login'):  ## 获得到成功

            self.write("Hello, world")
        else:
            print('---------------')
            self.redirect('/login')  ## 返回登录页面


class LoginHandler(BaseHandler, tornado.web.RequestHandler):

    def get(self):
        self.render('login.html')

    def post(self):
        v = self.get_argument('user')
        if v == 'root':  ## 登录成功
            self.session.set_value('is_login', True)
            v = self.session.get_value('is_login')
            print('v= ', v)
            print('okoko')
            self.redirect('/index')
        else:

            self.redirect('/login')  ## 返回当前页面


settings = {
    'static_path': 'static',  ## 静态文件
    'static_url_prefix': '/sss/',  ## url请求的前缀 -- html 只需要放前缀就可以了 :<link rel="stylesheet" href="/sss/commons.css">
    'template_path': 'templates',  ##模板路径
    # 'ui_methods': mt,  ## 注册模板函数，前端就可以用这个方法了
    # 'ui_modules': md,  ## 注册模板类，可以返回页面啥的
}

application = tornado.web.Application([
    (r"/index", IndexHandler),
    (r"/login", LoginHandler),
], **settings)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
