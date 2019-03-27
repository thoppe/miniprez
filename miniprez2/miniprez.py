import asyncio
import os

#_current_dir = os.path.join(os.getcwd(), '*.txt')
#target_file = os.path.abspath(__file__)

target_file = __file__

async def file_watcher(target_file, sleep_time=0.5):
    
    latest_modification_time = os.path.getmtime(target_file)
    
    while True:
        current_time = os.path.getmtime(target_file)
        if current_time > latest_modification_time:
            latest_modification_time = current_time
            yield current_time
        await asyncio.sleep(sleep_time)


async def main():
    async for changes in file_watcher(target_file):
        print(changes)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
