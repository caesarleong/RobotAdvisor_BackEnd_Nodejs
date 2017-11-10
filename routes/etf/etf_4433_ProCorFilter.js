var express = require('express');
var router = express.Router();
var path = require("path");
var uuid = require('node-uuid');
var PythonShell = require('python-shell');

router.post('/', function(req, res, next) {
	var Data = req.body.Selection;
	Data = JSON.parse(Data);
	var finalCommand = {
		reqTopic: "/frontEnd/RPfilter/ProCor",
		SelectDate: Data.date,
		fundList: Data.fundList,
		requestId: uuid.v4(),
		user: 'admin',
		type: Data.type,
		corNum: Data.corNum,
		profitNum: Data.profitNum,
		uma_selected: Data.uma_selected

	};

	//console.log(JSON.stringify(finalCommand));

	var options = {
		mode: 'text',
		pythonOptions: ['-u'],
		scriptPath: './py/etf',
		args: ['ProCorFilter', JSON.stringify(finalCommand)]
	};

	PythonShell.run('4433_Filter_ProCor.py', options, function(err, results) {
		if (err) throw err;
		// results[0]=fundNameList  results[3]=corMatrix   results[1]=resultSet  results[2]=FundNameStr
		//console.log(results);
		res.render('etf_RPfilter_FundResult', {
			title: '風險收益法 基金篩選結果',
			fundidList: results[0],
			name: results[2],
			resultStr: results[1].toString(),
			SelectDate: Data.date,
			uma_selected: Data.uma_selected
		});
	});



});
module.exports = router;