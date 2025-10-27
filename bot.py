import os
import asyncio
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from api_client import MedicalAPIClient

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv('BOT_TOKEN')
API_BASE_URL = os.getenv('API_BASE_URL')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
api_client = MedicalAPIClient(API_BASE_URL)

class LoginState(StatesGroup):
    waiting_for_credentials = State()

@dp.message(CommandStart())
async def start_handler(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👨⚕️ Врачи", callback_data="doctors")],
        [InlineKeyboardButton(text="📅 Записи", callback_data="appointments")],
        [InlineKeyboardButton(text="🔐 Войти", callback_data="login")]
    ])
    
    await message.answer(
        "🏥 Добро пожаловать в медицинского бота!\n\n"
        "Выберите действие:",
        reply_markup=keyboard
    )

@dp.callback_query(F.data == "doctors")
async def doctors_handler(callback: types.CallbackQuery):
    if not api_client.token:
        await callback.message.edit_text("❌ Сначала войдите в систему, нажав кнопку 'Войти'")
        return
        
    doctors = await api_client.get_doctors()
    if doctors:
        text = "👨⚕️ Список врачей:\n\n"
        for doctor in doctors:
            text += f"• {doctor.get('name', 'Неизвестно')} - {doctor.get('specialization', 'Не указано')}\n"
    else:
        text = "❌ Не удалось получить список врачей. Проверьте авторизацию."
    
    await callback.message.edit_text(text)
    await callback.answer()

@dp.callback_query(F.data == "appointments")
async def appointments_handler(callback: types.CallbackQuery):
    if not api_client.token:
        await callback.message.edit_text("❌ Сначала войдите в систему, нажав кнопку 'Войти'")
        return
        
    appointments = await api_client.get_appointments()
    if appointments:
        text = "📅 Записи на прием:\n\n"
        for apt in appointments:
            text += f"• {apt.get('patient_name', 'Неизвестно')} - {apt.get('appointment_time', 'Не указано')}\n"
    else:
        text = "❌ Не удалось получить список записей. Проверьте авторизацию."
    
    await callback.message.edit_text(text)
    await callback.answer()

@dp.callback_query(F.data == "login")
async def login_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("🔐 Отправьте данные для входа в формате:\nemail password")
    await state.set_state(LoginState.waiting_for_credentials)
    await callback.answer()

@dp.message(LoginState.waiting_for_credentials)
async def process_login(message: types.Message, state: FSMContext):
    try:
        email, password = message.text.split(' ', 1)
        success = await api_client.login(email, password)
        if success:
            await message.answer("✅ Успешный вход в систему!")
        else:
            await message.answer("❌ Ошибка входа. Проверьте данные.")
    except ValueError:
        await message.answer("❌ Неверный формат. Используйте: email password")
    
    await state.clear()

async def main():
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN не найден в .env файле")
        return
    
    logger.info("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())