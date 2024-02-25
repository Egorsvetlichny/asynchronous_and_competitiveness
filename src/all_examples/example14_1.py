import time
import asyncio


async def main():
    start = time.time()
    await asyncio.sleep(1)
    end = time.time()
    print(f'Сон занял {end - start} с')


asyncio.run(main())
