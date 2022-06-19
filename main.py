#import flask
from datetime import datetime
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return "<h1>Hello World!</h1>"


@app.route('/sum/x=<x>&y=<y>')
def get_sum(x, y):
    try:
        total = str(eval(x)+eval(y))
        return f'{x}+{y} 總和為：{total}'
    except Exception as e:
        print(e)
        return '<h1 style="color:red">輸入錯誤！</h1>'


@app.route('/today')
@app.route('/today/<name>')
def getToday(name='GUEST'):
    today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return f'<h1>Hello {name}. Welcome!</h1><br>{today}'


if __name__ == '__main__':  # 以防外面引用，希望只給本地端使用
    getToday('Emily')
    app.run(debug=True)
