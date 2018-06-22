#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @desc:
 @author: DYL
 @contact: chng547835@163.com
 @site: www.xxxx.com
 @software: PyCharm  @since:python 3.5.2 on 2016/11/3.10:49
 """
import socket
import select  ## win：select  Linux：epoll

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("127.0.0.1", 9999,))
sock.setblocking(False)
sock.listen(128)


class HttpRequest(object):
    """
    用户封装用户请求信息
    """

    def __init__(self, content):
        self.content = content

        self.header_bytes = bytes()
        self.header_dict = {}
        self.body_bytes = bytes()

        self.method = ""
        self.url = ""
        self.protocol = ""

        self.initialize()
        self.initialize_headers()

    def initialize(self):

        temp = self.content.split(b'\r\n\r\n', 1)
        if len(temp) == 1:
            self.header_bytes += temp
        else:
            h, b = temp
            self.header_bytes += h
            self.body_bytes += b

    @property
    def header_str(self):
        # return str(self.header_bytes, encoding='utf-8')
        return str(self.header_bytes)

    def initialize_headers(self):
        headers = self.header_str.split('\r\n')
        first_line = headers[0].split(' ')
        if len(first_line) == 3:
            self.method, self.url, self.protocol = headers[0].split(' ')
            for line in headers:
                kv = line.split(':')
                if len(kv) == 2:
                    k, v = kv
                    self.header_dict[k] = v


## 直接socket.accept() ， 但是同时只能接受一个请求
'''
等待一个或多个文件描述符为某种I/O.准备就绪
前三个参数是要等待的文件描述符序列：
'''


def main():
    return 'main'


def index():
    return 'index'


routes = [
    ('/main/', main),
    ('/index/', index),
]


def run():
    inputs = []
    inputs.append(sock)
    '''
        rlist -- wait until ready for reading ##准备读
        wlist -- wait until ready for writing
        xlist -- wait for an ``exceptional condition''
    '''
    while True:
        rlist, wlist, elist = select.select(inputs, [], [], 0.05)
        for r in rlist:
            if r == sock:  ## 表示发来新连接请求
                conn, addr = sock.accept()
                conn.setblocking(False)  ## 不阻塞
                inputs.append(conn)  ## 加入到列表
            else:
                ''' 发来请求数据'''
                data = b""
                while True:
                    try:
                        chunk = r.recv(1024)
                        data = data + chunk
                    except  Exception as e:
                        print(e)
                        chunk = None
                    if not chunk:  ## 数据接收完成
                        break  ##跳出循环

                ## data请求处理，请求头和请求体
                ## 1、请求头获取url
                request = HttpRequest(data)
                print(request.url)
                print(request.method)
                print(request.header_dict)
                print(request.body_bytes)
                ## 2、去路由匹配，获取指定的函数
                import re
                flag = False
                func = None
                for route in routes:
                    if re.match(route[0], request.url):
                        flag = True
                        func = route[1]  # 给函数赋值
                        break
                if flag:  ## 表示匹配成功
                    result = func(request)  ## 执行函数
                    # r.sendall(bytes('1111111111111111111')) ## 返回结果
                    r.sendall(bytes(result,encoding='utf-8'))  ## 返回结果
                else:  ## 没有匹配成功！
                    r.sendall(b'404')
                ## 3、执行函数，获取返回值

                ## 4、将返回值发送回去r.sendall(b'assasasas')  ##返回数据 HTTP结束了

                inputs.remove(r)  ## 移除
                r.close()  ##关闭
                print('-----------------')


if __name__ == '__main__':
    run()


''''
    本web框架的实现：只支持同步，还不能支持异步
'''


