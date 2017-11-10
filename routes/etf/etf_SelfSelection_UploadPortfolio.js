var express = require('express');
var router = express.Router();
var path = require("path");
var mysql = require('mysql');

var con = mysql.createConnection({
	host: "220.130.149.149",
	user: "root",
	password: "gis123",
	database: 'gis_db'
});

router.post('/', function(req, res, next) {
	if (!req.session.uname) {
		res.redirect('/login');
	} else {
		var index = req.body.pid;
		var data = req.session.array_self_object[index];
		console.log("inserting data:" + data.uname + "  " + data.time);
		con.query("insert into history_portfolio set ?", {
				uname: data.uname,
				uid: data.uid,
				generate_time: data.time,
				selected_date: data.selected_date.toString(),
				type: data.type,
				selected_type: data.selected_type,
				filter_type: data.filter_type,
				aum_id: data.aum_id,
				fund_result_id_str: data.fund_result_id_str,
				fund_result_name_str: data.fund_result_name_str,
				weights_str: data.weights_str,
				base64: data.base64,
				netvalue_str: data.netvalue_str,
				netvalue_3m_str: data.netvalue_3m_str,
				annualized_returnrate: data.annualized_returnrate
			},
			function(err, result, fields) {
				if (err) throw err;
				console.log("[db] 1 record inserted");
			}
		);
		res.render('etf_SelfSelection_ShowPortfolio2', {});

	}



});


module.exports = router;