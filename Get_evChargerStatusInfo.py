from config  import *
import requests
import datetime
import json
import pandas as pd
import xml.etree.ElementTree as ET
from urllib.request import urlopen
from urllib.parse import urlencode, unquote, quote_plus
import xmltodict
import pymongo
import math

result = []

def get_totalCount_fromUrl(zCode):
    url='http://apis.data.go.kr/B552584/EvCharger/getChargerStatus'
    parameter =  '?ServiceKey='+ servickeyEVcharger #본인의 공공데이터 key값
    parameter += '&pageNo=1'
    parameter += '&numOfRows=10'
    parameter += '&period=10'
    #Optional
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
    url='http://apis.data.go.kr/B552584/EvCharger/getChargerStatus'
    parameter =  '?ServiceKey='+ serviceKeyEVcharger #본인의 공공데이터 key
    parameter += '&pageNo=' + str(pageNo)
    parameter += '&numOfRows=' + str(numOfRows)
    parameter += '&period=10'
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

    resultList = []
    nStartPage = 1
    nEndPage = 2
    pageNo = 1
    numOfRows = 9999
    zCode = 11

    #MongoDB에 저장할 fields
    #statId,chgerId,stat,statUpdDt,lastTsdt,lastTedt,nowTsdt
    statId = []
    chgerId = []
    stat = []
    statUpdDt = []
    lastTsdt = []
    lastTedt = []
    nowTsdt = []

    totalCount = get_totalCount_fromUrl(zCode)
    print('totalCount ====',totalCount )
    nEndPage = math.ceil(totalCount/numOfRows)

    connect_to = pymongo.MongoClient("localhost",27017) #본인의 EC2 로컬호스트주소
    mongodb = connect_to.bigpie.evstations

    for pageNo in range(1, nEndPage+1):
        rawData = get_request_url(pageNo, numOfRows, zCode)

        results_to_json = xmltodict.parse(rawData)
        data = json.loads(json.dumps(results_to_json))

        evChargerInfo = data['response']['body']['items']['item']

        for i in evChargerInfo :

            # statID 매칭되는 항목 MongoDB에서 찾아 DB update
            mongoObj = mongodb.find_one({'충전소ID' : i['statId']},{'충전기ID' : i['chgerId']})

            if (mongoObj):
                print("mongoObj ...", mongoObj, i['statId'],i['chgerId'])
                newvalues = { "$push":{'충전기상태': i['stat'],'상태갱신일시': i['statUpdDt'],'마지막충전시작일시': i['lastTsdt'],'마지막충전종료일시': i['lastTedt'],'충전중시작일시': i['nowTsdt']}}
                #mongodb.update_one({'충전소ID': i['statId'],'충전기ID': i['chgerId']}, newvalues )
                mongodb.update_one({'_id' : mongoObj}, newvalues )
            else:
                pass

if __name__ == '__main__':
    main()
