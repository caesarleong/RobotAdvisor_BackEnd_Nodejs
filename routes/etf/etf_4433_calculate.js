var express = require('express');
var router = express.Router();
var path = require("path");
var uuid = require('node-uuid');
var PythonShell = require('python-shell');

router.post('/', function(req, res, next) {
	var jsonData = req.body.Selection;
	jsonData = JSON.parse(jsonData);

	var finalCommand = {
		reqTopic: "/frontEnd/4433/calculate",
		selectDate: jsonData.date,
		rank_3m: jsonData.rank_3m,
		rank_6m: jsonData.rank_6m,
		rank_1y: jsonData.rank_1y,
		rank_2y: jsonData.rank_2y,
		rank_3y: jsonData.rank_3y,
		rank_5y: jsonData.rank_5y

	};

	//console.log(JSON.stringify(finalCommand));

	var options = {
		mode: 'text',
		pythonOptions: ['-u'],
		scriptPath: './py/etf',
		args: ['4433', JSON.stringify(finalCommand)]
	};

	PythonShell.run('4433.py', options, function(err, results) {
		if (err) throw err;
		console.log(results);
		var resStr = results[0].toString().trim().split(' ');
		res.render('etf_4433_NumSelect', {
			fundList: resStr,
			Select_Date: jsonData.date
		});
	});



});
module.exports = router;