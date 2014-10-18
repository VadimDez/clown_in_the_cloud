var theThingsAPI = require('thethingsio-api');
var motion = require('./motion');

console.log("Hello");


var motionKEY = 'motion';

//create Client
var client = theThingsAPI.createClient();


function readMotions()
{
    //read latest write
    var req1 = client.thingReadLatest(motionKEY);

    //event fired when the response arrives
    req1.on('response',function(res){
        console.log('Read Latest\n',res.statusCode, res.payload.toString(),'\n\n');
        if (res.statusCode == 200 && res.payload !== undefined)
        {
            var payload = JSON.parse(res.payload);
            motion.doAction(payload.data[0].value);
        }
    });
    req1.end();
}

motion.doAction("stop");

setInterval(readMotions, 1000);