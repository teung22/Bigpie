const express = require('express');
const router = express.Router();
const request = require('request');
const bodyParser = require('body-parser')
const CircularJSON = require('circular-json')
const env = require("dotenv").config({ path:"/data/node/config/.env"});
//********************************************
router.use(bodyParser.json())
router.use(bodyParser.urlencoded({extended : false}))
router.use(express.json())
router.use(express.urlencoded({extended : true}))
//***********************************************

var mysql = require("sync-mysql") ;

var connection = new mysql({
   host : process.env.host,
   user : process.env.user,
   password : process.env.password,
   database : process.env.database
})


var app = express();
let urls =''

//  ;
router.get('/stgecode', function(req,res){
     input = req.query.code ;
  var sql = " SELECT A.ZSCODE AS ZSCODE , B.STG_NAME AS NAME , B.STG_LA AS LA , B.STG_LO AS LO"
      sql = sql + " FROM  StgInfo A , StgInfoDetail B"
      sql = sql + " WHERE A.stg_id = B.STG_ID  AND A.ZSCODE =?";

    let  rows = connection.query(sql,[input] );
      // if(!err){
           console.log('input code', input) ;
           console.log('The Codes is :', sql);
           console.log('The Codes is :', rows);
           var template = `
           <!doctype html>
           <html>
           <head>
           <title>Result</title>
           <meta charset="utf-8">
           </head>
           <body>
           <table border="1" margin:auto; text-align:center>
           <tr>
           <th>Stage_Name</th>
           <th>zscode</th>
           <th>Stage_la</th>
           <th>Stage_lo</th>
           </tr>
           `;
           for(var i=0; i<rows.length ;i++){
           template +=`
           <tr>
           <th>${rows[i]['NAME']}</th>
           <th>${rows[i]['ZSCODE']}</th>
           <th>${rows[i]['LA']}</th>
           <th>${rows[i]['LO']}</th>
           </tr>
           `
           }
           template +=`
           </table>
           </body>
           </html>
           `;
           res.writeHead(200);
           res.end(template);
       // }else{
       //   console.log('SQL', sql,input) ;
       //   console.log('Error while perforim Query') ;
       // }
}) ;

router.get('/stggetdata', function(req,res) {
  input = req.query.input ;

  var sql = " select a.zscode AS ZSCODE ,a.stg_id AS STG_ID, b.stg_name AS NAME, b.stg_la AS LA , b.stg_lo AS LO, count(c.stg_id) as CNT"
      sql = sql + " from StgInfo a ,( "
      sql = sql +" SELECT stg_id, stg_name, stg_la, stg_lo FROM StgInfoDetail WHERE stg_name LIKE '%"+ input +"%' limit 1 )  AS b left join prfDetail c   "
      sql = sql +" on c.stg_id = b.stg_id and c.prf_state='공연중' and c.prf_stging ='Y'"
      sql = sql +"where a.stg_id = b.stg_id  group by c.stg_id  "
    rows = connection.query(sql,[input] );
// console.log(rows) ;
return res.json(rows) ;
console.log('input value', input) ;

  })

router.post("/stageid",function(req,res) {

  var id = req.body.id ;
  // console.log(id) ;
  console.log(CircularJSON.stringify(req.body))
  sql = " select a.prf_name, b.stg_name , b.prf_from, b.prf_to, b.prf_cast ,b.prf_runtime,a.prf_poster, b.stg_distance"
  sql = sql + " from prfList a, prfDetail b "
  sql = sql+" where a.prf_id =  b.prf_id and  b.prf_state='공연중'  and b.prf_stging='Y'and b.stg_id =?"

  rows = connection.query(sql,[id]);
  var template = `
  <!doctype html>
  <html>
  <head>
  <title>Result</title>
  <link rel="stylesheet" href="index.css">
  <meta charset="utf-8">
  </head>
  <body>
  <table  margin:auto; text-align:center>
  <tr>
  <th id="prfhead">포스터</th>
  <th id="prfhead">공연명</th>
  <th id="prfhead">공연장</th>
  <th id="prfhead">공연기간</th>
  <th id="prfhead">출연진</th>
  <th id="prfhead">공연시간</th>
  <th id="prfhead">공연요일</th>
  </tr>
  `;
  for(var i=0; i<rows.length ;i++){
  template +=`
    <tr>
      <td id="pfmtd" align=center><img src=${rows[i]['prf_poster']} width=50% , height=50%></td>
      <td id="pfmtd">${rows[i]['prf_name']}</td>
      <td id="pfmtd">${rows[i]['stg_name']}</td>
      <td id="pfmtd">${rows[i]['prf_from']}~${rows[i]['prf_to']}</td>
      <td id="pfmtd">${rows[i]['prf_cast']}</td>
      <td id="pfmtd">${rows[i]['prf_runtime']}</td>
      <td id="pfmtd">${rows[i]['stg_distance']}</td>
    </tr>
  `
  }
  template +=`
  </table>
  </body>
  </html>
  `;
  res.writeHead(200);
  res.end(template);
})

