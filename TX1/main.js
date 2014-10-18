//var theThingsAPI = require('thethingsio-api');  
//
//var KEY = 'voltage';
//var interval = 500;//ms
//
////create Client
//var client = theThingsAPI.createClient();
//
//
////The object to write.
//var object = {
//    "values":
//        [
//            {
//                "key": KEY,
//                "value": "100",
//                "units": "V",
//                "type": "temporal"
//            }
//        ]
//}
////write the object
//
//setInterval(function() {
//    object.values[0].value = Math.floor(Math.random()*100);
//    var req3 = client.thingWrite(object);
//    req3.on('response',function(res){
//        console.log('Write\n',res.statusCode,res.payload.toString() ,'\n\n');
//    });
//    req3.end();
//    console.log("send", object);
//},interval);

var mraa = require('mraa'); //require mraa
console.log('MRAA Version: ' + mraa.getVersion()); //write the mraa version to the console

var myDigitalPin6 = new mraa.Gpio(2); //setup digital read on Digital pin #6 (D6)
myDigitalPin6.dir(mraa.DIR_IN); //set the gpio direction to input

periodicActivity(); //call the periodicActivity function

function periodicActivity() //
{
  var myDigitalValue =  myDigitalPin6.read(); //read the digital value of the pin
  console.log('Gpio is ' + myDigitalValue); //write the read value out to the console
  setTimeout(periodicActivity,400); //call the indicated function after 1 second (1000 milliseconds)
}