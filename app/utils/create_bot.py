from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os

load_dotenv()
token = os.environ.get('TG_TOKEN')
bot = Bot(token="6896821960:AAGL9u82tRfoymIvTWvFbn18Uh1ndD4NalA", parse_mode="HTML")
dp = Dispatcher()

