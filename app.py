from flask import Flask, url_for

app = Flask(__name__)


@app.route('/hello', methods=['GET', 'POST'])
@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

#<转换器：变量名> 把year的值转换为整数
@app.route('/goback/<int:year>')
def go_back(year):
    return '<p>Welcome to %d!</p>' % (2018 - year)
#any转换器，需要在转换器后添加括号来给出可选值
#需要在any转换器中传入一个预先定义的列表，可以通过格式化字符串的方式来构建URL规则字符串
colors = ['red', 'blue', 'green', 'yellow', 'cyan', 'magenta', 'yellow']
@app.route('/colors/<any(%s):color>'%str(colors)[1:-1])
def three_colors(color):
    return '<p><b>%s</b></p>' % color
@app.route('/hello/<name>')
def hello_name(name=None):
    # _external = True 会显示全部路径，不然会显示局部路径
    print(url_for('hello_world', name=name, _external=True))
    return 'Hello, {}!'.format(name)

#注册flask命令
@app.cli.command()
def hello():
    print('hello')


if __name__ == '__main__':
    app.run()
