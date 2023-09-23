from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from data import config

from middlewares.loggindmiddleware import LoggingMiddleware
from middlewares.lastactivitymiddleware import LastActivityMiddleware
from loguru import logger
from sys import stderr

# from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.schedulers.asyncio import AsyncIOScheduler

logger.remove()  # Удаляем все существующие обработчики
logger.add(stderr, format="<white>{time:HH:mm:ss}</white>"
                          " | <level>{level: <8}</level>"
                          " | <cyan>{line}</cyan>"
                          " - <magenta>{message}</magenta>")

# scheduler_bg = BackgroundScheduler()
# scheduler_io = AsyncIOScheduler()
bot = Bot(config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())
dp.middleware.setup(LastActivityMiddleware())