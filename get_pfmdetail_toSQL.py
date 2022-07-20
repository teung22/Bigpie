import requests
import pandas as pd
import xmltodict
import datetime
import json
import pymysql
import re
import xml.etree.ElementTree as ET
from config import*
from sqlalchemy import create_engine
from urllib.request import urlopen
from urllib.parse import urlencode, unquote, quote_plus

# DB coneection
db_connection_str ='mysql+pymysql://'+ db_config2
db_connection = create_engine(db_connection_str)
conn = db_connection.connect()

# 공연리스트 추출
sql = "SELECT prf_id, prf_name FROM prfList"
df_sql = pd.read_sql(sql,db_connection)

#오늘요일 가져오기
weekday = ['월요일','화요일','수요일','목요일','금요일','토요일','일요일']
today = datetime.datetime.now()
week = today.weekday()
to_weekday = weekday[week]
todaytime = today.strftime('%Y-%m-%d %H:%M:%S')

# sprint('today=>',type(today),today,  'to_week=>', type(to_weekday),to_weekday )
prf_id = []  #공연 ID
stg_id =[]  #공연시설
prf_name= [] #공연명
stg_name=[] #공연시설명
prf_cast = []  #공연출연진
prf_crew =[]  #공연제작진
prf_runtime = [] #공연시간
prf_state =[]  #공연상태
prf_from = [] #공연시작일
prf_to =[] #공연종료일
prf_age =[] # 관람연령
prf_psnm =[]  # 제작사
prf_ticktprice =[] # 티켓가격
stg_distance=[] #공연시간
prf_stging =[]
prf_today =[]

cnt = 0

for inx, row in df_sql.iterrows()  :
    tmp_id = row['prf_id']
    tmp_name = row['prf_name']
    # print(tmp_id,tmp_name)
    url =f'http://www.kopis.or.kr/openApi/restful/pblprfr/{tmp_id}?service={service_key}'

    response = urlopen(url)
    results = response.read().decode("utf-8")
    root = ET.fromstring(results)
    stage_element = root.iter(tag="db")

    for element in stage_element :
        prf_id.append(element.find('mt20id').text)
        stg_id.append(element.find('mt10id').text)
        stg_name.append(element.find('fcltynm').text)
        prf_name.append(element.find('prfnm').text)
        prf_state.append(element.find('prfstate').text)
        prf_from.append(element.find('prfpdfrom').text)
        prf_to.append(element.find('prfpdto').text)
        prf_cast.append(element.find('prfcast').text)
        prf_crew.append(element.find('prfcrew').text)
        prf_runtime.append(element.find('prfruntime').text)
        prf_age.append(element.find('prfage').text)
        prf_psnm.append(element.find('entrpsnm').text)
        prf_ticktprice.append(element.find('pcseguidance').text)

        if to_weekday in (element.find('dtguidance').text) :    #해당요일 공연이 있는지 확인
             prf_stging.append("Y")
        else :
            prf_stging.append("N")

        stg_distance.append(element.find('dtguidance').text)
        prf_today.append(todaytime)
        cnt+=1

df=pd.DataFrame([prf_id ,stg_id ,stg_name ,prf_name,prf_state ,prf_from ,prf_to, prf_cast ,prf_crew ,prf_runtime ,prf_age ,prf_psnm ,prf_ticktprice  ,stg_distance,prf_stging, prf_today]).T
df.columns=['prf_id','stg_id','stg_name','prf_name','prf_state','prf_from','prf_to','prf_cast','prf_crew','prf_runtime','prf_age','prf_psnm','prf_ticktprice','stg_distance','prf_stging', 'prf_today']

print("공연상세정보=>", cnt )
#MySQL에 저장
# df.to_sql(name='prfDetail',con= conn, if_exists='replace', index='id', dtype= dtypesql )
df.to_sql(name='prfDetail',con= conn, if_exists='replace', index='id' )
conn.close()
print("데이터베이스에 저장하였습니다.")
# # # # # # csv 파일 생성
# df.to_csv('./data/prf/prf_detail_0715.csv')
