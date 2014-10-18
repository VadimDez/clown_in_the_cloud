var theThingsAPI = require('thethingsio-api');  

//create Client
var client = theThingsAPI.createClient();

var mraa = require('mraa');

var button = new mraa.Gpio(2),
    rotationSensorPin = new mraa.Aio(0),
    lastRotation = 500;

button.dir(mraa.DIR_IN);


main();

function main() {
    
    var pressed =  button.read(); 
    console.log('Pressed: ' + pressed);
    
    var rotationAngle = rotationSensorPin.read();
    console.log('Rotation: ' + rotationAngle);
    
    var req3 = client.thingWrite({  
        "values":
            [
                {
                    "key": "motion",
                    "value": (pressed === 1) ? "go" : "stop",
                    "units": "",
                    "type": "temporal"
                },
                {
                    "key": "turn",
                    "value" : rotation(rotationAngle),
                    "units": "",
                    "type": "temporal"
                }
            ]
    });
    req3.on('response',function(res){
        lastRotation = rotationAngle;
    });
    req3.end();
    
  setTimeout(main,400);
}

function rotation(rotationAngle) {
    if (rotationAngle)
    return "straight";
}