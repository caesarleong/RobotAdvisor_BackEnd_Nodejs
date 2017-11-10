var express = require('express');
var router = express.Router();
var path = require("path");
var mysql = require('mysql');

//using MySQL
//using MySQL
var con = mysql.createConnection({
	host: "220.130.149.149",
	user: "root",
	password: "gis123",
	database: "gis_db",
	port: 3306
});

router.post('/', function(req, res, next) {
	var id = req.body.login_account;
	var pwd = req.body.login_pwd;
	var success_userid;

	con.query("select * from user where account = ?", [id],
		function(err, result) {
			if (err) throw err;

			if (result == "" || pwd != result[0].pwd) { //login wrong
				console.log("帳號密碼登入錯誤");
				res.render('login', {
					err_msg: '請輸入正確帳號及密碼'
				});
			} else { //login success
				req.session.uid = result[0].id;
				req.session.uname = result[0].name;
				req.session.account = result[0].account;
				req.session.pwd = result[0].pwd;
				req.session.rank = result[0].rank;

				var current_time = new Date();
				var ipAddress;
				var headers = req.headers;
				var forwardedIpsStr = headers['x - real - ip'] || headers['x - forwarded -for'];
				forwardedIpsStr ? ipAddress = forwardedIpsStr : ipAddress = null;
				if (!ipAddress) {
					ipAddress = req.connection.remoteAddress;
				}

				var login_record = "[SystemLogin] " + current_time + " " + ipAddress + " acc:" + req.session.account;
				console.log("======================");
				console.info('\x1b[33m%s\x1b[0m', login_record);
				console.log("======================");


				var fs = require('fs');
				fs.appendFile('./logs/login.txt', current_time + " || " + ipAddress + " || " + req.session.account + "\n", function(err) {
					if (err) throw err;
					console.log('log saved!');
				});

				res.redirect('/');
			}
		}
	);
});


module.exports = router;