
import requests
import pandas as pd
import xmltodict
import json
import pymysql
import datetime
from config import*
from sqlalchemy import create_engine
from urllib.request import urlopen
from urllib.parse import urlencode, unquote, quote_plus
from dateutil.relativedelta import relativedelta

url =f'http://kopis.or.kr/openApi/restful/boxoffice?service={service_key}&'
#http://kopis.or.kr/openApi/restful/boxoffice?service={ServiceKey}&ststype=day&date=20171218&catecode=AAAA&area=11

zcode = '11'  #서울
today = datetime.datetime.today().date()
todaytime = today.strftime('%Y-%m-%d %H:%M:%S')
basedate = today - relativedelta(days=1)
basedate = basedate.strftime('%Y%m%d')

queryParams = urlencode({ quote_plus('ststype') : 'day',     #일별
                          quote_plus('date') : basedate,     #날짜  : 하 루전 집계자료
                        #   quote_plus('catecode') : 'AAAA', 장르구분
                          quote_plus('area') : zcode
                                                })
url2 = url + queryParams
print(basedate)
print(url2)
print("==>api 데이터 받아오기")
response = urlopen(url2)
results = response.read().decode("utf-8")
results_to_json = xmltodict.parse(results)
data = json.loads(json.dumps(results_to_json))

try :
    stage = data['boxofs']['boxof']

    prf_id = []  #공연 ID
    prf_name= [] #공연명prfdtcnt
    prf_runm = []  #공연 순위
    prf_dtcnt =[]  # 상연횟수
    prf_seatcnt=[]
    prf_today =[]

    # print(stage)
    cnt = 0

    for i in stage:
        prf_id.append(i['mt20id'])
        prf_name.append(i['prfnm'])
        prf_runm.append(i['rnum'])
        prf_dtcnt.append(i['prfdtcnt'])
        prf_seatcnt.append(i['seatcnt'])
        prf_today.append(todaytime);
        cnt+=1
    print("==DBconnection")

    # #DB Connection
    db_connection_str = 'mysql+pymysql://'+db_config2
    db_connection = create_engine(db_connection_str)
    conn = db_connection.connect()


    df=pd.DataFrame([prf_id,prf_name,prf_runm,prf_dtcnt,prf_seatcnt, prf_today]).T
    df.columns=['prf_id','prf_name','prf_runm','prf_dtcnt','prf_seatcnt','prf_today']

    df.to_sql(name='prfBoxOffice',con= conn, if_exists='replace', index='id'  )
    # 공연정보 저장 완료
    print("공연갯수=>", cnt )
    print("공연정보를 저장 하였습니다.")
    conn.close()

except Exception as e  :
    print(e , "오류가 발생했습니다.")
# # # csv 파일 생성
# df.to_csv('./data/prf/rf_box_0720.csv',encoding='utf-8')
# # Mysql 저장
