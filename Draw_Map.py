
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

    input = sys.argv[1]
    latitude =sys.argv[2] # 위도
    longitude = sys.argv[3] # 경도
    input_name = sys.argv[4]
    input_cnt = sys.argv[5]
    availableCount = json.loads(sys.argv[6])
    #availableCount = json.loads(json.dumps(sys.argv[6]), ensure_ascii=True)
    # #bottle
    # name = input

    if int(input_cnt) >= 3:
        map = folium.Map(location=[latitude, longitude], zoom_start=15)
        iframe = folium.IFrame('오늘 총 ' + '<b>'+str(input_cnt)+'</b>'+'개의 공연이 있어 혼잡이 예상됩니다.'+'<br>'+' 여유로운 충전소를 찾으세요!', width = 350, height = 80)
        popup = folium.Popup(iframe, max_width=350)
        folium.Marker(location=[latitude, longitude], icon=folium.Icon(icon='star',color='red'), tooltip = input_name, popup = popup ).add_to(map)
    else:
        map = folium.Map(location=[latitude, longitude], zoom_start=16)
        iframe = folium.IFrame('오늘 총 ' + '<b>'+str(input_cnt)+'</b>'+'개의 공연이 있습니다.' ,width = 230, height = 80)
        popup = folium.Popup(iframe, max_width=350)
        folium.Marker(location=[latitude, longitude], icon=folium.Icon(icon='star',color='orange'), tooltip = input_name, popup = popup).add_to(map)


    for i in availableCount:
        lat = i['위도']
        long= i['경도']

        if (i['주차료무료']=='Y'):
            isFree = '무료'
        elif (i['주차료무료']=='N'):
            isFree = '유료'
        else : #주차료정보 없는 경우
            isFree = '정보없음'

        print("LAT & LONG", lat, long)
        if int(i['안내']) >= 5:
            iframe = folium.IFrame('<b>충전소명</b> : ' + str(i['충전소명']) + '<br><br>' + '<b>주소</b> : ' + str(i['주소']) + '<br><br>'+ '<b>충전가능 대수</b> : ' + str(i['안내'])+'대'+ '<br><br>' +'<b>전화번호</b> : ' +str(i['전화번호']) + '<br><br>' +'<b>주차료</b> : ' +isFree, height = 220)
            popup = folium.Popup(iframe, min_width=300, max_width=400)
            folium.Marker(location=[lat, long], icon=folium.Icon(icon='flag',color='darkblue'), tooltip= str(i['안내'])+'대', popup=popup).add_to(map)

        elif int(i['안내'])>= 3:
            iframe = folium.IFrame('<b>충전소명</b> : ' + str(i['충전소명']) + '<br><br>' + '<b>주소</b> : ' + str(i['주소']) + '<br><br>'+ '<b>충전가능 대수</b> : ' + str(i['안내'])+'대'+ '<br><br>' +'<b>전화번호</b> : ' +str(i['전화번호']) + '<br><br>' +'<b>주차료</b> : ' +isFree, height = 220)
            popup = folium.Popup(iframe, min_width=300, max_width=400)
            folium.Marker(location=[lat, long], icon=folium.Icon(icon='flag',color='blue'), tooltip=str(i['안내'])+'대', popup=popup).add_to(map)

        else:
            iframe = folium.IFrame('<b>충전소명</b> : ' + str(i['충전소명']) + '<br><br>' + '<b>주소</b> : ' + str(i['주소']) + '<br><br>'+ '<b>충전가능 대수</b> : ' + str(i['안내'])+'대'+ '<br><br>' +'<b>전화번호</b> : ' +str(i['전화번호']) + '<br><br>' +'<b>주차료</b> : ' +isFree, height = 220)
            popup = folium.Popup(iframe, min_width=300, max_width=400)
            folium.Marker(location=[lat, long], icon=folium.Icon(icon='flag',color='lightblue'), tooltip=str(i['안내'])+'대', popup=popup).add_to(map)





    LocateControl().add_to(map)
    map.save('public/map_station2.html')
    print("Draw_Map.py::map.saved")

if __name__ == '__main__':
    main()

# #bottle
# return static_file('map_station2.html', root='./public/')
# run(host='0.0.0.0', port=8080, threaded=True)
