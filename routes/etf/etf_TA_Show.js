var express = require('express');
var router = express.Router();
var path = require("path");
var uuid = require('node-uuid');
var mqtt = require('mqtt');
var SECURE_CERT = path.join(__dirname, '../key', 'oring-cert.pem');
var options = {
	certPath: SECURE_CERT,
	rejectUnauthorized: false,
	username: 'test',
	password: 'test',
	clientId: 'TA_Show.js',
};
var mqttClient = mqtt.connect('mqtts://140.119.19.243:8883', options);

mqttClient.on('connect', function() {
	mqttClient.subscribe('/fund/TA/req');
	mqttClient.subscribe('/fund/TA/res');
});

router.post('/', function(req, res, next) {
	var TA_Data = req.body.TASelection;
	TA_Data = JSON.parse(TA_Data);

	var req_type = TA_Data.req_type;
	var TA_Date = TA_Data.Date;
	var Select_TA = TA_Data.TA;


	var finalCommand = {
		req_type: req_type,
		TA_Date: TA_Date,
		Select_TA: Select_TA,
		requestId: uuid.v4(),
		user: 'admin',
	};

	console.log(JSON.stringify(finalCommand));
	var mqttmsg = JSON.stringify(finalCommand);


	mqttClient.publish('/fund/TA/req', mqttmsg);


	mqttClient.on('message', handleMqttMsg);

	function handleMqttMsg(topic, message) {
		try {
			var val = JSON.parse(message);
			//data type:     "req_type" : "TA_filter","Date" : Select_date,"TA" : Select_TA
			switch (topic) {
				case "/fund/TA/req":
					console.log("got message from fund/TA/req ");
					if (val.requestId === finalCommand.requestId) {

						/** MongoDB Query **/

						/** Render to Next Page **/
						res.render('TA_Show', {
							title: '技術指標分析',
							"Select_date": val.TA_Date,
							"Select_TA": val.Select_TA
						});
						mqttClient.removeListener('message', handleMqttMsg);
						console.log("TA_Show.js: removeListener done")
					}
					break;
				default:
					console.log(message.toString());
					break;
			}
		} catch (err) {
			console.log('cannot parse message to json object : ', err);
		}

	}

});
module.exports = router;