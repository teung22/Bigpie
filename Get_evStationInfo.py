
from config  import *
import requests
import datetime
import json
import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
import math
import json
import xmltodict
from urllib.request import urlopen
from urllib.parse import urlencode, unquote, quote_plus
import pymongo


result = []

def get_totalCount_fromUrl(zCode):
    url='http://apis.data.go.kr/B552584/EvCharger/getChargerInfo'
    parameter =  '?ServiceKey='+ servickeyEVcharger #본인의 공공데이터 key값
    parameter += '&pageNo=1'
    parameter += '&numOfRows=10'
    #Optional Zcode 11 (서울) 41 (경기)
    if(zCode != 0):
        parameter += '&zcode=' + str(zCode)
    url = url  + parameter

    response = urlopen(url)

    if response.getcode() == 200 :
        print('접속성공 \n')
        results = response.read().decode("utf-8")
        root = ET.fromstring(results)
        totalCount = int(root.find('header').find('totalCount').text)
        return totalCount
    else:
        print(url, ' 접속실패')


def get_request_url(pageNo, numOfRows, zCode):
    url='http://apis.data.go.kr/B552584/EvCharger/getChargerInfo'
    parameter =  '?ServiceKey='+ servickeyEVcharger #본인의 공공데이터 key값
    parameter += '&pageNo=' + str(pageNo)
    parameter += '&numOfRows=' + str(numOfRows)
    #Optional
    if(zCode != 0):
        parameter += '&zcode=' + str(zCode)
    url = url  + parameter

    print(url)

    response = urlopen(url)

    if response.getcode() == 200 :
        print('접속성공 \n')
        results = response.read().decode("utf-8")
        return results
    else:
        print(url, ' 접속실패')




def main():
    parsedData = pd.DataFrame()
    resultList = []
    data = {}
    nStartPage = 1
    nEndPage = 1
    pageNo = 1
    numOfRows = 9999
    zCode = 11  #전국 정보 필요할때는 zCode = 0으로 세팅하기

    #MongoDB에 저장할 fields
    statNm = []
    statId = []
    chgerId = []
    chgerType = []
    addr = []
    location = []
    lat = []
    lng = []
    useTime = []
    busiCall = []
    stat = []
    statUpdDt = []
    lastTsdt = []
    lastTedt = []
    nowTsdt = []
    zcode = []
    zscode = []
    parkingFree = []
    note = []
    limitYn = []
    limitDetail = []
    delYn = []

    totalCount = get_totalCount_fromUrl(zCode)
    print('totalCount ====',totalCount )
    nEndPage = math.ceil(totalCount/numOfRows)
    print('nEndPage ====',nEndPage )

    for pageNo in range(1, nEndPage+1):
        rawData = get_request_url(pageNo, numOfRows, zCode)

        results_to_json = xmltodict.parse(rawData)
        data = json.loads(json.dumps(results_to_json))

        print("Loading pages... # :", pageNo)

        evStationInfo = data['response']['body']['items']['item']

        for i in evStationInfo :
            print("Fetching data ...")
            # 이용제한 충전소정보는 DB에서 제외 (아파트등 특정인 소유인 경우)
            if (i['limitYn']=='Y'):
                pass
            elif (i['limitDetail'] =='외부인 사용불가' or i['limitDetail'] =='거주자외 출입제한'
                    or i['limitDetail'] =='거주자외 출입제한)' or i['limitDetail'] =='직원 외 출입제한'):
                pass
            elif ( i['note'] == '외부인 사용불가' or i['note'] == '이용자제한' or i['note'] == '공동주택 입주민 전용'
                    or i['note'] == '공동주택 입주민전용' or i['note'] =='업무용 빌딩 입주자 대상 개방'
                    or i['note'] =='입주민 등 거주자 외 출입 제한' or i['note'] =='입주민만 사용가능 거주자외 출입제한'
                    or i['note'] =='입주민만 사용가능 거주자 외 출입제한'):
                pass
            else:
                statNm.append(i['statNm'])
                statId.append(i['statId'])
                chgerId.append(i['chgerId'])
                chgerType.append(i['chgerType'])
                stat.append(i['stat'])
                zcode.append(i['zcode'])
                zscode.append(i['zscode'])
                addr.append(i['addr'])
                location.append(i['location'])
                lat.append(i['lat'])
                lng.append(i['lng'])
                useTime.append(i['useTime'])
                busiCall.append(i['busiCall'])
                statUpdDt.append(i['statUpdDt'])
                lastTsdt.append(i['lastTsdt'])
                lastTedt.append(i['lastTedt'])
                nowTsdt.append(i['nowTsdt'])
                parkingFree.append(i['parkingFree'])
                note.append(i['note'])
                # limitYn.append(i['limitYn'])
                # limitDetail.append(i['limitDetail'])
                # delYn.append(i['delYn'])


    df=pd.DataFrame([statNm,statId,chgerId,chgerType,stat,zcode,zscode,addr,location,lat,lng,useTime,busiCall,statUpdDt,lastTsdt,lastTedt, nowTsdt,parkingFree, note]).T #,limitYn,limitDetail,delYn
    df.columns=['충전소명.string()','충전소ID.string()','충전기ID.string()','충전기타입.string()','충전기상태.string()','zcode.string()','zscode.string()','주소.string()','위치.string()','위도.string()','경도.string()','사용시간.string()','전화번호.string()','상태갱신일시.string()','마지막충전시작일시.string()','마지막충전종료일시.string()','충전중시작일시.string()','주차료무료.string()','안내.string()']
    #df.columns=['충전소명','충전소ID','충전기ID','충전기타입','충전기상태','zcode','zscode','주소','위치','위도','경도','사용시간','전화번호','상태갱신일시','마지막충전시작일시','마지막충전종료일시','충전중시작일시','주차료무료','안내']
    #df=df.sort_values(by='zscode', ascending=True)
    print("Saving csv file ...")
    df.to_csv('evStationInfo.csv',index=False)


if __name__ == '__main__':
    main()
