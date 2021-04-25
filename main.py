import asyncio
from timeit import default_timer
from aiohttp import ClientSession
import requests


async def fetch(url, session):
    fetch.start_time[url] = default_timer()
    async with session.get(url) as response:
        resp = await response.read()
        elapsed = default_timer() - fetch.start_time[url]
        print(f'{url:30} {elapsed:.2f} {asterisks(elapsed)}')
        return resp


async def fetch_all(urls):
    tasks = []
    fetch.start_time = dict()
    async with ClientSession() as session:
        for url in urls:
            task = asyncio.ensure_future(fetch(url, session))
            tasks.append(task)
        _ = await asyncio.gather(*tasks)


def demo_async(urls):
    start_time = default_timer()

    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(fetch_all(urls))
    loop.run_until_complete(future)

    total_elapsed = default_timer() - start_time
    print(f'WITH ASYNCIO: {total_elapsed:.2f} {asterisks(total_elapsed)}')


def demo_sequential(urls):
    start_time = default_timer()
    for url in urls:
        start_time_url = default_timer()
        _ = requests.get(url)
        elapsed = default_timer() - start_time_url
        print(f'{url:30} {elapsed:.2f}secs {asterisks(elapsed)}')
    total_elapsed = default_timer() - start_time
    print(f'TOTAL SECONDS: {total_elapsed:.2f} {asterisks(total_elapsed)}')


def asterisks(num):
    return int(num*10)*'*'


if __name__ == '__main__':
    URL_LIST = [
        'https://facebook.com',
        'https://github.com',
        'https://google.com',
        'https://microsoft.com',
        'https://yahoo.com',
    ]
    demo_sequential(URL_LIST)
    print('')
    demo_async(URL_LIST)
