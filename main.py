#import flask
from datetime import datetime
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return "<h1>Hello World!</h1>"


@app.route('/stock')
def stock():
    stocks = [
        {'分類': '日經指數', '指數': '22,920.30'},
        {'分類': '韓國綜合', '指數': '2,304.59'},
        {'分類': '香港恆生', '指數': '25,083.71'},
        {'分類': '上海綜合', '指數': '3,380.68'}
    ]
    for stock in stocks:
        print(stock['分類'], stock['指數'])
    return render_template('./stocks.html', stocks=stocks)


@app.route('/sum/x=<x>&y=<y>')
def get_sum(x, y):
    try:
        total = str(eval(x)+eval(y))
        # return f'{x}+{y} 總和為：{total}'
    except Exception as e:
        print(e)
        total = '輸入錯誤！'
        # return '<h1 style="color:red">輸入錯誤！</h1>'
    result = {
        'x': x,
        'y': y,
        'total': total
    }
    return render_template('./index.html', result=result)


@app.route('/today')
@app.route('/today/<name>')
def getToday(name='GUEST'):
    today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return f'<h1>Hello {name}. Welcome!</h1><br>{today}'


if __name__ == '__main__':  # 以防外面引用，希望只給本地端使用
    getToday('Emily')
    app.run(debug=True)
