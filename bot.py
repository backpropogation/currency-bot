import json
import logging
import os

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ParseMode
from aiogram.types.message import ContentType
from aiogram.utils.emoji import emojize
from aiogram.utils.executor import start_polling
from aiogram.utils.markdown import bold, italic, text, code
from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientConnectorError

API_TOKEN = os.environ.get('TOKEN')
RATES_URL = 'https://barakhtaev.engineer/api/rates/'
GRAPH_URL = 'https://barakhtaev.engineer/api/graphs/'
EXCHANGE_URL = 'https://barakhtaev.engineer/api/rates/exchange/'
WRONG_ARGS_ERROR = 'Wrong args, call /help for usage info'
API_ERROR = 'Something went wrong.'
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)

dp = Dispatcher(bot)


async def fetch(url, session):
    async with session.get(url) as response:
        return await response.text()


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    msg = text(
        bold('I can respond to the following commands:'),
        '/list', '/graph <currency>', '/exchange <currency> <amount> <currency>',
        sep='\n'
    )
    await message.reply(msg, parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(commands=['list'])
async def list_command(message: types.Message):
    await types.ChatActions.typing()

    content = await get_content()
    await message.reply(text(content, sep='\n'), parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(commands=['exchange'])
async def exchange_command(message: types.Message):
    await types.ChatActions.typing()
    args = message.get_args().split(' ')

    if len(args) == 3:
        rates = await get_exchange(*args)
        await message.reply(text(rates, sep='\n'), parse_mode=ParseMode.MARKDOWN)
    else:
        await message.reply(text(WRONG_ARGS_ERROR, sep='\n'), parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(commands=['graph'])
async def graph_command(message: types.Message):
    await types.ChatActions.typing()
    args = message.get_args().split(' ')
    if len(args) > 1:
        await bot.send_message(message.chat.id, text(WRONG_ARGS_ERROR),
                               parse_mode=ParseMode.MARKDOWN)
    else:
        async with ClientSession() as session:
            data = json.loads(await fetch(f'{GRAPH_URL}{args[0].upper()}/', session))
            photo = data.get('image', None)
            if photo:
                await bot.send_photo(message.from_user.id, photo=photo, caption='',
                                     reply_to_message_id=message.message_id)
            else:
                await message.reply(text(data.get('detail', API_ERROR), sep='\n'),
                                    parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(content_types=ContentType.ANY)
async def unknown_message(message: types.Message):
    msg = text(
        emojize('I dont know what to do with it:astonished:'),
        italic('I just remind you '), 'that there is', '/help', code('command'))
    await message.reply(msg, parse_mode=ParseMode.MARKDOWN)


async def get_exchange(*args):
    try:
        request_data = {
            'from_currency': args[0].upper(),
            'amount': args[1],
            'to_currency': args[2].upper(),
        }
        async with ClientSession() as session:
            async with session.post(EXCHANGE_URL, json=request_data) as response:
                if response.status != 200:
                    return json.loads(await response.text()).get('detail', API_ERROR)
                else:
                    response_data = json.loads(await response.text())
                    message = f'{response_data["amount"]} {response_data["from_currency"]} ' \
                              f'--> {response_data["result"]} {response_data["to_currency"]}\n' \
                              f'base currency = {response_data["base_currency"]}'
                    return message
    except ClientConnectorError:
        return API_ERROR


async def get_content():
    async with ClientSession() as session:
        data = json.loads(await fetch(RATES_URL, session))
    message = f"Rate parsed on {data['date']} with base currency {bold(data['base_currency'])}:\n"
    message += '\n'.join(
        [
            f"{bold(currency['name'])}: {italic(currency['rate_to_base_currency'])}"
            for currency in data['currencies']
        ]
    )
    return message


if __name__ == '__main__':
    start_polling(dp, skip_updates=True)
