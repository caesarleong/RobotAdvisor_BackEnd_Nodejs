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

		//FundResultID is an array.
		var finalCommand = {
			SelectDate: Data.date,
			FundResultID: Data.FundResultID
		};
		console.log("[GoPortfolio]" + JSON.stringify(finalCommand));

		var options = {
			mode: 'text',
			pythonOptions: ['-u'],
			scriptPath: './py/etf',
			args: [JSON.stringify(finalCommand)]
		};


		var pyObj = PythonShell.run('portfolio_entry.py', options, function(err, results) {
			if (err) throw err;
			//console.log(results);

			var b64code = results[0].toString().slice(2, -1);
			var fundResultID = results[1].trim().split(" ");
			var fundResultName = results[2].split("||"); //名字中有空白 另外處理
			var weights = results[3].trim().split(" ");
			var annualized_returnrate = results[4];
			var expected_return = results[5];
			var netvalue = results[6].trim().split(" ");
			var netvalue_3m = results[7].trim().split(" ");

			req.session.rp100_object.base64 = b64code;
			req.session.rp100_object.fund_result_id = fundResultID;
			req.session.rp100_object.fund_result_name = fundResultName;
			req.session.rp100_object.weights = weights;
			req.session.rp100_object.fund_result_id_str = results[1].trim();
			req.session.rp100_object.fund_result_name_str = results[2];
			req.session.rp100_object.weights_str = results[3].trim();
			req.session.rp100_object.annualized_returnrate = parseFloat(annualized_returnrate);
			req.session.rp100_object.expected_return = expected_return;
			req.session.rp100_object.netvalue = netvalue;
			req.session.rp100_object.netvalue_3m = netvalue_3m;
			req.session.rp100_object.netvalue_str = results[6].trim();
			req.session.rp100_object.netvalue_3m_str = results[7].trim();

			//append this_time_obj to sess array
			req.session.array_rp100_object.push(req.session.rp100_object);

			//console.log(req.session.array_rp100_object);

			//#write file to log
			var fs = require('fs');
			var current_time = new Date();
			var ipAddress;
			var headers = req.headers;
			var forwardedIpsStr = headers['x - real - ip'] || headers['x - forwarded -for'];
			forwardedIpsStr ? ipAddress = forwardedIpsStr : ipAddress = null;
			if (!ipAddress) {
				ipAddress = req.connection.remoteAddress;
			}
			fs.appendFile('./logs/portfolio.txt', current_time + " || " + ipAddress + " || " + req.session.account + " || " + req.session.rp100_object.selected_type + "\n", function(err) {
				if (err) throw err;
				console.log('log saved!');
			});

			return res.render('etf_RPfilter_ShowPortfolio2', {
				title: '風險收益法 效益前緣',
				base64: b64code,
				SelectDate: Data.date
			});
			pyObj.close


		});
	}
});
module.exports = router;