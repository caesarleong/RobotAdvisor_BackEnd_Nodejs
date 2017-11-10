var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
	res.render('etf_4433_setting', {
		title: 'Robot Advisor'
	});
});

module.exports = router;
