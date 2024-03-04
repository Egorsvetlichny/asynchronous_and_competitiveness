# Асинхронный генератор отличается от обычного тем, что отдает не объекты Python,
# а генерирует сопрограммы, которые могут ждать получения результата с помощью
# await. Поэтому обычные циклы for и функция next с такими генераторами работать не будут.
# А вместо них предложена специальная синтаксическая конструкция async for.

import asyncio
from src.util import delay, async_timed


async def positive_integers_async(until: int):
    for integer in range(1, until):
        await delay(integer)
        yield integer


@async_timed()
async def main():
    async_generator = positive_integers_async(3)
    print(type(async_generator))

    async for number in async_generator:
        print(f'Получено число {number}')


asyncio.run(main())
