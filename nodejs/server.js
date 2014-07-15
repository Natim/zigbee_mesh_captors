var express = require('express')
  , app = express()
  , fs = require('fs')
  , db = require('./model/db')
  , mongoose = require('mongoose')
  , Measurement = mongoose.model('Measurement')
  , conf = require('./config')
  , serial = require('./serial');

app.listen(conf.port, conf.host, function () {
  console.log('Server running on ' + conf.host + ':' + conf.port);
});

app.get('/values', function(req, res, next) {
  var id = req.query.sensor;
  if(id) {
    //Find 3 most recent measurements (Requested by app programmer).
    Measurement.find({sensorId: id}).sort({timestamp: 'desc'}).limit(3).exec(function(err, docs) {
		  if(err) console.error(err);
		  console.log(docs);
		  if(docs) {
		    res.send({allValues: docs});
		  } else {
		    res.send({allValues: null});
		  }
	  });
	} else {
	  res.send({allValues: null});
	}
});

