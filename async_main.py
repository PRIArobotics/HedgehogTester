from hedgehog.client.async_client import connect

import asyncio
import sys
from math import sin, pi
from aiostream.aiter_utils import anext

target = sys.argv[1] if len(sys.argv) > 1 else 'raspberrypi'
print("Hello {}".format(target))


async def main():
    async with connect('tcp://localhost:10789'.format(target)) as hedgehog:
        async def run():
            for i in range(16):
                await hedgehog.set_input_state(i, True)

            async def motors():
                while True:
                    for i in range(20):
                        speed = int(1000 * sin(2 * pi * i / 20))
                        for port in range(4):
                            await hedgehog.move(port, speed)
                        yield

            async def servos():
                while True:
                    for i in range(10):
                        pos = int(1024 + 900 * sin(2 * pi * i / 10))
                        for port in range(4):
                            await hedgehog.set_servo(port, True, pos)
                        yield

            async def sensors():
                while True:
                    analogs = [await hedgehog.get_analog(port) for port in range(8)]
                    digitals = [await hedgehog.get_digital(port) for port in range(8, 16)]

                    print("".join('#=-.'[int(a / 1024)] for a in analogs) + " " +
                          "".join('.' if d else '#' for d in digitals))
                    yield

            m = motors()
            s = servos()
            io = sensors()

            for i in range(20000):
                await anext(m)
                await anext(s)
                await anext(io)
                if i % 20 == 0:
                    print()
                await asyncio.sleep(0.5)

        await run()

        # Test running in a separate task from the one that connected
        # task = await hedgehog.spawn(run())
        # await task

asyncio.get_event_loop().run_until_complete(main())
