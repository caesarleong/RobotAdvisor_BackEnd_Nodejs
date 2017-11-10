var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {

	if (req.session.uname) {
		res.render(
			'etf_GenIndex', {
				title: 'ETF'
			});
	} else {
		res.redirect('/login');
	}
});

module.exports = router;