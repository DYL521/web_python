# !/usr/bin/env python3
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
import time


class MainHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        future = Future()
        ## 设置5s时间，特殊的形式等待5s-- 这5秒处理别的请求

        tornado.ioloop.IOLoop.current().add_timeout(time.time() + 5, self.doing)

        yield future ## 监听future

    ## 5s以后自动执行方法doing --- 在等待的5s中，可以访问/index,直接返回了结果
    def doing(self, *args, **kwargs):
        self.write('async===main')
        self.finish()


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
