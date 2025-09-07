import logging
import aiohttp
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import List, Tuple
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
import os

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
MODEL_API_PORT= int(os.getenv('MODEL_API_PORT'))
TELEGRAM_BOT_PORT= int(os.getenv('TELEGRAM_BOT_PORT'))
DOMAIN=os.getenv('DOMAIN')


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)



bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

QUESTIONS = {
    'age': ("Ваш возраст:", "numeric"),
    'height': ("Ваш рост в сантиметрах:", "numeric"),
    'weight': ("Ваш вес в килограммах:", "numeric"),
    'gender': ("Пол:", "options", [("Мужской", 1), ("Женский", 2)]),
    'angina': ("У вас была стенокардия или ишемическая болезнь сердца?", "options", [("Да", 1), ("Нет", 2)]),
    'stroke': ("У вас когда-нибудь был инсульт?", "options", [("Да", 1), ("Нет", 2)]),
    'health_status': ("Вы бы сказали, что ваше здороье:", "options", [
        ("Идеальное", 1), ("Отличное", 2), ("Хорошее", 3),
        ("Удовлетворительное", 4), ("Плохое", 5)
    ]),
    'cholesterol': ("Был ли у вас повышенный уровень холестерина?", "options", [("Да", 1), ("Нет", 2)]),
    'cigarettes': ("Вы выкурили 100+ сигарет за всю жизнь?", "options", [("Да", 1), ("Нет", 2)]),
    'marital_status': ("Ваше семейное положение:", "options", [
        ("Женат/Замужем", 1), ("Разведен(а)", 2),
        ("Вдова/Вдовец", 3), ("Живем раздельно", 4),
        ("Не в браке", 5), ("Есть пара", 6)
    ]),
    'employment': ("Ваш статус занятости:", "options", [
        ("Работаю по найму", 1), ("Самозанятый", 2),
        ("Без работы <1 года", 3), ("Без работы 1+ год", 4),
        ("Домохозяйка", 5), ("Студент", 6), ("Пенсионер", 7), ("Не могу работать", 8)
    ]),
    'copd': ("У вас был ХОБЛ, эмфизема или хронический бронхит?", "options", [("Да", 1), ("Нет", 2)]),
    'personal_doctor': ("У вас есть личный врач?", "options", [("Да", 1), ("Нет", 2)]),
    'depression': ("У вас когда-либо было депрессивное расстройство?", "options", [("Да", 1), ("Нет", 2)]),
    'walking_difficulty': ("Возникают ли у вас трудности при ходьбе или подъеме по лестнице?", "options", [("Да", 1), ("Нет", 2)]),
    'last_checkup': ("Когда у вас был последний осмотр у врача?", "options", [
        ("<1 года назад", 1), ("<2 лет назад", 2),
        ("<5 лет назад", 3), ("5+ лет назад", 4),
        ("Никогда", 5)
    ]),
    'hypertension': ("У вас есть постоянное повышенное давление?", "options", [
        ("Да", 1), ("Только при беременности", 2),
        ("Нет", 3), ("Есть предгипертензия", 4)
    ]),
    'diabetes': ("У вас есть диабет?", "options", [
        ("Да", 1), ("Был только при беременности", 2),
        ("Нет", 3), ("Преддиабет", 4)
    ])
}

class Form(StatesGroup):
    age = State()
    height = State()
    weight = State()
    gender = State()
    angina = State()
    stroke = State()
    health_status = State()
    cholesterol = State()
    cigarettes = State()
    marital_status = State()
    employment = State()
    copd = State()
    personal_doctor = State()
    depression = State()
    walking_difficulty = State()
    last_checkup = State()
    hypertension = State()
    diabetes = State()


async def create_keyboard(options: List[Tuple[str, int]]) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    for text, value in options:
        builder.add(types.InlineKeyboardButton(text=text, callback_data=str(value)))
    builder.adjust(2)
    return builder

async def ask_question(message: types.Message, state: FSMContext, question: str):
    question_data = QUESTIONS[question]
    question_text = question_data[0]
    question_type = question_data[1]
    
    await state.set_state(getattr(Form, question))
    
    if question_type == "numeric":
        await message.answer(question_text)
    else:
        options = question_data[2]
        builder = await create_keyboard(options)
        await message.answer(question_text, reply_markup=builder.as_markup())

