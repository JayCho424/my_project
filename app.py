from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

import requests, random

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbLotto_SP

Recent_Lotto_WK = '924'
app.route('/')

#wk회차에 대한 Lotto API를 불러옴
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
    db.Lotto_Rnd_Try.remove({})
    Recent_Lot = get_Lotto_API(Recent_Lotto_WK)
    Recent_all_list = list(db.LottoAPI.find({}, {'_id' : False}).sort('drwNo',-1))
    return jsonify({'result' : 'success',
                    'No' : Recent_Lot['drwNo'],
                    '6Nums' : [Recent_Lot['drwtNo1'],
                              Recent_Lot['drwtNo2'],
                              Recent_Lot['drwtNo3'],
                              Recent_Lot['drwtNo4'],
                              Recent_Lot['drwtNo5'],
                              Recent_Lot['drwtNo6']], 'list' : Recent_all_list})

@app.route('/lucky', methods = ['GET'])
def my_lucky():

    random_numbers = []
    rnd_num = random.randint(1,45)
    for i in range(6):
        while rnd_num in random_numbers:
            rnd_num = random.randint(1,45)
        random_numbers.append(rnd_num)
    random_numbers.sort()

    db.Lotto_Rnd_Try.insert_one({'No1' : random_numbers[0],
                                 'No2' : random_numbers[1],
                                 'No3' : random_numbers[2],
                                 'No4' : random_numbers[3],
                                 'No5' : random_numbers[4],
                                 'No6' : random_numbers[5]})
    random_list = list(db.Lotto_Rnd_Try.find({}, {'_id': False}))

    return jsonify({'result' : 'success',
                    'rand_nums' : random_numbers,
                    'rand_list' : random_list,
                    'msg' : 'Lucky page'})

@app.route('/luxury', methods = ['GET'])
def my_luxury():
    list_Count = list(db.Lotto_Appear_Count.find({}, {'_id' : False}).sort('Num',1))
    list_Max = list(db.Lotto_Appear_Count.find({}, {'_id' : False}).sort('Count',-1))[0:6]
    list_Min = list(db.Lotto_Appear_Count.find({}, {'_id': False}).sort('Count', 1))[0:6]
    return jsonify({'result' : 'success',
                    'Max' : list_Max,
                    'Min' : list_Min,
                    'Count_list' : list_Count,
                    'msg' : 'Lucky page'})

if __name__ == '__main__':
    app.run('127.0.0.1', port=5000, debug=True)