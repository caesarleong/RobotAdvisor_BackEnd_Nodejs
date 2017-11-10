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
		console.log(selected_date, selected_type);

		req.session.array_self_object = [];
		req.session.self_object.selected_type = selected_type;

		var options = {
			mode: 'text',
			pythonOptions: ['-u'],
			scriptPath: './py/etf',
			args: ['genRiskProfit', selected_date, selected_type]
		};

		PythonShell.run('genRiskProfit.py', options, function(err, results) {
			if (err) throw err;
			var fundlist = results[6].toString()

			//console.log("query done");

			res.render('etf_SelfSelection_SelectFund', {
				title: '基金篩選條件',
				date: selected_date,
				selected_type: selected_type,
				fundlist: fundlist
			});
		});
	}


});

module.exports = router;