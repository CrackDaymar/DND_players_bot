from aiogram import Bot, Dispatcher, types, executor
import random
from loguru import logger
from setting import API_TOKEN
from func_random import find_count_dice, find_dice
from character import create_new_character, change_characters_current_hp, update_curr_hp, find_characters, take_curr_hp


bot = Bot(token = API_TOKEN)
dp = Dispatcher(bot)
logger.add('info.log', format="{time} {level} {message}",
           level='INFO', rotation="10KB", compression='zip')


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_message(message.chat.id, "Привіт, тут Ви можете кинути дайси для гри в днд, для цього Вам треба "
                                            "просто написали к чи d та число куба, наприклад к20 чи d6, також можна "
                                            "додати число кубів перед кидком, наприклад 5к6 чи 10d10")


@logger.catch(level="info")
@dp.message_handler(commands=["додати"])
async def new_characters(message: types.Message):
    data = message.text[8:]
    try:
        name, hp = data.split()
        create_new_character(name, hp, message.chat.id)
        await bot.send_message(message.chat.id, "персонаж створений")
    except:
        await bot.send_message(message.chat.id, "Не правильний формат запису, введіть формат у вигляді /новий персонаж "
                                                "'ім'я персонажу' 'кількість хп персонажа'")


@dp.message_handler(commands=["удалить"])
async def delete_characters(message: types.Message):
    pass


@dp.message_handler(commands=["удар"])
async def change_cur_hp(message: types.Message):
    data = message.text[6:]
    try:
        name, hp = data.split()
        curr_hp = change_characters_current_hp(name, hp)
        if curr_hp > 0:
            await bot.send_message(message.chat.id, f"Тепер у Вашого персонажа {curr_hp}")
        elif curr_hp == 0:
            await bot.send_message(message.chat.id, "Вас вибили до 0 хп")
        elif curr_hp < 0:
            await bot.send_message(message.chat.id, f"Вас вибили в мінуса, Ваш персонаж лежить та борется за життя")
    except:
        await bot.send_message(message.chat.id, "Не правильний формат запису, введіть формат у вигляді /новий персонаж "
                                                "'ім'я персонажу' 'кількість хп персонажа'")


@dp.message_handler(commands=["відпочинок"])
async def full_hp(message: types.Message):
    try:
        update_curr_hp()
        await bot.send_message(message.chat.id, "Ви відпочили, тепер у Вас фулл хп, але будьте обережні, у ворогів "
                                                "також відновилися хп")
    except:
        await bot.send_message(message.chat.id, "Не правильний формат запису, введіть формат у вигляді /новий персонаж "
                                                "'ім'я персонажу' 'кількість хп персонажа'")


@dp.message_handler(commands=["персонаж"])
async def find_char(message: types.Message):
    name = message.text[10:]
    try:
        data = find_characters(name)
        await bot.send_message(message.chat.id, f"Ваш персонаж: \n1. Ім'я - {data[0][0]}"
                                                f"\n2. Максимальне хп - {data[0][1]}"
                                                f"\n3. Залишилося хп - {data[0][3]}")
    except:
        await bot.send_message(message.chat.id, "Не знайдений персонаж")



@logger.catch(level="INFO")
@dp.message_handler(content_types=['text'])
async def all_mes(message: types.Message):
    try:
        dice, out_log, summ = find_dice(message.text), [], 0
        count = find_count_dice(message.text, dice)
        for c in range(0, count):
            out_log.append(random.randint(1, dice))
            summ += out_log[c]
        await bot.send_message(message.chat.id, f"Куби які накинулись = {out_log} \nі їх сумма = {summ}")
        logger.info(f"{message.chat.full_name} кинув {count}к{dice} і отримав = {summ}")
    except:
        pass


@logger.catch(level="info")
def main():
    logger.info('Start')
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    main()
