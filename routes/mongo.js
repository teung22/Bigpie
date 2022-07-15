const express = require('express');
const router = express.Router();
const mongoose = require('mongoose');
const request = require('request');
const moment = require('moment');
const axios = require('axios')
const dateutil = require('date-utils');
const mongoClient = require('mongodb').MongoClient
const spawn = require('child_process').spawn
const exec = require('child_process').exec;
let today = new Date();
var now = today.toFormat("YYYYMMDDHH");
const { PythonShell } = require("python-shell");
const async = require("async");
var mysql = require("mysql") ;
var connection = mysql.createConnection({
  host :'database-1.csmitlu4hfs1.ap-northeast-2.rds.amazonaws.com',
  user : 'admin',
  password : 'admin1234',
  database : 'st_db'
})
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
  var input = '11710';

  EvStation.find({"zscode":input},function(err,docs){

    if(err) console.log('/api/list function::err');


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
                 tmp_urls = "http://3.36.89.204:8000/get?"
                 queryParams = "input="+result_zscode+"&stg_name="+result_name+"&stg_la="+result_la+"&stg_lo="+result_lo+"&stg_cnt="+result_prfcnt ;

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
//sql test
// router.get('/get/sql', function(req, res, next) {
//   console.log('/Get function');
//   db = req.db;
//   var input = req.query.input;
//   urls ="http://54.215.67.115:3000/stggetdata?input="+ req.query.input;
//   console.log(urls);
//   request(urls, {json:true}, (err,result,body) =>{
//     if(err) {return console.log(err)}
//     console.log(body);
//     console.log(result);
//
//
//   })
// })

//////////////////////////////////////////////

router.get('/get', function(req, res, next) {
  var count=[{}];
  let num =[];
  console.log('/Get function');
  db = req.db;
  var input = req.query.input;
  var input_name =req.query.stg_name;
  var input_la = req.query.stg_la;
  var input_lo = req.query.stg_lo;
  var input_cnt = req.query.stg_cnt;



  console.log("input::::",input)
 if(input=='') {

      EvStation.findOne({},function(err,docs){
        if(err) console.log('err');
        res.send(docs);
      });
    } else {
      console.log("Draw_Map.py params:::",input,input_la,input_lo);

      var template;
      let options = {
        scriptPath: "/data/node/evInfo",
        args: [input,input_la,input_lo,input_name,input_cnt]
      };
      async.waterfall([
            function(callback) {
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
              <body>
                <table border = "1" margin:auto; text-align:center;>


               <tr>
                 <iframe align = "center" name="targetURL1" class="iframe-preview center1" width="1000px" height="500px" src="./map_station2.html"></iframe>
               </tr>

             `;

             EvStation.find({"zscode":input},function(err,docs){

               if(err) console.log('err');

                 template += `
                  <table border = "1" width = 1000px;>
                   <tr>
                   <th>충전소명</th>
                   <th>충전기ID</th>
                   <th>충전가능 대수</th>
                   <th>주소</th>
                   <th>전화번호</th>
                   </tr>
                   `;

                   var firstflag = 1;
                   var cLength = 0;
                   for(var i =0; i<docs.length; i++){
                     if(docs[i]['충전기상태'] == '2'){
                       if(firstflag){
                         count[0] = docs[0]
                         firstflag = 0;
                         cLength ++;
                       }
                       // if(!count.inclues(docs[i]['충전소ID'])){
                       //   count.push(item))
                       // }


                       //count 배열 내 같은 충전소명 있으면 충전가능대수만 1 추가
                       //count 배열 내 같은 충전소명 없으면 장소명 추가
                       console.log("count.length ::", cLength)
                       for(var j=0; j<cLength; j++){
                         if(count[j]['충전소ID'] !=docs[i]['충전소ID']){

                           if(j == cLength-1){
                             console.log("마지막count:: 충전소명 없으면 장소명 추가:", count[j]['충전소ID'], " != ",docs[i]['충전소ID']  )
                             count[j+1] = docs[i]
                             count[j+1]['충전기상태'] = 1;
                             cLength ++;
                             console.log("충전소명 없으면 장소명 추가:", count[j+1]['충전소ID'],count[j+1]['충전기상태'])

                           }
                         }
                         else {
                           console.log("count 배열 내 같은 충전소명 있으면 충전가능대수만 1 추가:" )
                           // num[j] = count[j]['충전기상태']
                           console.log(":::::::",count[j]['충전기상태'])
                           let temp=parseInt(count[j]['충전기상태'])
                           count[j]['충전기상태'] = temp +1;
                           // count[j]['충전기상태'] =count[j]['충전기상태']+1;
                           console.log(":::::::",count[j]['충전기상태'])
                           break;
                         }



                       }


                     }

                   }

                   for (var i =0; i<count.length; i++){
                     template += `
                       <tr>
                       <th>${count[i]['충전소명']}</th>
                       <th>${count[i]['충전기ID']}</th>
                       <th>${count[i]['충전기상태']}</th>
                       <th>${count[i]['주소']}</th>
                       <th>${count[i]['전화번호']}</th>
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

             });

              console.log(new Date());
          callback(null)
       }],
       function (err) {
         if (err){
           console.log(err)
           return;
         }
         console.log("/Get function::map async completed")
       }
    );


      }
});
module.exports = router;


//10분에 한번씩 실행할 방법?
//cron 으로 돌리니 자꾸 server가 죽음 why?
/*
const resultexec1 = exec('python Get_evChargerStatusInfo.py');
console.log ("python Get_evChargerStatusInfo.py")
resultexec1.stdout.on('data', function(ls_result){
    console.log(ls_result.toString());
})
*/

//10분에 한번씩 UpdateMongoDB하기 (feat. Get_evChargerStatusInfo.py)
//cron 으로 돌리니 자꾸 server가 죽음 ..
//8분간격 (딜레이보장안되니 10분했을때 딜레이생기면 update안되는 항목 생길수있음)
//var timer = setInterval(UpdateMongoDB,480000);
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
