
module.exports = function()
{
  var mraa = require("mraa"); //require mraa
  console.log('MRAA Version: ' + mraa.getVersion()); //write the mraa version to the console

  var motorADirection = new mraa.Gpio(4);
  motorADirection.dir(mraa.DIR_OUT); //set the gpio direction to output
  motorADirection.write(0);

  var motorBDirection = new mraa.Gpio(7);
  motorBDirection.dir(mraa.DIR_OUT); //set the gpio direction to output
  motorBDirection.write(0);

  //var motorAPower = new mraa.Pwm(5);
  //motorAPower.period_us(2000);
  var motorAPower = new mraa.Gpio(5);
  motorAPower.dir(mraa.DIR_OUT); //set the gpio direction to output

  var motorBPower = new mraa.Gpio(6);
  motorBPower.dir(mraa.DIR_OUT); //set the gpio direction to output

  function doStart()
  {
      console.log('Motors: Go!');
      motorAPower.write(1);
      motorBPower.write(1);
      setTimeout(doStop, 5000);
  }

  function doStop()
  {
      console.log('Motors: Stop!');
      motorAPower.write(0);
      motorBPower.write(0);
  }

  function action(actionText)
  {
    if (actionText == 'go')
    {
        doStart();
    }
    else if (actionText == 'stop')
    {
        doStop();
    }
  }

  return {
        doAction: action
  };
}();