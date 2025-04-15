import multiprocessing
from app.settings import logger
import asyncio
import async_data_downloader


def start_downloading():
    try:
        process = multiprocessing.Process(target=run_async_data_downloader)
        process.start()
        logger.info("Data downloader started")
    except Exception as e:
        logger.error(f"Error starting data downloader: {e}")

def run_async_data_downloader():
    asyncio.run(async_data_downloader.main())

if __name__ == "__main__":
    start_downloading()