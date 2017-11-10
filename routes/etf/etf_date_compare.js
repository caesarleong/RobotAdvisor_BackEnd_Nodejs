var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
	res.render('etf_date_compare_selectDate');
});

module.exports = router;