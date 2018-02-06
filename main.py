from time import sleep
from hedgehog.client.sync_client import connect

import sys
from math import sin, pi

target = sys.argv[1] if len(sys.argv) > 1 else 'raspberrypi'
print("Hello {}".format(target))

with connect('tcp://{}.local:10789'.format(target), emergency=15) as hedgehog:
    def run():
        for i in range(16):
            hedgehog.set_input_state(i, True)

        def motors():
            while True:
                for i in range(20):
                    speed = int(1000 * sin(2 * pi * i / 20))
                    for port in range(4):
                        hedgehog.move(port, speed)
                    yield

        def servos():
            while True:
                for i in range(10):
                    pos = int(1024 + 900 * sin(2 * pi * i / 10))
                    for port in range(4):
                        hedgehog.set_servo(port, True, pos)
                    yield

        def sensors():
            while True:
                analogs = [hedgehog.get_analog(port) for port in range(8)]
                digitals = [hedgehog.get_digital(port) for port in range(8, 16)]

                print("".join('#=-.'[int(a / 1024)] for a in analogs) + " " +
                      "".join('.' if d else '#' for d in digitals))
                yield

        m = motors()
        s = servos()
        io = sensors()

        for i in range(20000):
            next(m)
            next(s)
            next(io)
            if i % 20 == 0:
                print()
            sleep(0.5)

    run()

    # Test running in a different thread than the one that connected
    # thread = hedgehog.spawn(run)
    # thread.join()
