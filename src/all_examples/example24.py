# Данный код будет работать только в Unix-системах

import asyncio
from asyncio import AbstractEventLoop
import socket
import logging
import signal
from typing import List


# Считать данные, и если пользователь отправил 'boom', возбудить ошибку, иначе отправить данные пользователю
async def echo(connection: socket, loop: AbstractEventLoop) -> None:
    try:
        while data := await loop.sock_recv(connection, 1024):
            print('got data!')
            if data == b'boom\r\n':
                raise Exception("Неожиданная ошибка сети")
            await loop.sock_sendall(connection, data)
    except Exception as ex:
        logging.exception(ex)
    finally:
        connection.close()


echo_tasks = []


# Принять подключение от пользователя, создать задачу echo-функцию и добавить задачу в список задач
async def connection_listener(server_socket, loop):
    while True:
        connection, address = await loop.sock_accept(server_socket)
        connection.setblocking(False)
        print(f"Получено сообщение от {address}")
        echo_task = asyncio.create_task(echo(connection, loop))
        echo_tasks.append(echo_task)


class GracefulExit(SystemExit):
    pass


def shutdown():
    raise GracefulExit()


# Получаем список задач, ожидаем по 2с их выполнения, либо снятие задач по истечении таймаута
async def close_echo_tasks(echo_tasks: List[asyncio.Task]):
    waiters = [asyncio.wait_for(task, 2) for task in echo_tasks]
    for task in waiters:
        try:
            await task
        except asyncio.exceptions.TimeoutError:
            # Здесь мы ожидаем истечения тайм-аута
            pass


# Инициализируем сокет, добавляем обработчики сигналов 'SIGINT' и 'SIGTERM', ожидаем подключение пользователя
async def main():
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = ('127.0.0.1', 8000)
    server_socket.setblocking(False)
    server_socket.bind(server_address)
    server_socket.listen()

    for signame in {'SIGINT', 'SIGTERM'}:
        loop.add_signal_handler(getattr(signal, signame), shutdown)
    await connection_listener(server_socket, loop)


loop = asyncio.new_event_loop()

# Выполняем программу до завершения main, либо до прерывания сигналами, пытаясь выполнить активные задачи
# В конце закрываем наш созданный цикл событий
try:
    loop.run_until_complete(main())
except GracefulExit:
    loop.run_until_complete(close_echo_tasks(echo_tasks))
finally:
    loop.close()
