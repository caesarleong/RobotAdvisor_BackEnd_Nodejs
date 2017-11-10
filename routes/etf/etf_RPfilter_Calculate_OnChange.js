var express = require('express');
var router = express.Router();
var path = require("path");
var uuid = require('node-uuid');
var PythonShell = require('python-shell');

router.post('/', function(req, res, next) {
	if (!req.session.uname) {
		res.redirect('/login');	
	} else {
		var Data = req.body.Selection_OnChange;
		Data = JSON.parse(Data);
		var selected_date = Data.date;
		var type = Data.type;
		var time_interval = 260;
		var sma_day = 0;
		console.log(type);
		if (type == "ma10")
			sma_day = 10;
		else if (type == "ma20")
			sma_day = 20;
		console.log(sma_day);

		var options = {
			mode: 'text',
			pythonOptions: ['-u'],
			scriptPath: './py/etf',
			args: ['genRiskProfit', selected_date, time_interval, sma_day]
		};

		PythonShell.run('genRiskProfit.py', options, function(err, results) {
			if (err) throw err;

			var xy = results.toString()
				// console.log(xy);

			res.render('etf_RPfilter_100Selection', {
				title: '基金篩選條件',
				data: xy,
				date: selected_date,
				sma_day: sma_day
			});
		});
	}
	


});
module.exports = router;