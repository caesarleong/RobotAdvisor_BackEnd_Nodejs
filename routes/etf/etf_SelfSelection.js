var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
	if (!req.session.uname) {
		res.redirect('/login');
	} else {
		//create new rp100_object
		req.session.array_self_object = []
		req.session.self_object = {}
		req.session.self_object.uid = req.session.uid;
		req.session.self_object.uname = req.session.uname;
		req.session.self_object.time = Number(new Date());
		req.session.self_object.type = "Self-Selection";
		console.log("self_object inited:" + JSON.stringify(req.session.self_object));

		res.render(
			'etf_SelfSelection', {
				title: '基金篩選條件'

			});
	}
});

module.exports = router;