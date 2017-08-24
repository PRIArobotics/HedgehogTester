Hedgehog Tester
===============

This project contains a small hardware test program for the Hedgehog controller.
The program continuously moves servos and motors, and shows sensor values on the console.

Usage
-----

Start the program and connect actuators to see that they are moving back and forth,
and connect sensors to check their output values.

To test properly, make sure to observe motors moving in both directions,
as an improperly soldered H-bridge may only affect one direction of movement.

The sensor output consists of 16 dots that change into other ASCII characters depending on sensor values::

    ......=. ........
    ......=. ........
    -.....=. ........

    -.....-. ......#.
    =....... ......#.
    #....... ........
    #....... ........

The above sample output shows analog sensors on ports 0 and 6 being adjusted,
and a push button on port 14 being pressed shortly.
Button 15 is configured as emergency stop, so make that port the last when testing.
Observing the empty line scrolling by helps confirming that the tester program is running properly,
even when there are no changes in sensor values and the console output therefore doesn't change.
