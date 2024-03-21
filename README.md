# Roulette-on-Pi-Pico-with-LCD-Display
Project: Roulette simulation on an raspi pico with python

Status: finished
roulette.py contains just the roulette script which can be executed at any python 3 supporting device and outputs at the shell.
the Roulette-on-raspi-pico needs an rasberry pi pico with lcd display and i2c port with sda on pin 20 and scl on pin 21, a joystick on pin 26/27 and the joystick button on pin 14/an extra button on pin 14 
Finally random.choices may have to be random.choice depending on python versions. If random.choice is used, all resNumber[0] have to be replaced with resNumber.
