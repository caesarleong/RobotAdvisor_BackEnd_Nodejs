var express = require('express');
var path = require('path');
var favicon = require('serve-favicon');
var logger = require('morgan');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');
var app = express();
var session = require("express-session");


//Session
app.use(session({
  secret: 'secret-key',
  resave: true,
  saveUninitialized: true,
  cookie: {
    cookie: {
      expires: new Date(253402300000000)
    }
  }
}))

app.use(function(req, res, next) {
  res.locals.uid = req.session.uid;
  res.locals.uname = req.session.uname;
  res.locals.account = req.session.account;
  res.locals.pwd = req.session.pwd;
  res.locals.rank = req.session.rank;
  res.locals.rp100_object = req.session.rp100_object;
  res.locals.array_rp100_object = req.session.array_rp100_object;
  res.locals.self_object = req.session.self_object;
  res.locals.array_self_object = req.session.array_self_object;

  next();
});


//Router Settings
var home = require('./routes/index');
var users = require('./routes/users');
var service_index = require('./routes/service_index');
var login = require('./routes/login');
var logout = require('./routes/logout');
var login_submit = require('./routes/login_submit');
/** Mutual Fund **/

/** ETF **/
var etf_GenIndex = require('./routes/etf/etf_GenIndex');
var etf_date_compare = require('./routes/etf/etf_date_compare');
var etf_date_compare_show = require('./routes/etf/etf_date_compare_show');
var etf_RPfilter = require('./routes/etf/etf_RPfilter');
var etf_RPfilter_Calculate = require('./routes/etf/etf_RPfilter_Calculate');
var etf_RPfilter_Calculate_OnChange = require('./routes/etf/etf_RPfilter_Calculate_OnChange');
var etf_RPfilter_ProCorFilter = require('./routes/etf/etf_RPfilter_ProCorFilter');
var etf_RPfilter_GetXYfromSQL = require('./routes/etf/etf_RPfilter_GetXYfromSQL');
var etf_RPfilter_GoPortfolio = require('./routes/etf/etf_RPfilter_GoPortfolio');
var etf_setting4433 = require('./routes/etf/etf_4433_setting');
var etf_calculate4433 = require('./routes/etf/etf_4433_calculate');
var etf_4433_FundResult = require('./routes/etf/etf_4433_ProCorFilter');
var etf_re_RPfilter = require('./routes/etf/etf_re_RPfilter');
var etf_history = require('./routes/etf/etf_history');
var etf_RPfilter_UploadPortfolio = require('./routes/etf/etf_RPfilter_UploadPortfolio');
var etf_RPfilter_UpdatePortfolio = require('./routes/etf/etf_RPfilter_UpdatePortfolio'); //usage: history update
var etf_SelfSelection = require('./routes/etf/etf_SelfSelection');
var etf_SelfSelection_SelectFund = require('./routes/etf/etf_SelfSelection_SelectFund');
var etf_SelfSelection_GoPortfolio = require('./routes/etf/etf_SelfSelection_GoPortfolio');
var etf_SelfSelection_UploadPortfolio = require('./routes/etf/etf_SelfSelection_UploadPortfolio');

//View Engine Settings
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');

app.use(logger('dev'));
app.use(bodyParser.json({
  limit: '5mb'
}));
app.use(bodyParser.urlencoded({
  limit: '5mb',
  extended: true
}));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));


//Path Stack Control
app.use('/', home);
app.use('/service_index', service_index)
app.use('/users', users);
app.use('/login', login);
app.use('/logout', logout);
app.use('/login_submit', login_submit);

/** ETF **/
app.use('/etf', etf_GenIndex);
app.use('/etf_date_compare', etf_date_compare);
app.use('/etf_date_compare_show', etf_date_compare_show)
app.use('/etf_RPfilter_SelectDate', etf_RPfilter);
app.use('/etf_RPfilter_SelectBlocks', etf_RPfilter_GetXYfromSQL);
app.use('/etf_RPfilter_SelectBlocks_OnChange', etf_RPfilter_Calculate_OnChange)
app.use('/etf_RPfilter_SelectNum', etf_RPfilter_Calculate);
app.use('/etf_FundResult', etf_RPfilter_ProCorFilter);
app.use('/etf_Portfolio', etf_RPfilter_GoPortfolio);
app.use('/etf_4433_FundResult', etf_4433_FundResult);
app.use('/etf_4433_Setting', etf_setting4433);
app.use('/etf_4433_SelectNum', etf_calculate4433);
app.use('/etf_re_RPfilter', etf_re_RPfilter);
app.use('/etf_history', etf_history);
app.use('/etf_RPfilter_UploadPortfolio', etf_RPfilter_UploadPortfolio);
app.use('/etf_RPfilter_UpdatePortfolio', etf_RPfilter_UpdatePortfolio);
app.use('/etf_SelfSelection', etf_SelfSelection);
app.use('/etf_SelfSelection_SelectFund', etf_SelfSelection_SelectFund);
app.use('/etf_SelfSelection_GoPortfolio', etf_SelfSelection_GoPortfolio);
app.use('/etf_SelfSelection_UploadPortfolio', etf_SelfSelection_UploadPortfolio);

//Error Handlers
app.use(function(req, res, next) {
  var err = new Error('Not Found');
  err.status = 404;
  next(err);
});

//Development error handler
// print stacktrace
if (app.get('env') === 'development') {
  app.use(function(err, req, res, next) {
    res.status(err.status || 500);
    res.render('error', {
      message: err.message,
      error: err
    });
  });
}

//Production error handler
// no stacktraces leaked to user
app.use(function(err, req, res, next) {
  res.status(err.status || 500);
  res.render('error', {
    message: err.message,
    error: {}
  });
});

module.exports = app;