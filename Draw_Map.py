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
# 0720 : 쉼표 없애는 함수
def functrim(parm):
    if(parm[0]==parm[-1] ) and parm.startswith(("'",'"')) :
        return parm[1:-1]
    return parm ;

def main():

    input = sys.argv[1]
    latitude =sys.argv[2] # 위도
    longitude = sys.argv[3] # 경도
    input_name = sys.argv[4]
    input_cnt = sys.argv[5]
    availableCount = json.loads(sys.argv[6])
    input_stgid = sys.argv[7]  # 0720 stg_id :공연시설 ID
    chargerTypeInfo = json.loads(sys.argv[8])  # 0720 충전기타입 정보
    #availableCount = json.loads(json.dumps(sys.argv[6]), ensure_ascii=True)
    # #bottle
    # name = input

    #0720 공연정보API :: IP고정
    input_stgid = functrim(input_stgid) #0720 ' 제거
    iframe="<iframe width='350' height=300 src='http://3.38.37.58:3000/getPrfInfo?input="+input_stgid+"&cnt="+input_cnt+"' title='공연정보' frameborder=0 allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture' allowfullscreen></iframe>"

    if int(input_cnt) >= 3:
        map = folium.Map(location=[latitude, longitude], zoom_start=15)
       # iframe = folium.IFrame('오늘 총 ' + '<b>'+str(input_cnt)+'</b>'+'개의 공연이 있어 혼잡이 예상됩니다.'+'<br>'+' 여유로운 충전소를 찾으세요!', width = 350, height = 80)
        popup = folium.Popup(iframe, max_width=350)
        folium.Marker(location=[latitude, longitude], icon=folium.Icon(icon='star',color='red'), tooltip = input_name, popup = popup ).add_to(map)
    else:
        map = folium.Map(location=[latitude, longitude], zoom_start=16)
       # iframe = folium.IFrame('오늘 총 ' + '<b>'+str(input_cnt)+'</b>'+'개의 공연이 있습니다.' ,width = 230, height = 80)
        popup = folium.Popup(iframe, max_width=350)
        folium.Marker(location=[latitude, longitude], icon=folium.Icon(icon='star',color='orange'), tooltip = input_name, popup = popup).add_to(map)

    temp = ''

    for i in availableCount:
        lat = i['위도']
        long= i['경도']
        type =''
        flag1=0
        flag2=0
        flag3=0
        flag4=0
        flag5=0
        flag6=0
        flag7=0
        if (i['주차료무료']=='Y'):
            isFree = '무료'
        elif (i['주차료무료']=='N'):
            isFree = '유료'
        else : #주차료정보 없는 경우
            isFree = '정보없음'

        for j in chargerTypeInfo:

            if(j['충전소ID'] == i['충전소ID']):

                if (j['충전기타입']=='01'):      flag1 = 1
                elif (j['충전기타입']=='02'):    flag2 = 1
                elif (j['충전기타입']=='03'):    flag3 = 1
                elif (j['충전기타입']=='04'):    flag4 = 1
                elif (j['충전기타입']=='05'):    flag5 = 1
                elif (j['충전기타입']=='06'):    flag6 = 1
                elif (j['충전기타입']=='07'):    flag7 = 1

                type = ''
                if (flag1):     type += 'DC차데모' + '<br>'
                if (flag2):     type += 'AC완속'  + '<br>'
                if (flag3):     type += 'DC차데모+AC3상' + '<br>'
                if (flag4):     type += 'DC콤보' + '<br>'
                if (flag5):     type += 'DC차데모+DC콤보' + '<br>'
                if (flag6):     type += 'DC차데모+AC3상+DC콤보' + '<br>'
                if (flag7):     type += 'AC3상' + '<br>'





        print("['충전소ID']:",j['충전소ID'], "['충전기타입']", type)
        print("LAT & LONG", lat, long)
        #0720 충전소 pop-up html 및 스타일시트 추가
        template =" <table style='width:100%' border=0><tr>"
        template = template+"<th style='background: #008000	;color :#FFFFFF; padding:5px;height : 25px;border-bottom: 1px solid gray;font-family:Malgun Gothic;font-size:12px'>충전소명 : "+ str(i['충전소명']) + "</th>"
        template = template+"</tr><tr><td align=left style='padding:5px;border-bottom: 1px solid gray;font-family:Malgun Gothic;font-size:12px;line-height:1.5;'>"
        template = template+"<ul>"
        template = template+" <li>주소 : "+str(i['주소'])+"</li>"
        template = template+" <li><font color='#dc143c'> 충전가능대수 : <b> "+str(i['안내']) +"대</b></font></li>"
        template = template+" <li>전화번호 : "+str(i['전화번호']) +"</li>"
        template = template+" <li>사용시간 : "+str(i['사용시간']) +"</li>"
        template = template+" <li>주차료 : "+isFree +"</li>"
        template = template+" <li>사용가능한 충전기타입 : "+'<br>'+ type +"</li>"
        template = template+"</ul>"
        template = template+"</td></tr>"
        template = template+"</table>"

        if int(i['안내']) >= 5:
          # iframe = folium.IFrame('<b>충전소명</b> : ' + str(i['충전소명']) + '<br><br>' + '<b>주소</b> : ' + str(i['주소']) + '<br><br>'+ '<b>충전가능 대수</b> : ' + str(i['안내'])+'대'+ '<br><br>' +'<b>전화번호</b> : ' +str(i['전화번호']) + '<br><br>' +'<b>사용시간</b> : ' +str(i['사용시간']) + '<br><br>'+'<b>주차료</b> : '+ isFree, height = 260)
            iframe = folium.IFrame(template, height =200)
            popup = folium.Popup(iframe, min_width=320,max_width=400)
            folium.Marker(location=[lat, long], icon=folium.Icon(icon='flag',color='darkblue'), tooltip= str(i['안내'])+'대', popup=popup).add_to(map)

        elif int(i['안내'])>= 3:
          #  iframe = folium.IFrame('<b>충전소명</b> : ' + str(i['충전소명']) + '<br><br>' + '<b>주소</b> : ' + str(i['주소']) + '<br><br>'+ '<b>충전가능 대수</b> : ' + str(i['안내'])+'대'+ '<br><br>' +'<b>전화번호</b> : ' +str(i['전화번호']) + '<br><br>' +'<b>사용시간</b> : ' +str(i['사용시간']) + '<br><br>' +'<b>주차료</b> : '+ isFree, height = 260)
            iframe = folium.IFrame(template, height =200)
            popup = folium.Popup(iframe, min_width=320, max_width=400)
            folium.Marker(location=[lat, long], icon=folium.Icon(icon='flag',color='blue'), tooltip=str(i['안내'])+'대', popup=popup).add_to(map)

        else:
          #  iframe = folium.IFrame('<b>충전소명</b> : ' + str(i['충전소명']) + '<br><br>' + '<b>주소</b> : ' + str(i['주소']) + '<br><br>'+ '<b>충전가능 대수</b> : ' + str(i['안내'])+'대'+ '<br><br>' +'<b>전화번호</b> : ' +str(i['전화번호']) + '<br><br>' +'<b>사용시간</b> : ' +str(i['사용시간']) + '<br><br>'+'<b>주차료</b> : '+ isFree, height = 260)
            iframe = folium.IFrame(template, height =200)
            popup = folium.Popup(iframe, min_width=320, max_width=400)
            folium.Marker(location=[lat, long], icon=folium.Icon(icon='flag',color='lightblue'), tooltip=str(i['안내'])+'대', popup=popup).add_to(map)

    LocateControl().add_to(map)
    map.save('public/map_station2.html')
    print("Draw_Map.py::map.saved")

if __name__ == '__main__':
    main()
