var express = require('express');
var router = express.Router();
var path = require("path");
var uuid = require('node-uuid');
var PythonShell = require('python-shell');

router.post('/', function(req, res, next) {
	if (!req.session.uname) {
		res.redirect('/login');
	} else {
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
			aum_selected: Data.aum_selected

		};

		if (Data.corNum == 0) {
			req.session.rp100_object.filter_type = "全高收益篩選";
		} else if (Data.profitNum == 0) {
			req.session.rp100_object.filter_type = "全低關聯篩選";
		} else {
			req.session.rp100_object.filter_type = "綜合性篩選";
		}


		console.log(JSON.stringify(finalCommand));

		var options = {
			mode: 'text',
			pythonOptions: ['-u'],
			scriptPath: './py/etf',
			args: ['ProCorFilter', JSON.stringify(finalCommand)]
		};

		PythonShell.run('Filter_ProCor.py', options, function(err, results) {
			if (err) throw err;
			// results[0]=fundNameList  results[3]=corMatrix   results[1]=resultSet  results[2]=FundNameStr
			console.log(results);
			res.render('etf_RPfilter_FundResult', {
				title: '風險收益法 基金篩選結果',
				fund_id: results[0],
				full_fund_id: results[1],
				aum_id: results[2],
				full_aum_id: results[3],
				SelectDate: Data.date
			});
		});
	}



});
module.exports = router;