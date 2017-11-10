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
	if (req.session.uname) {
		uname = req.session.uname;
		uid = req.session.uid;
		con.query("use gis_db");
		//delete

		var sql = "DELETE FROM history_portfolio WHERE _id = '" + req.body.pid + "'";
		con.query(sql, function(err, result) {
			if (err) throw err;
			console.log("Number of records deleted: " + result.affectedRows);
		});


		//select
		var sql = "select * from history_portfolio where uid=" + req.session.uid + " order by generate_time desc ";
		con.query(sql,
			function(err, result, fields) {
				if (err) throw err;
				var arr_obj = [];
				for (var i in result) {
					var json_obj = {
						_id: result[i]._id,
						generate_time: result[i].generate_time,
						selected_date: result[i].selected_date,
						selected_type: result[i].selected_type,
						filter_type: result[i].filter_type,
						aum_id: result[i].aum_id,
						fund_result_id: result[i].fund_result_id_str.split(" "),
						fund_result_name: result[i].fund_result_name_str.split("||"),
						weights: result[i].weights_str.split(" "),
						base64: result[i].base64,
						type: result[i].type,
						annualized_returnrate: result[i].annualized_returnrate,
						netvalue: result[i].netvalue_str.split(" "),
						netvalue_3m: result[i].netvalue_3m_str.split(" ")
					}
					arr_obj.push(json_obj);
				}
				//console.log(arr_obj);
				res.render('etf_history', {
					"arr_obj": arr_obj
				});
			}
		);


	} else {
		res.redirect('/login');
	}



});


module.exports = router;