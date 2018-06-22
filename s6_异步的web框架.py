#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import select  ## win：select  Linux：epoll
import time

class HttpRequest():
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
        self.initialize_headers() ## 设置

    def initialize(self):

        temp = self.content.split(b'\r\n\r\n', 1) ##请求头与请求体分割
        if len(temp) == 1:
            self.header_bytes += temp[0]
        else:
            h = temp[0] ##头
            b = temp[1] ##体
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


class Future():
    def __init__(self):
        self.result = None


## 直接socket.accept() ， 但是同时只能接受一个请求
'''
等待一个或多个文件描述符为某种I/O.准备就绪
前三个参数是要等待的文件描述符序列：
'''
F = None  ## 全局的对象


def main(request):
    global F
    F = Future()
    return F


def index(request):
    return 'index'


def stop(request):
    global F
    F.result = b'xxxxxxxxxxxxxxxxxx'
    return 'stop'


routes = [
    ('/main/', main),
    ('/index/', index),
    ('/stop/', stop),
]




def run():
    ## 启动socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("127.0.0.1", 9999,))
    sock.setblocking(False)
    sock.listen(128)

    inputs = []
    inputs.append(sock)

    async_request_dict = {
        # 'socket': futrue
    }

    while True:
        rlist, wlist, elist = select.select(inputs, [], [], 0.05)
        for r in rlist:
            if r == sock:
                """新请求到来"""
                conn, addr = sock.accept()
                conn.setblocking(False)
                inputs.append(conn)
            else:
                """客户端发来数据"""
                data = b""
                while True:
                    try:
                        chunk = r.recv(1024)
                        data = data + chunk
                    except Exception as e:
                        chunk = None
                    if not chunk:
                        break
                # data进行处理：请求头和请求体
                request = HttpRequest(data)
                # 1. 请求头中获取url
                # 2. 去路由中匹配，获取指定的函数
                # 3. 执行函数，获取返回值
                # 4. 将返回值 r.sendall(b'alskdjalksdjf;asfd')
                import re
                flag = False
                func = None ## 执行的函数
                for route in routes:##2去路由中匹配，获取指定的函数
                    if re.match(route[0], request.url):
                        flag = True
                        func = route[1]
                        break
                if flag:
                    result = func(request)
                    if isinstance(result, Future): ## 判断是否返回Future 对象
                        async_request_dict[r] = result
                    else:
                        r.sendall(bytes(result, encoding='utf-8'))
                        inputs.remove(r)
                        r.close()
                else:
                    r.sendall(b"404")
                    inputs.remove(r)
                    r.close()
    ## 非阻塞的实现-- 自动断开
        for conn in async_request_dict.keys():
            future = async_request_dict[conn]
            start = future.start  # 获取开始时间
            timeout = future.timeout  ## 超时时间
            ctime = time.time()  ##当前的时间
            if (start + timeout) <= ctime:
                future.result = b"timeout" ## 设置值--就会停止
            if future.result:
                conn.sendall(future.result)
                conn.close()
                del async_request_dict[conn]
                inputs.remove(conn)


if __name__ == '__main__':
    run()

''''
    如果有人跟你装逼说：Tornato 异步非阻塞式怎么实现的？
    回答是：Future对象实现的，Future 会标识是否已经完成 -- 没有连接一直不断开
            只要Future 对象一改变，就会直接断开连接！
'''
'''
    # 1、启动一个socket，绑定并监听端口，死循环监听
    # 2、使用select模块，循环遍历，把每一个来的连接，存放都一个列表
    # 3、死循环，当前的连接conn == 表里的连接 ，就收数据，直到数据接收完成
    
'''