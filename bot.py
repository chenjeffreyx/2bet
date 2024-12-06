import os
import asyncio
import telegram

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
STAGING_AREA_TELEGRAM_CHAT_ID = os.getenv('STAGING_AREA_TELEGRAM_CHAT_ID')
TESTING_AREA_TELEGRAM_CHAT_ID = os.getenv('TESTING_AREA_TELEGRAM_CHAT_ID')

def create_message_from_bet_data(bet_data):
    r = ''
    for key, value in bet_data.items():
        r += f'{key}: {value}\n'
    return r

async def send_bet_to_staging_area(bet):
    bot = telegram.Bot(TELEGRAM_BOT_TOKEN)
    async with bot:
        message = create_message_from_bet_data(bet)
        await bot.send_message(text=message, chat_id=STAGING_AREA_TELEGRAM_CHAT_ID)

async def send_bet_to_testing_area(bet):
    bot = telegram.Bot(TELEGRAM_BOT_TOKEN)
    async with bot:
        message = create_message_from_bet_data(bet)
        await bot.send_message(text=message, chat_id=TESTING_AREA_TELEGRAM_CHAT_ID)
