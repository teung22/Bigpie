
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import font_manager
import pymongo
import sys

plt.rcParams['font.size'] = 12.0
plt.rcParams['font.family'] = 'batang'
plt.rcParams['font.family'] = 'Malgun Gothic'

# font_location = "c:/Windows/fonts/malgun.ttf"
# font_name = font_manager.FontProperties(fname=font_location).get_name()
#matplotlib.rc('font', family=font_name)

#------------------------------------------------------------------------------------------------------
import webbrowser
import folium, json
import os
from folium.plugins import MarkerCluster #사용
from folium.plugins import LocateControl
import requests
# #bottle
# @route('/get/<name>')
# def index(name=""):

def main():
    #1. 현재 위치 가져오기 (기능정의서 #2,3)
    ############################################
    #kakao Geo api로 내 위치 가져오기(?)
    #필수: lat, lng, zcode(시), zscode(구)
    #for test :: 고정
    input = sys.argv[1]
    latitude =sys.argv[2] # 위도
    longitude = sys.argv[3] # 경도
    input_name = sys.argv[4]
    input_cnt = sys.argv[5]
    # #bottle
    # name = input
    print("11111: ", latitude, longitude)
    if int(input_cnt) >= 3:
        map = folium.Map(location=[latitude, longitude], zoom_start=15)
        iframe = folium.IFrame(str(input_cnt)+'개의 공연이 있어 혼잡이 예상됩니다.'+'<br>'+' 여유로운 충전소를 찾으세요!', width = 300, height = 70)
        popup = folium.Popup(iframe, max_width=230)
        folium.Marker(location=[latitude, longitude], icon=folium.Icon(icon='star',color='red'), tooltip = input_name, popup = popup ).add_to(map)
    else:
        map = folium.Map(location=[latitude, longitude], zoom_start=16)
        folium.Marker(location=[latitude, longitude], icon=folium.Icon(icon='star',color='orange'), tooltip = input_name).add_to(map)

    #2. 데이터 가져오기 from MongoDB
    ############################################
    #for test : df로 가져오기 from Get_evStationInfo.py

    connect_to = pymongo.MongoClient("3.36.89.204",27017)
    mongodb = connect_to.bigpie.evstations
    print("Draw_Map.py::mongodb.find({'zscode' : ", input)

    for i in mongodb.find({'zscode' : input}):


        lat = i['위도']
        long= i['경도']

        if int(i['충전기상태']) >= 5:
            iframe = folium.IFrame('<b>충전소명</b> : ' + str(i['충전소명']) + '<br><br>' + '<b>주소</b> : ' + str(i['주소']) + '<br><br>'+ '<b>충전가능 대수</b> : ' + str(i['충전기상태'])+'대'+ '<br><br>' +'<b>전화번호</b> : ' +str(i['전화번호']))
            popup = folium.Popup(iframe, min_width=300, max_width=350)
            folium.Marker(location=[lat, long], icon=folium.Icon(icon='flag',color='darkblue'), tooltip= str(i['충전기상태'])+'대', popup=popup).add_to(map)

        elif int(i['충전기상태'])>= 3:
            iframe = folium.IFrame('<b>충전소명</b> : ' + str(i['충전소명']) + '<br><br>' + '<b>주소</b> : ' + str(i['주소']) + '<br><br>'+ '<b>충전가능 대수</b> : ' + str(i['충전기상태'])+'대'+ '<br><br>' +'<b>전화번호</b> : ' +str(i['전화번호']))
            popup = folium.Popup(iframe, min_width=300, max_width=350)
            folium.Marker(location=[lat, long], icon=folium.Icon(icon='flag',color='blue'), tooltip=str(i['충전기상태'])+'대', popup=popup).add_to(map)

        else:
            iframe = folium.IFrame('<b>충전소명</b> : ' + str(i['충전소명']) + '<br><br>' + '<b>주소</b> : ' + str(i['주소']) + '<br><br>'+ '<b>충전가능 대수</b> : ' + str(i['충전기상태'])+'대'+ '<br><br>' +'<b>전화번호</b> : ' +str(i['전화번호']))
            popup = folium.Popup(iframe, min_width=300, max_width=350)
            folium.Marker(location=[lat, long], icon=folium.Icon(icon='flag',color='lightblue'), tooltip=str(i['충전기상태'])+'대', popup=popup).add_to(map)





    LocateControl().add_to(map)
    map.save('public/map_station2.html')
    print("Draw_Map.py::map.saved")

if __name__ == '__main__':
    main()

# #bottle
# return static_file('map_station2.html', root='./public/')
# run(host='0.0.0.0', port=8080, threaded=True)
