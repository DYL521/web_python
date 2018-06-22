#!/usr/bin/env python3  
# -*- coding: utf-8 -*-  
"""  
 @desc:  
 @author: DYL  
 @contact: chng547835@163.com  
 @site: www.xxxx.com  
 @software: PyCharm  @since:python 3.5.2 on 2016/11/3.10:49  
 """

from flask import Flask, render_template, request,\
    make_response,redirect,url_for,session

## 1、# 静态文件和模板路径的配置
app = Flask(__name__)


## 5、自定义模板函数
def jinxin():
    return '<h1>OKOKKO</h1>'


## 6、设置请求的方式
@app.route("/index/", methods=['GET', 'POST'])
def hello():
    ## 3、返回字符串
    # return "Hello World!"

    '''
    request.method
    request.args
    request.form
    request.values
    request.files
    request.cookies
    request.headers
    request.path
    request.full_path
    request.script_root
    request.url
    request.base_url
    request.url_root
    request.host_url
    request.host
    '''
    ## python ORM框架 SQLAchemy框架--- django自带ORM框架

    ##7、接受参数request 对象中
    print(request.args)

    ##8、构造响应额外的数据 --- flask
    # obj = make_response(render_template('index.html'
    #                                     , k1='root', k2=[1, 2, 3]
    #                                     , k3={'name': 'alex', 'age': 24}
    #                                     , k4=jinxin))
    # obj.set_cookie(k1 = 'v1')
    # return obj

    ## 4、返回一个模板
    # return render_template('index.html'
    #                        , k1='root', k2=[1, 2, 3]
    #                        , k3={'name': 'alex', 'age': 24}
    #                        , k4=jinxin)

    ## 10、session # 就是个字典
    #session['username'] = request.form['username']

    ## 9、重定向 --- 类似于reverse功能:url_for
    # return redirect('/test/about')
    url = url_for('test','about') ##相当于django的reverse
    return redirect(test)

'''
返回的数据主要有三种：
    1、只返回字符串
    2、返回返回模板引擎-- 也是字符串带上其他数据
    3、重定向
'''


'''路由系统
@app.route('/user/<username>')
@app.route('/post/<int:post_id>')
@app.route('/post/<float:post_id>')
@app.route('/post/<path:path>')
@app.route('/login', methods=['GET', 'POST'])
'''


## 只接受的参数-- 匹配字符串、或者python项目
## 只接受其中一个参数，其他都不要！
@app.route('/test/<any(about, help, imprint, class, "foo,bar"):page_name>')
def test(page_name):
    return page_name


if __name__ == "__main__":
    # 2、设置IP和端口
    app.run()
    ##app.wsgi_app() ## 请求入口


