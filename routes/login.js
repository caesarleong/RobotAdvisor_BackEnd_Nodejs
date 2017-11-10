var express = require('express');
var router = express.Router();

/* GET login page. */
router.get('/', function(req, res, next) {
	res.render('login', {
		title: 'Robot Advisor',
		err_msg: '',
	});
});

module.exports = router;