Node.Js Example
===============

Small example on how to use Node.Js with an arduino sending data over 
serial.

It stores data coming from an arduino and make them available through http.

#Requirements

* Node.Js
* MongoDB

#Installation

* Install dependencies: `npm install`.
* Run: `node server.js`.

#Configuration

The following parameters can be configured in config.json.
Default values should be overwritten to fit your settings.

<table>
  <tr>
    <th>Parameter</th><th>Default value</th><th>Comment</th>
  </tr>
  <tr>
    <td>host</td><td>localhost</td><td>Domain or IP on which the server is running.</td>
  </tr>
  <tr>
    <td>port</td><td>8080</td><td>Port to be used.</td>
  </tr>
  <tr>
    <td>serial</td><td>/dev/ttyACM0</td><td>The serial port to listen to.</td>
  </tr>
</table>

#Input data

The program listen for data on the serial. We assume data to be a string with the following structure:
```
"sensorId, sensorValue\n"
```
Don't forget **\n** as it is used to delimit each frame.

#API Description

You can retrieve data on /values with parameter **sensor** containing the id of the sensor.
For example, to get all data concerning sensor 1: **curl -XGET localhost:8080/values?sensor=1**
```javascript
{
  "allValues": [
    {
      "sensorId": 1,
      "timestamp": 1389344261521,
      "value": 168,
      "_id": "52cfb605dadbb2166b00000f",
      "__v": 0
    },
    {
      "sensorId": 1,
      "timestamp": 1389344255521,
      "value": 167,
      "_id": "52cfb5ffdadbb2166b00000e",
      "__v": 0
    },
    {
      "sensorId": 1,
      "timestamp": 1389344247518,
      "value": 168,
      "_id": "52cfb5f7dadbb2166b00000d",
      "__v": 0
    }
  ]
}
```

###Data Structure

Data stored in Mongo have the following fields:
* timestamp
* sensorId
* value

#About

This example is taken from the project vvision/R4D2 and has been 
slightly modified.

