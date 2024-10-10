### WARNING
**Transmitting infrared remote control signals via an audio device may damage your hardware. You proceed at your own risk.**  
I am not an electrician, and I'm wary of the non-linear behaviors that can occur with LEDs under different conditions. Therefore, I cannot guarantee which hardware setups are safe to use.

Theoretically, common headphones have several Ohms of impedance, so using an LED with a 10 Ohm resistor might make sense. However, in my case, the currents were too small to activate the LED's transmission process, so I connected it directly to the headphone preamp. However, I surely can say that using line-level outputs is useless. On the other hand, the LED requires at least 50mA current, but the signals from the audio device are less than 1V with an impedance of over 100 Ohms, resulting in around 10mA of current, which is far too low. Use amplified outputs instead.

## What

This repository contains the code I use to control my lamps via the NEC protocol over infrared (IR) remote signals. My use cases include:
1. Turning on the lamp when I wake up, as I find it impossible to get out of bed without sunlight.
2. Turning the lamp on/off or adjusting its brightness when I am at my PC.

There are two infrared control methods:

### Infrared LED connected to a 3.5mm Jack, powered by the sound card
A standard infrared LED is soldered to a 3.5mm jack connector. IR control requires signals modulated at a 38 kHz carrier frequency. Some consumer devices may not transmit these signals, even if they claim to work at 44 kHz or higher. My Behringer UMC204HD does not have low-pass filters on its outputs, and I verified with an oscilloscope that it can generate "1010101010..." at 192 kHz. All the relevant code, including the NEC implementation, is in the `audio_ir` folder.

### Dummy Arduino device controlled via USB
This method is less convenient as it requires a dedicated USB port and power for the Arduino. However, it was useful during the debugging stage. The code for this is in the `arduino_ir` folder.
