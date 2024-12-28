from flask import Flask, g, url_for, redirect, abort, json, make_response, jsonify,request,session
import logging
app = Flask(__name__)


# @app.route('/hello', methods=['GET', 'POST'])
@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!++++'
    # 这里会重定向baidu页面
    # return '<h1>Hello World!</h1>',301,{'Location':'https://baidu.com'}


@app.route('/hi')
def hi():
    """进行重定向hello_world"""
    return redirect(url_for('hello_world'))


@app.route('/foo')
def foo():
    """使用dump将字典转换为json格式处理并返回"""
    # data = {
    #     'name':'wangjiuyung',
    #     'gender':'male'
    # }
    # response = make_response(json.dumps(data))
    # response.mimetype = 'application/json'
    # return response

    """jsonify()函数接收多种形式的函数，可以时普通函数也是关键字函数,也可以是字典列表或者元组"""
    # return jsonify({'name':'wangjiuyung','gender':'male'})
    """jsonify()默认生成200响应。也可以通过附加状态码来自定义响应类型"""
    return jsonify(message='Error!'), 500


@app.route('/404')
def not_found():
    """返回无法寻找的页面"""
    abort(404)


# <转换器：变量名> 把year的值转换为整数
@app.route('/goback/<int:year>')
def go_back(year):
    return '<p>Welcome to %d!</p>' % (2018 - year)


# any转换器，需要在转换器后添加括号来给出可选值
# 需要在any转换器中传入一个预先定义的列表，可以通过格式化字符串的方式来构建URL规则字符串
colors = ['red', 'blue', 'green', 'yellow', 'cyan', 'magenta', 'yellow']


@app.route('/colors/<any(%s):color>' % str(colors)[1:-1])
def three_colors(color):
    return '<p><b>%s</b></p>' % color


@app.route('/hello/<name>')
def hello_name(name=None):
    # _external = True 会显示全部路径，不然会显示局部路径
    print(url_for('hello_world', name=name, _external=True))
    return 'Hello, {}!'.format(name)


# 注册flask命令
@app.cli.command()
def hello():
    print('hello')


@app.before_request
def do_something():
    """在每个函数运作之前会输出before_request"""
    # print('before_request')
    """获取全局变量g的值"""
    g.name = request.args.get('name')
    print(g.name)

@app.route('/set/<name>')
def set_cookie(name):
    """设置cookie"""
    response = make_response(redirect(url_for('hello')))
    response.set_cookie('name', name)
    return response


@app.route('/hello')
def hello():
    """在flask中，cookie可以用过请求对象的cookies属性读取"""
    # name = request.args.get('name')  #先在cookies的属性找name值
    # print(f'name1={name}')
    # if name is None:
    #     name = request.cookies.get('name', 'hahahaha')  #从cookie中获取name值
    #     print(f'name2={name}')
    # return 'my name is %s ' % name


    '''判断session中是否包含logged_in键，如果有则表示用户已登录。
        如果用户登录过了，显示[Authenticated],
        否者显示 [Not authenticated]
    '''
    name = request.args.get('name')
    if name is None:
        name = request.cookies.get('name','hahaha')
        response = '<p>Hello, {}!</p>'.format(name)
        #根据用户状态返回不同的内同
        if 'logged_in' in session:
            response += '[Authenticated]'
        else:
            response += '[Not authenticated]'
        return response
    # return redirect(url_for('hello_world'))
"""
程序的密钥可以通过flask.secret_key属性或者配置SECRET_KEY设置：
app.secret_key = 'secret string'
或者在.env环境中写入
SECRET_KEY = secret string
然后使用os模块提供的getenv()方法获取
import os
... 
app.secret_key = os.getenv('SECRET_KEY','secret string')
"""
app.secret_key ='secret string'
@app.route('/login')
def login():
    """模拟用户登录"""
    session['logged_in'] = True #写入session
    return redirect(url_for('hello'))

@app.route('/admin')
def admin():
    """通过判断logged_in是否在session中，可以实现用户已经认证会返回一行提示文字，否则会返回403错误响应"""
    if 'logged_in' not in session:
        abort(403)
    return 'Welcome to admin page.'

@app.route('/logout')
def logout():
    "删除session中的logged_in里面的cookie设置"
    if 'logged_in' in session:
        #None是发现没有logged_in键的时候防止报错
        session.pop('logged_in', None)
    return redirect(url_for('hello_world'))
@app.errorhandler(500)
def server_error(e):
    """设置全局错误，出现500错误返回一个"""
    logging.exception(e)
    return 'Server error!',500
if __name__ == '__main__':
    app.run()
