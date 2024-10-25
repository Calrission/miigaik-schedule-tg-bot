from os import getenv
from aiogram import Dispatcher
from dotenv import load_dotenv

from data.repositories.remote_data import RemoteData
from data.repositories.remote_data_abc import RemoteDataABC
from data.storage.database import Database
import locale
import sys

from data.storage.storage_abc import StorageABC

if sys.platform == 'win32':
    locale.setlocale(locale.LC_ALL, 'rus_rus')
else:
    locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

load_dotenv()
TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()
db: StorageABC = Database("db")
api: RemoteDataABC = RemoteData()
