var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
	if (!req.session.uname) {
		res.redirect('/login');
	} else {
		//create new rp100_object
		req.session.array_rp100_object = []
		req.session.rp100_object = {}
		req.session.rp100_object.uid = req.session.uid;
		req.session.rp100_object.uname = req.session.uname;
		req.session.rp100_object.time = Number(new Date());
		req.session.rp100_object.type = "RPS100";
		console.log("rp100_object inited:" + JSON.stringify(req.session.rp100_object));

		res.render(
			'etf_RPfilter', {
				title: '基金篩選條件'

			});
	}
});

module.exports = router;