@dp.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Привет! Я бот для оценки риска инфаркта.\n"
        "Для получения результата. Ответьте на несколько вопросов.\n"
        "Для начала опроса введите /survey\n"
        "Для отмены опроса введите /cancel\n"
    )

@dp.message(Command("survey"))
async def start_survey(message: types.Message, state: FSMContext):
    await state.clear()
    await ask_question(message, state, 'age')

@dp.message(Command("cancel"))
async def cancel_survey(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Опрос прерван. Для начала нового опроса введите /survey")

@dp.message(Form.age)
async def process_age(message: types.Message, state: FSMContext):
    try:
        value = int(message.text)
        if value < 1 or value > 120:
            await message.answer("Пожалуйста, введите корректный возраст (1-120)")
            return
            
        await state.update_data(age=value)
        await ask_question(message, state, 'height')
    except ValueError:
        await message.answer("Пожалуйста, введите целое число")

@dp.message(Form.height)
async def process_height(message: types.Message, state: FSMContext):
    try:
        value = int(message.text)
        if value < 50 or value > 250:
            await message.answer("Пожалуйста, введите корректный рост (50-250 см)")
            return
            
        await state.update_data(height=value)
        await ask_question(message, state, 'weight')
    except ValueError:
        await message.answer("Пожалуйста, введите целое число")

@dp.message(Form.weight)
async def process_weight(message: types.Message, state: FSMContext):
    try:
        value = int(message.text)
        if value < 20 or value > 300:
            await message.answer("Пожалуйста, введите корректный вес (20-300 кг)")
            return
            
        await state.update_data(weight=value * 100)
        await ask_question(message, state, 'gender')
    except ValueError:
        await message.answer("Пожалуйста, введите целое число")

@dp.callback_query(F.data)
async def handle_options(callback: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if not current_state:
        await callback.answer("Сессия устарела. Начните опрос заново /survey")
        return
    
    state_name = current_state.split(':')[1]
    question_data = QUESTIONS.get(state_name)
    
    if not question_data or question_data[1] != "options":
        await callback.answer("Неизвестный вопрос")
        return
    
    value = int(callback.data)
    options = question_data[2]
    chosen_text = next((text for text, val in options if val == value), "Неизвестный вариант")
    
    await state.update_data({state_name: value})
    await callback.message.edit_text(f"{question_data[0]}\nВы выбрали: {chosen_text}")
    await callback.answer()
    
    questions_order = list(QUESTIONS.keys())
    try:
        next_index = questions_order.index(state_name) + 1
        if next_index < len(questions_order):
            await ask_question(callback.message, state, questions_order[next_index])
        else:
            await show_results(callback.message, state)
    except ValueError:
        await callback.message.answer("Произошла ошибка. Пожалуйста, начните опрос заново с помощью /survey")

async def show_results(message: types.Message, state: FSMContext):
    data = await state.get_data()
    logger.info(f"Ответы пользователя: {data}")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"http://model-api:{MODEL_API_PORT}/predict",
                json=data,
                timeout=5.0
            ) as response:
                
                if response.status == 200:
                    result = await response.json()
                    prediction_result = result.get('prediction', 0)
                    
                    
                    
                    if prediction_result == 1:
                        await message.answer("⚠️ Есть риск инфаркта. Рекомендуем обратиться к врачу для полного обследования.")
                    else:
                        await message.answer("✅ Низкий риск инфаркта. Продолжайте вести здоровый образ жизни!")
                else:
                    error_text = await response.text()
                    logger.error(f"Ошибка API: {response.status} - {error_text}")
                    await message.answer("Произошла ошибка при расчете риска. Попробуйте позже.")
    except asyncio.TimeoutError:
        logger.error("Таймаут при запросе к API")
        await message.answer("Сервис временно недоступен. Попробуйте позже.")
    except Exception as e:
        logger.error(f"Ошибка API: {str(e)}")
        await message.answer("Сервис временно недоступен. Попробуйте позже.")



async def main():
    
    webhook_url = f"https://{DOMAIN}/webhook/{TELEGRAM_BOT_TOKEN}"
    
    app = web.Application()
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=f"/webhook/{TELEGRAM_BOT_TOKEN}")
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', TELEGRAM_BOT_PORT) 
    await site.start()
    
    logger.info(f"Сервер запущен на 0.0.0.0:{TELEGRAM_BOT_PORT}")
    
    await bot.set_webhook(webhook_url)
    logger.info(f"Webhook установлен: {webhook_url}")
    
    await asyncio.Event().wait()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