router.get('/getPrfInfo',function(req,res) {

  input = req.query.input ;
  cnt=req.query.cnt ;
     // console.log(input) ;
  // sql = " select a.prf_name, b.stg_name , b.prf_from, b.prf_to, b.prf_cast ,b.prf_runtime,a.prf_poster, b.stg_distance"
  // sql = sql + " from prfList a, prfDetail b "
  // sql = sql+" where a.prf_id =  b.prf_id and  b.prf_state='공연중'  and b.prf_stging='Y'and b.stg_id =?"

  sql = " select a.prf_name, b.stg_name , b.prf_from, b.prf_to, b.prf_cast ,b.prf_runtime,a.prf_poster, b.stg_distance,c.prf_runm,c.prf_seatcnt "
  sql = sql + " from prfList a, prfDetail b left Join  prfBoxOffice  c on b.prf_id = c.prf_id "
  sql = sql + "  where a.prf_id =  b.prf_id and  b.prf_state='공연중'  and b.prf_stging='Y'and b.stg_id =?"
  sql = sql + " order by c.prf_runm desc "

  rows = connection.query(sql,[input]);
  var template = `
    <!doctype html>
    <html>
    <head>
    <link rel="stylesheet" href="index.css">
    <title>공연정보</title>
    <meta charset="utf-8">
    </head>
    <body>
    <table id="evlist01" margin:auto; text-align:center>
    `;
     if(cnt==0){
       template +=`<tr>
       <th id="pfmtitle" colspan=2> 오늘은 공연이 없습니다.</th>
       </tr>
       `;
     }else if(cnt>=3){
        template +=`<tr>
        <th id="pfmtitle" colspan=2> 오늘 총 ${cnt}개의 공연이 있어 혼잡이 예상됩니다.<br> 여유로운 충전소를 찾으세요!</th>
        </tr>
        `;
    }else{
      template +=`<tr>
        <th id="pfmtitle" colspan=2> 오늘 총 ${cnt}개의 공연이 있습니다.</th>
      </tr>
        `;
      }
  for(var i=0; i<rows.length ;i++){
  template +=`
    <tr>
    <th id="pfmth" colspan=2>${rows[i]['prf_name']}</th>
    </tr>`

    if(rows[i]['prf_runm']!=null){
      template +=`
      <tr>
      <th id="pfmbox" colspan=2>
      예매순위 : ${rows[i]['prf_runm']} / 좌석수 : ${rows[i]['prf_seatcnt']}
     </th></tr>
      `
    }

    template +=`
    <tr>
    <td id="pfmtd">
    <img src=${rows[i]['prf_poster']}  style="height:120px"></td>
     <td rowpan=5  id="pfmtd" ">
     <ul>
     <li><b>${rows[i]['stg_name']}</b> </li>
     <li>${rows[i]['prf_from']}~ ${rows[i]['prf_to']} </li>
     <li>${rows[i]['prf_cast']} </li>
     <li>${rows[i]['prf_runtime']}</li>
     <li>${rows[i]['stg_distance']}</li>
     </ul>
     </td>
    </tr>
    `
    }
    template +=`
    <tr><td colspan=2>※출처 : 공연예술종합전산망(KOPIS)</td></tr>
    </table>
    </body>
    </html>
    `;
  res.writeHead(200);
  res.end(template);
})

// connection.end();
module.exports = router;
