var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {

	if (req.session.uname) {
		res.render(
			'service_index', {});
	} else {
		res.redirect('/login');
	}

});

module.exports = router;