# RNBO-RPi-LEDseq

You've just made your own desktop synthesizer with RNBO and the Raspberry Pi, you're ready to switch the lights off and jam out - but there's no visual feedback... If there's a bleep in a dark studio but there's no pulses of twinkling light - did it even happen?

> ⚙️ *Before attempting this tutorial, make sure you're already familiar with the basics of exporting your RNBO patchers to the RPi and that your audio interface is working correctly with it.*

## Things you'll need  

* 8x through-hole LEDs
* 8x 220 ohm resistors[^1]
* 1x 12mm push button momentary switch (optional)
* Breadboard
* Hook up wires

We'll start by exporting the following patcher to the Raspberry Pi target:​

We're going to use the LEDs to light up the current step of the sequence. If you've also got a momentary push button handy we'll add that as a little transport control start/stop button.

We'll write a quick python script on the Raspberry Pi to use alongside the rnbo runner that's running the sequencer patcher.

ssh in, or connect up a keyboard and monitor. We'll use a library that should already be on your RPi image called `gpiozero` and another for communicating with the runner via OSC. You can use any OSC library you like, this example will use `pyliblo3`. We've used this library before - so if you've done this in a previous tutorial - you can skip this step.

To install `pyliblo3` run the following two commands from the terminal on your RPi.

```bash
sudo apt install liblo-dev
pip install pyliblo3
```

Now `sudo poweroff` the RPi, and disconnect the power. Let's create our circuit:

## Running the script
Power up the Pi again and run the script

```bash
python RNBO-RPi-LEDseq.py
```

The script will start the transport rolling, you should be able to turn the transport on and off using the button. Try using `rnbo.remote` to toggle the transport also - you should see the state reflected in the `attrui` whether you use the button or the toggle.

If you want to control the step values, you can open the Raspberry Pi Debug Interface to control the parameters.

[^1]: this is a general approximate resistor value for these current limiting resistors (without them, you can burn out your pins on your RPi or blow the LEDs) if you really want to be precise, this tool from digikey is really handy.
