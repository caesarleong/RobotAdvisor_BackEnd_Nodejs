var express = require('express');
var router = express.Router();
var path = require("path");
var mysql = require('mysql');
var PythonShell = require('python-shell');

router.post('/', function(req, res, next) {
	if (!req.session.uname) {
		res.redirect('/login');
	} else {
		var Data = req.body.Selection;
		Data = JSON.parse(Data);
		var selected_date = Data.date;
		var selected_type = Data.type;
		//console.log(selected_date, selected_type);

		var options = {
			mode: 'text',
			pythonOptions: ['-u'],
			scriptPath: './py/etf',
			args: ['genRiskProfit', selected_date, selected_type]
		};

		PythonShell.run('genRiskProfit.py', options, function(err, results) {
			if (err) throw err;
			console.log(results);

			var point_1m = results[0].toString()
			var point_3m = results[1].toString()
			var point_6m = results[2].toString()
			var point_1y = results[3].toString()
			var point_2y = results[4].toString()
			var point_3y = results[5].toString()
			var fundlist = results[6].toString()
				//var point_stock = results[6].toString() // [ [{x,y}*30] *num]
				//var stock_list = results[7].toString() // [ {id,name} *num]
				//console.log("query done");

			res.render('etf_date_compare_100Selection', {
				title: '基金篩選條件',
				point_1m: point_1m,
				point_3m: point_3m,
				point_6m: point_6m,
				point_1y: point_1y,
				point_2y: point_2y,
				point_3y: point_3y,
				date: selected_date,
				selected_type: selected_type,
				fundlist: fundlist
			});
		});
	}


});

module.exports = router;