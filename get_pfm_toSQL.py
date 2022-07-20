
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

weekday = ['월요일','화요일','수요일','목요일','금요일','토요일','일요일']
today = datetime.datetime.now()
week = today.weekday()
to_weekday = weekday[week]
todaytime = today.strftime('%Y-%m-%d %H:%M:%S')
stardate = today.strftime('%Y%m%d')   # 공연중인 데이터를 기준 : 익일기준 한달  데이터를 가지고 오기
enddate =  today + relativedelta(months=1)
enddate = enddate.strftime('%Y%m%d')

url =f'http://www.kopis.or.kr/openApi/restful/pblprfr?service={service_key}&'
# stdate=20160601&eddate=20160630&cpage=1&rows=5&prfstate=02&signgucode=11&signgucodesub=1111&kidstate=Y'  #1606
zcode = '11'  #서울
queryParams = urlencode({ quote_plus('stdate') : stardate,     #익일 연월일
                          quote_plus('eddate') : enddate,     #다음달
                          quote_plus('cpage') : 1,
                          quote_plus('rows') : 9999,
                          quote_plus('signgucode') : zcode
                          })
url2 = url + queryParams
# print(url2)

response = urlopen(url2)
results = response.read().decode("utf-8")
results_to_json = xmltodict.parse(results)
data = json.loads(json.dumps(results_to_json))

stage = data['dbs']['db']
prf_id = []  #공연 ID
prf_name= [] #공연명
prf_gen = []  #공연 장르명
prf_state =[]  #공연상태
prf_from = [] #공연시작일
prf_to =[] #공연종료일
zscode =[]   # 지역시군 : 경주시
prf_poster =[] # 공연포스터경로
stg_name=[] #공연시설명
prf_openrun =[] #오픈런
prf_zcode =[]
prf_today =[]

cnt = 0

for i in stage:

    prf_id.append(i['mt20id'])
    prf_name.append(i['prfnm'])
    prf_gen.append(i['genrenm'])
    prf_state.append(i['prfstate'])
    prf_from.append(i['prfpdfrom'])
    prf_to.append(i['prfpdto'])
    prf_poster.append(i['poster'])
    stg_name.append(i['fcltynm'])
    prf_openrun.append(i['openrun'])
    prf_zcode.append(zcode);
    prf_today.append(todaytime);

    cnt+=1

# DB Connection
db_connection_str ='mysql+pymysql://'+ db_config2
db_connection = create_engine(db_connection_str)
conn = db_connection.connect()

print("공연갯수=>", cnt )

df=pd.DataFrame([prf_id,prf_name,prf_gen,prf_state,prf_from,prf_to,prf_poster,stg_name,prf_openrun,prf_zcode,prf_today]).T
df.columns=['prf_id','prf_name','prf_gen','prf_state','prf_from','prf_to','prf_poster','stg_name','prf_openrun','prf_zcode','prf_today']
df.to_sql(name='prfList',con= conn, if_exists='replace', index='id'  )
# 공연정보 저장 완료
print("공연정보를 저장 하였습니다.")
conn.close()

# csv 파일 생성
# df.to_csv('./data/prf/rf_list_0714.csv',encoding='utf-8')
# Mysql 저장
