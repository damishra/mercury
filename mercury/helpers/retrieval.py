import aiocron
import asyncio
import aiohttp
import sys


@aiocron.crontab('*/30 * * * *')
async def run_auto_retrieval():
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://reddit.com/r/all.json') as response:
            data = await response.json()
            posts: list[dict] = data['data']['children']
            sub_counter: dict[str, int] = {}
            for post in posts:
                if post['data']['subreddit'] in sub_counter.keys():
                    sub_counter[post['data']['subreddit']
                                ] = sub_counter[post['data']['subreddit']] + 1
                else:
                    sub_counter[post['data']['subreddit']] = 1

            print(sub_counter)

try:
    asyncio.get_event_loop().run_forever()
except Exception:
    sys.exit(1)
