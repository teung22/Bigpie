const express = require('express')
const morgan = require('morgan')
const path = require('path')
const app = express()
const bodyParser = require('body-parser')
const cookieParser = require('cookie-parser')
const router = express.Router()
const spawn = require('child_process').spawn


app.set('port', process.env.PORT || 8000)

app.use(morgan('dev'))
app.use(bodyParser.json())
app.use(bodyParser.urlencoded({extended: false}))
app.use(cookieParser())
app.use(express.static(path.join(__dirname, 'public')))



const mongoose = require('mongoose')
mongoose.connect('mongodb://3.36.89.204:27017/bigpie')

var mongo = require('./routes/mongo.js')
app.use('/', mongo)

// var mysql = require('./routes/mysql.js')
// app.use('/', mysql)

app.listen(app.get('port'), () => {
  console.log('8000 Port : Server started...')
});
