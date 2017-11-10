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
		var Select_Date = Data.date;
		var blocks_1m = Data.blocks_1m;
		var blocks_3m = Data.blocks_3m;
		var blocks_6m = Data.blocks_6m;
		var blocks_1y = Data.blocks_1y;
		var blocks_2y = Data.blocks_2y;
		var blocks_3y = Data.blocks_3y;
		var strategy_1m = Data.strategy_1m;
		var strategy_3m = Data.strategy_3m;
		var strategy_6m = Data.strategy_6m;
		var strategy_1y = Data.strategy_1y;
		var strategy_2y = Data.strategy_2y;
		var strategy_3y = Data.strategy_3y;
		var selected_type = Data.selected_type;
		//var stock_list = Data.stock_list; // [ {id,name} *num]
		var aum_selected = Data.aum_selected; //25 144 23 777 

		//console.log("uma:" + stock_list);


		var finalCommand = {
			reqTopic: "/frontEnd/RPfilter/Filter",
			SelectDate: Select_Date,
			blocks_1m: blocks_1m,
			blocks_3m: blocks_3m,
			blocks_6m: blocks_6m,
			blocks_1y: blocks_1y,
			blocks_2y: blocks_2y,
			blocks_3y: blocks_3y,
			strategy_1m: strategy_1m,
			strategy_3m: strategy_3m,
			strategy_6m: strategy_6m,
			strategy_1y: strategy_1y,
			strategy_2y: strategy_2y,
			strategy_3y: strategy_3y,
			selected_type: selected_type,
			aum_selected: aum_selected

		};

		//append to rp100_object sess
		req.session.rp100_object.selected_date = Select_Date;
		req.session.rp100_object.selected_type = selected_type;
		req.session.rp100_object.blocks_1m = blocks_1m;
		req.session.rp100_object.blocks_3m = blocks_3m;
		req.session.rp100_object.blocks_6m = blocks_6m;
		req.session.rp100_object.blocks_1y = blocks_1y;
		req.session.rp100_object.blocks_2y = blocks_2y;
		req.session.rp100_object.blocks_3y = blocks_3y;
		req.session.rp100_object.strategy_1m = strategy_1m;
		req.session.rp100_object.strategy_3m = strategy_3m;
		req.session.rp100_object.strategy_6m = strategy_6m;
		req.session.rp100_object.strategy_1y = strategy_1y;
		req.session.rp100_object.strategy_2y = strategy_2y;
		req.session.rp100_object.strategy_3y = strategy_3y;
		req.session.rp100_object.aum_id = aum_selected.trim();

		//console.log(JSON.stringify(req.session.rp100_object));



		//console.log(JSON.stringify(finalCommand));

		var options = {
			mode: 'text',
			pythonOptions: ['-u'],
			scriptPath: './py/etf',
			args: ['Union&Intersection', JSON.stringify(finalCommand)]
		};

		var pyObj = PythonShell.run('Filter_UnionIntersection.py', options, function(err, results) {
			if (err) throw err;
			var resStr = results[0].toString().trim().split(' ');
			console.log(results);
			//console.log(results[1]);
			res.render('etf_RPfilter_NumSelect', {
				title: '風險收益法篩選頁面',
				fundList: resStr,
				initNum: results[1],
				Select_Date: Select_Date,
				aum_selected: aum_selected.trim()
			});
			pyObj.close
		});
	}



});
module.exports = router;