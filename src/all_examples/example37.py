import aiohttp
import asyncio
from src.util import fetch_status
from src.util import async_timed


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        url = 'https://example.com'
        fetchers = [asyncio.create_task(fetch_status(session, url)),
                    asyncio.create_task(fetch_status(session, url)),
                    asyncio.create_task(fetch_status(session, url, delay=3))]

        done, pending = await asyncio.wait(fetchers, timeout=1)

        print(f'Число завершившихся задач: {len(done)}')
        print(f'Число ожидающих задач: {len(pending)}')

        for done_task in done:
            result = await done_task
            print(result)


asyncio.run(main())
