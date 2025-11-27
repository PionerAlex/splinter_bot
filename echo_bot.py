

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
from pprint import pprint
# Вместо BOT TOKEN HERE нужно вставить токен вашего бота,
# полученный у @BotFather
BOT_TOKEN = TOKEN

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(Command(commands='start'))
async def process_start_command(message: Message):
    await message.answer('Напиши мне что-нибудь и в ответ '
        'я пришлю тебе твое сообщение')


@dp.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.reply('Привет!\nМеня зовут Эхо-бот!\nНапиши мне что-нибудь')

@dp.message()
async def send_echo(message: Message):
    print(message.model_dump_json(indent=4, exclude_none=True))
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(
            text='Данный тип апдейтов не поддерживается '
                 'методом send_copy'
        )


if __name__ == '__main__':
    dp.run_polling(bot)