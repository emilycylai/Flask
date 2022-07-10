from datetime import datetime
from flask import Flask, render_template, request
from scrape.pm25 import get_pm25, get_six_pm25, get_all_city, get_city_pm25
import json
from bs4 import BeautifulSoup

app = Flask(__name__)


@app.route('/')
@app.route('/<name>')
def index(name='GUEST'):
    today = getToday()
    # return "<h1>Hello World!</h1>"
    return render_template('./index.html', today=today, name=name)


@app.route('/city-pm25/<city>', methods=['GET'])
def pm25_city_json(city):
    stationName, result = get_city_pm25(city)
    return json.dumps({'stationName': stationName, 'result': result}, ensure_ascii=False)


@app.route('/six-pm25-json', methods=['POST'])
def pm25_six_json():
    six_cities, result = get_six_pm25()
    return json.dumps({'citys': six_cities, 'result': result}, ensure_ascii=False)


@app.route('/pm25-json', methods=['GET', 'POST'])
def pm25_json():
    columns, values = get_pm25(False)

    stationName = [value[1] for value in values]
    result = [value[2] for value in values]

    data = {'date': getToday(), 'stationName': stationName, 'result': result}
    return json.dumps(data, ensure_ascii=False)

    # for value in values:
    #print(value[1], value[2])


@app.route('/pm25-chart')
def pm25_chart():
    citys = get_all_city()
    return render_template('./pm25-charts-bulma.html', countys=citys)


@app.route('/pm25', methods=['GET', 'POST'])  # 預設為GET
def pm25():
    sort = False

    if (request.method == 'POST'):
        # print('POST')
        if request.form.get('sort'):
            sort = True
            # print('SORT')

        # if request.form.get('update'):#因為上面已有sort=False宣告
            # sort=False
            # print('UPDATE')

    today = getToday()
    columns, values = get_pm25(sort)
    return render_template('./pm25.html', **locals())


@app.route('/stock')
def stock():
    today = getToday()
    stocks = [
        {'分類': '日經指數', '指數': '22,920.30'},
        {'分類': '韓國綜合', '指數': '2,304.59'},
        {'分類': '香港恆生', '指數': '25,083.71'},
        {'分類': '上海綜合', '指數': '3,380.68'}
    ]
    for stock in stocks:
        print(stock['分類'], stock['指數'])
    return render_template('./stocks.html', **locals())


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
def getToday():
    today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # return f'<h1>Hello {name}. Welcome!</h1><br>{today}'
    return today


if __name__ == '__main__':  # 以防外面引用，希望只給本地端使用
    # getToday('Emily')
    # pm25_json()
    app.run(debug=True)
