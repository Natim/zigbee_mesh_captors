var mongoose = require('mongoose');

var measurementSchema = mongoose.Schema({
	sensorId: Number,
	timestamp: Number,
	value: Number
});

var Measurement = mongoose.model('Measurement', measurementSchema);
