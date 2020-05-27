import asyncio

from ytarchiver.log import log
from ytarchiver.server import YtArchiver


async def main():
    archiver = YtArchiver()
    while True:
        try:
            archiver.run()
            await asyncio.sleep(15.0)
        except:
            log.exception("An unknown error occurred while processing downloads")
            await asyncio.sleep(60.0)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
