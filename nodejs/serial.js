//Handle Serial Communication
var serialport = require("serialport")
  ,SerialPort = serialport.SerialPort
  , db = require('./model/db')
  , mongoose = require('mongoose')
  , Measurement = mongoose.model('Measurement')
  , conf = require('./config')
  , serialPort = new SerialPort(conf.serial, {
      baudrate: 9600,
      buffersize: 576,
      parser: serialport.parsers.readline("\n")
    });

//Listen on Serials
serialPort.on("open", function () {
  console.log('Now listening on Serial ' + conf.serial);

  //When receiving data
  serialPort.on('data', function(data) {
    console.log('Received: ' + data);

    //Parse data
    data = data.split(',');
    if(data.length >= 2) {
      var arduino = data[0];
      var value = data[1];

      //Create a new document
      var val = new Measurement({
        sensorId: arduino,
        timestamp: Date.now(),
        value: value
      });

      //Insert it in Mongo
      val.save(function (err, data) {
        if (err) console.log(err);
        console.log(data);
        //Remove too old data
        var old = val.timestamp - 60000 ;
        Measurement.find().where('sensorId').equals(val.sensorId).where('timestamp').lt(old).remove().exec();
      });
    }

  });
});



