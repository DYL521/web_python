#!/usr/bin/env python3  
# -*- coding: utf-8 -*-  
"""  
 @desc:  
 @author: DYL  
 @contact: chng547835@163.com  
 @site: www.xxxx.com  
 @software: PyCharm  @since:python 3.5.2 on 2016/11/3.10:49  
 """

from snow import Snow
from snow import HttpResponse

#http://www.cnblogs.com/wupeiqi/articles/6536518.html
def index(request):
    return HttpResponse('OK')


routes = [
    (r'/index/', index),
]

app = Snow(routes)
app.run(port=8012)