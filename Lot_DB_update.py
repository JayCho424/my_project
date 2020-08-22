from pymongo import MongoClient
import requests

client = MongoClient('localhost', 27017)
db = client.dbLotto_SP

Recent_Lotto_WK = '924'

#wk회차에 대한 Lotto API를 불러옴
def get_Lotto_API(wk):
    url = 'https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=' + wk
    data = requests.get(url)
    lotto_num = data.json()
    return lotto_num

#Weekly Update (매 주 1회 update) :
#   기능 1 : 최근 API db에 업데이트 (db : LottoAPI)
#   기능 2 : 출현 횟수 업데이트 (db: Lotto_Appear_Count)
def update_Weekly():
    count_list = [0 for i in range(45)]
    Recent_all_list = list(db.LottoAPI.find({}, {'_id': False}).sort('drwNo', -1))
    for one in Recent_all_list:
        for j in range(6):
            drw_num = int(one['drwtNo'+str(j+1)]) - 1
            count_list[drw_num] = count_list[drw_num] + 1
    print(count_list)
    return count_list

#초기 data update
#for wk in range(int(Recent_Lotto_WK)):
#    Recent_Lot = get_Lotto_API(str(wk+1))
#    db.LottoAPI.insert_one(Recent_Lot)
#    print(Recent_Lot)
#초기 count update
#count_list = update_Weekly()
#for i in range(len(count_list)):
#    db.Lotto_Appear_Count.insert_one({'Num' : i+1, 'Count' : count_list[i]})