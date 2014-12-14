var theThingsAPI = require('thethingsio-api');  

//create Client
var client = theThingsAPI.createClient();
var mraa = require('mraa');
var button = new mraa.Gpio(2),
    rotationSensorPin = new mraa.Aio(0),
    lastRotation = 500, // center
    touchSensor = new mraa.Gpio(4),
    jsonToSend = {};

touchSensor.dir(mraa.DIR_IN);
button.dir(mraa.DIR_IN);
main();

function main() {
    var pressed =  button.read(),
        rotationAngle = rotationSensorPin.read(),
        newJson = {
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
                    },
                    {
                        "key": "light",
                        "value": touchSensor.read(),
                        "units": "",
                        "type": "temporal"
                    }
                ]
        };

    if (newJson !== jsonToSend) {
        jsonToSend = newJson;
        var req3 = client.thingWrite(jsonToSend);
        req3.on('response',function(res) {
            lastRotation = rotationAngle;
        });
        req3.end();
    }
    
  setTimeout(main,400);
}

/**
 * Decide rotation
 */
function rotation(rotationAngle) {
    if (350 < rotationAngle && rotationAngle < 650)
        return "straight";
    else if (rotationAngle > 650)
        return "left";
    
    return "right";
}