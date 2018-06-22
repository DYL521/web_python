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
from tornado import gen
from tornado.concurrent import Future

##tornado 异步io模块，发送请求，因为http请求压根不占cpu，可以执行其他的操作
class MainHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        from tornado import httpclient
        http = httpclient.AsyncHTTPClient()
        yield http.fetch('http://www.google.com',self.done)

    def done(self):
        self.write('Main')
        self.finish()
'''
    如果先访问/main ,再访问/index,则会等待main执行完成，才会执行index
'''
class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


application = tornado.web.Application([
    (r"/main", MainHandler),
    (r"/index", IndexHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()








