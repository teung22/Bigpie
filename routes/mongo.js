const express = require('express');
const router = express.Router();
const mongoose = require('mongoose');
const request = require('request');
const moment = require('moment');
const axios = require('axios')
const dateutil = require('date-utils');
const mongoClient = require('mongodb').MongoClient
let today = new Date();
var now = today.toFormat("YYYYMMDDHH");
const { PythonShell } = require("python-shell");
const async = require("async");

//let controller = require("/map")

const lainfo = '';
const loinfo = '';
const zscodeinfo = '';
//define scheme
var evStationInfoSchema = mongoose.Schema({
      충전소명: String,
      충전소ID : String,
      충전기ID : String,
      충전기타입 : String,
      충전기상태 : String,
      zcode : String,
      zscode : String,
      주소 : String,
      위치 : String,
      위도 : String,
      경도 : String,
      사용시간 : String,
      전화번호 : String,
      상태갱신일시 : String,
      마지막충전시작일시 : String,
      마지막충전종료일시 : String,
      충전중시작일시 : String,
      주차료무료 : String,
      안내 : String,

});


const EvStation = mongoose.model('evstations',evStationInfoSchema);

router.get('/api/list', function(req, res, next) {
  console.log('/api/list function');
  var count=[{}];
  let num =[];


      var template = `
      <!doctype html>
      <html>
      <head>
        <title>Result</title>
        <meta charset="utf-8">
      </head>
      <body>
          <iframe align = "center" name="targetURL1" class="iframe-preview center1" width="980px" height="1500px" src="../intro.html"></iframe>
      </body>
      </html>
     `;
       //console.log('api/list function::',template);
      res.end(template);


});


// get
let urls = ""
router.get('/getcode', function(req,res,next) {
    var input = req.query.input;
    if (input=='') {
      console.log("where is input?")
    }else{
  //    console.log(" 8000input=>", input)
    //****************************************************************************************
      var url = "http://3.38.37.58:3000" ;
      var queryParams = "/stggetdata?input="+ input ;
      // console.log(url+queryParams)
      request({
          url: encodeURI(url+queryParams),
          method: 'GET'
        }, function (error, response, body) {
          if(!error){
              // console.log('Status', response.statusCode);
              // console.log('Headers', JSON.stringify(response.headers));
              // console.log('Reponse received', body);

              let data = JSON.parse(body);
              // res.json(data);
              // req.flash('input', data)
              console.log("1=>", data)

              var result_zscode  = data[0].ZSCODE ;
              var result_name = data[0].NAME ;
              var result_la = data[0].LA;
              var result_lo = data[0].LO;
              var result_prfcnt = data[0].CNT;
              var result_stgid = data[0].STG_ID;   //#0720 공연장 ID 추가

             //
              console.log(result_zscode,result_name,result_la, result_lo,result_prfcnt)  ;
              //
              // if(req.query.name == null) {
              //   urls = "http://13.209.234.117:3000/api/users/user?user_id="+req.query.user_id;
              // } else {
              //   urls = "http://13.209.234.117:3000/api/users/user?user_id="+req.query.user_id+"&name="+req.query.name;
              // }
              // request(urls, { json:true }, (err, result, body) => {
              //   if (err) { return console.log(err) }
              //   res.send(CircularJSON.stringify(body))
              // })
              //get 으로 Parameter 넘기기 start
              //0720 &stg_id="+result_stgid
                 tmp_urls = "http://54.215.35.186:8000/get?"
                 queryParams = "input="+result_zscode+"&stg_name="+result_name+"&stg_la="+result_la+"&stg_lo="+result_lo+"&stg_cnt="+result_prfcnt+"&stg_id="+result_stgid  ;

                 urls = encodeURI(tmp_urls + queryParams)
                 console.log(urls)
                 request(urls, { json:true }, (err, result, body) => {
                   if (err) { return console.log(err) }
                   res.end(body)

                 })


             //
//parameter 넘기기

            // axios
            //   .get('http://3.38.37.58:8000/get')
            //   .then(result => {
            //      console.log(data) ;
            //       return res.send(CircularJSON.stringify(data))
            //     })
            //     .catch(error => {
            //       console.log(error)
            //     })    //** 클라이언트로 값이 넘어가 버림

//parameter 넘기기

         } else{
           console.log("error",error) ;
          }
        });
      }
});


//////////////////////////////////////////////

