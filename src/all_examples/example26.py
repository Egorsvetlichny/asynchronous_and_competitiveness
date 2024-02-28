import asyncio
import aiohttp
from src.util import async_timed
from src.util import fetch_status


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        url = 'https://www.example.com'
        status = await fetch_status(session, url)
        print(f'Состояние для {url} было равно {status}')


asyncio.run(main())
