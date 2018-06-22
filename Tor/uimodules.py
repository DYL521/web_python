#!/usr/bin/env python3  
# -*- coding: utf-8 -*-  
"""  
 @desc:  
 @author: DYL  
 @contact: chng547835@163.com  
 @site: www.xxxx.com  
 @software: PyCharm  @since:python 3.5.2 on 2016/11/3.10:49  
 """

from tornado.web import UIModule
from tornado import escape


class custom(UIModule):

    def render(self, *args, **kwargs):
        return escape.xhtml_escape('<h1>wupeiqi</h1>')
        # return escape.xhtml_escape('<h1>wupeiqi</h1>')
