import asyncio
import aiohttp
from src.util import fetch_status


async def main():
    async with aiohttp.ClientSession() as session:
        api_a = asyncio.create_task(fetch_status(session, 'https://www.example.com'))
        api_b = asyncio.create_task(fetch_status(session, 'https://www.example.com', delay=2))

        done, pending = await asyncio.wait([api_a, api_b], timeout=1)

        for task in pending:
            if task is api_b:
                print('API "B" слишком медленный, отмена')
                task.cancel()

        for task in done:
            result = await task
            print(result)


asyncio.run(main())
