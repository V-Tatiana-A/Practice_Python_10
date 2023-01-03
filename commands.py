from bot_config import dp, bot
from aiogram import types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile
import keyboard as kb




class UserState(StatesGroup):
    temp = State()
    alc = State()
    age = State()
    results = State()
    exit = State()


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await bot.send_message(message.from_user.id, text="Привет! Я бот, который подскажет рецепт напитка на вечер.\n"
                                                      "Давай начнем!")
    await UserState.temp.set()
    await bot.send_message(message.from_user.id, text="Вы хотите горячий или холодный напиток?",
                           reply_markup=kb.buttons_2)


@dp.message_handler(commands=['help'])
async def process_start_command(message: types.Message):
    await bot.send_message(message.from_user.id, text="По заданным параметрам мы будем подбирать вам напиток "
                                                      "из небольшого списка. \n"
                                                      "Для корректной работы рекомендуем обращаться через появляющиеся кнопки.\n"
                                                      "Чтобы начать нажми /start . ")


@dp.message_handler(state=UserState.temp)
async def get_temp(message: types.Message, state: FSMContext):
    if message.text=='Горячий' or message.text=='Холодный':
        await state.update_data(temp=message.text)
        await UserState.next()
        await bot.send_message(message.from_user.id, text="Вы желаете алкогольный напиток?",
                               reply_markup=kb.buttons_1)
    else:
        await bot.send_message(message.from_user.id, text="Выберите пожалуйста из 2 вариантов на кнопках ниже.")


@dp.message_handler(state=UserState.alc)
async def get_alco(message: types.Message, state: FSMContext):
    if message.text == 'Да' or message.text == 'Нет':
        await state.update_data(alc=message.text)
        data = await state.get_data()
        if data["alc"] == "Да":
            await bot.send_message(message.from_user.id, text="А 18 лет вам есть?", reply_markup=kb.buttons_1)
            await UserState.age.set()
        else:
            await state.update_data(age="Нет")
            await get_cocktail(message, state)
    else:
        await bot.send_message(message.from_user.id, text="Выберите пожалуйста из 2 вариантов на кнопках ниже.")


@dp.message_handler(state=UserState.age)
async def get_age(message: types.Message, state: FSMContext):
    if message.text == 'Да' or message.text == 'Нет':
        await state.update_data(age=message.text)
        data = await state.get_data()
        if data["age"]=="Да":
            await UserState.next()
            await get_cocktail(message, state)
        else:
            await bot.send_message(message.from_user.id, text="Тогда ничего крепче кваса не предложу)\n"
                                                          "Покажу пожалуй список безалкогольных напитков")
            await UserState.next()
            await get_cocktail(message, state)
    else:
        await bot.send_message(message.from_user.id, text="Выберите пожалуйста из 2 вариантов на кнопках ниже.")


rec_book={}


async def get_cocktail(message: types.Message, state: FSMContext):
    data = await state.get_data()
    global rec_book
    if data["temp"] == 'Горячий':
        if data["age"] == 'Да':
            rec_book=kb.recipes("ГА.txt")
        else:
            rec_book=kb.recipes("ГБА.txt")
    else:
        if data["age"] == 'Да':
            rec_book=kb.recipes("ХА.txt")
        else:
            rec_book=kb.recipes("ХБА.txt")
    await UserState.results.set()
    await bot.send_message(message.from_user.id, 'Список:', reply_markup=kb.genmarkup(rec_book))



@dp.callback_query_handler(lambda call: True, state=UserState.results)
async def print_recipe(query: types.CallbackQuery):
    global rec_book
    photo = InputFile(f"photos/{query.data}.png")
    await bot.send_photo(query.from_user.id, photo=photo)
    await bot.send_message(query.from_user.id, f'{rec_book.get(query.data)}')
    await UserState.exit.set()
    await bot.send_message(query.from_user.id, text="Вы хотите посмотреть другой рецепт по тем же параметрам?",
                           reply_markup=kb.buttons_1)


@dp.message_handler(state=UserState.exit)
async def get_alco(message: types.Message, state: FSMContext):
    global rec_book
    if message.text=="Да":
        await get_cocktail(message, state)
    else:
        await bot.send_message(message.from_user.id, text="Спасибо, что зашли, буду ждать снова!")
        rec_book.clear()
        await state.finish()

@dp.message_handler()
async def unknown_request(message: types.Message):
    await bot.send_message(message.from_user.id, text="Я монозадачный бот и такие команды вне контекста не воспринимаю.\n"
                                                      "Попробуй обратиться через кнопки или начать заново через /start.")











