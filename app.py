from flask import Flask, render_template, jsonify, request
import requests

app = Flask(__name__)
Recent_Lotto_WK = '924'
app.route('/')

def get_Lotto_API(wk):
    url = 'https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=' + wk
    data = requests.get(url)
    lotto_num = data.json()
    return lotto_num

@app.route('/')
def fucntion():
    return render_template('index.html')

@app.route('/recent', methods = ['GET'])
def lotto_recent():
    Recent_Lot = get_Lotto_API(Recent_Lotto_WK)
    print(Recent_Lot)

    return jsonify({'result' : 'success', 'msg' : 'Recent page'})

@app.route('/lucky', methods = ['GET'])
def my_lucky():
    page_recieve = request.args.get('page_give')
    print(page_recieve)
    return jsonify({'result' : 'success', 'msg' : 'Lucky page'})

@app.route('/luxury', methods = ['GET'])
def my_luxury():
    page_recieve = request.args.get('page_give')
    print(page_recieve)
    return jsonify({'result' : 'success', 'msg' : 'Luxury page'})

if __name__ == '__main__':
    app.run('127.0.0.1', port=5000, debug=True)