router.get('/get', function(req, res, next) {

    console.log('/get ==>');
    db = req.db;
    var input = req.query.input;        //지역코드
    var input_name =req.query.stg_name; //공연장 이름
    var input_la = req.query.stg_la;    //공연장 위도
    var input_lo = req.query.stg_lo;
    var input_cnt = req.query.stg_cnt;  //공연장 공연개수
    var input_stgid = req.query.stg_id ;    //0720 공연장id 추가


   if(input=='') {

        EvStation.findOne({},function(err,docs){
          if(err) console.log('err');
          res.send(docs);
        });
      } else {

        var template;

       var cLength = 0;
       var count=[];
       var countTypeInfo=[];
        async.waterfall([
          function (callback) {
            EvStation.find({"zscode":input},function(err,docs){
              if(err) console.log('err');

              var firstflag = 1;

              for(var i =0; i<docs.length; i++){
                if(docs[i]['충전기상태'] == '2'){
                  if(firstflag){
                    count.push({충전소명 : docs[0]['충전소명'], 충전소ID : docs[0]['충전소ID'], 위도 : docs[0]['위도'],  경도 : docs[0]['경도'],
                               충전기상태 : docs[0]['충전기상태'], 주소 :  docs[0]['주소'], 전화번호 : docs[0]['전화번호'], 사용시간 : docs[0]['사용시간'], 주차료무료 : docs[0]['주차료무료'], 안내 : '1' });
                    countTypeInfo.push({충전소ID : docs[0]['충전소ID'], 충전기ID : docs[0]['충전기ID'], 충전기타입 : docs[0]['충전기타입']})
                    firstflag = 0;
                    cLength ++;
                  }

                  //count 배열 내 같은 충전소명 있으면 충전가능대수만 1 추가
                  //count 배열 내 같은 충전소명 없으면 장소명 추가

                  for(var j=0; j<cLength; j++){

                    if(count[j]['충전소ID'] !=docs[i]['충전소ID']){

                      if(j == cLength-1){
                        //console.log("마지막count:: 충전소명 없으면 장소명 추가:", count[j]['충전소ID'], " != ",docs[i]['충전소ID']  )
                        count.push({충전소명 : docs[i]['충전소명'], 충전소ID : docs[i]['충전소ID'],  위도 : docs[i]['위도'],  경도 : docs[i]['경도'],
                        충전기상태 : docs[i]['충전기상태'],주소 :  docs[i]['주소'], 전화번호 : docs[i]['전화번호'], 사용시간 : docs[i]['사용시간'], 주차료무료 : docs[i]['주차료무료'], 안내 : '1' });
                        cLength ++;
                      }
                    }
                    else {
                      //console.log("count 배열 내 같은 충전소명 있으면 충전가능대수만 1 추가:" )
                      //console.log(":::::::",count[j]['충전기상태'])

                      let temp=parseInt(count[j]['안내'])
                      count[j]['안내'] = temp +1;



                      break;
                    }
                  }
                  countTypeInfo.push({충전소ID : docs[i]['충전소ID'], 충전기ID : docs[i]['충전기ID'], 충전기타입 : docs[i]['충전기타입']})

                }
              }

              callback(null)
            });

          },
              function(callback) {

                let options = {
                  scriptPath: "/data/node/evInfo",
                  args: [input,input_la,input_lo,input_name,input_cnt,JSON.stringify(count),JSON.stringify(input_stgid),JSON.stringify(countTypeInfo) ]   //#0720 공연장 ID 추가
                };
                PythonShell.run("Draw_Map.py", options, function(err, data) {
                  if (err) throw err;
                  console.log(data);
                  console.log(new Date());
                  callback(null,data)
              });
            },
              function(data,callback) {
                console.log("function(data,callback)");
                template = `
                <!doctype html>
                <html>
                <head>
                  <title>Result</title>
                  <meta charset="utf-8">
                </head>
                <link rel="stylesheet" href="index.css">
                <body>
                  <table border = "1" margin:auto; text-align:center;>
                 <tr>
                   <iframe align = "center" name="targetURL1" class="iframe-preview center1" width="1000px" height="500px" src="./map_station2.html"></iframe>
                 </tr>
                  <table border = "1" width = 1000px;>
                   <tr>
                   <th id="evthead">충전소명</th>
                   <th id="evthead">충전소ID</th>
                   <th id="evthead">충전가능 대수</th>
                   <th id="evthead">주소</th>
                   <th id="evthead">전화번호</th>
                   </tr>
                   `;

                     for (var i =0; i<cLength; i++){
                       template += `
                         <tr>
                         <td id="evtd">${count[i]['충전소명']}</td>
                         <td id="evtd" align="center">${count[i]['충전소ID']}</td>
                         <td id="evtd" align="center">${count[i]['안내']}</td>
                         <td id="evtd">${count[i]['주소']}</td>
                         <td id="evtd">${count[i]['전화번호']}</td>
                         </tr>
                         `;
                     }

                     template += `
                     </table>
                     </table>
                    </body>
                    </html>
                   `;
                   //console.log("/Get function::",template);
                   res.end(template);



                console.log(new Date());
            callback(null)
         }],
         function (err) {
           if (err){
             console.log(err)
             return;
           }
           console.log("/Get function::draw map sync completed")
         }
      );


        }
});
module.exports = router;


//10분에 한번씩 UpdateMongoDB하기 (feat. Get_evChargerStatusInfo.py)
//실시간 data 업데이트
//cron 으로 돌리니 자꾸 server가 죽음 ..

var timer =
setInterval(UpdateMongoDB,600000);


function UpdateMongoDB(){
  console.log("Timer:: UpdateMongoDB");
  let options = {
    scriptPath: "/data/node/evInfo",
    //args: ["value1", "value2", "value3"]
  };
  PythonShell.run("Get_evChargerStatusInfo.py", options, function(err, data) {
    if (err) throw err;
    console.log(data);
    console.log(new Date());
  });
}


console.log(new Date());
