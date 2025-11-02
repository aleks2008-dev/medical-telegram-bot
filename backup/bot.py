import os
import asyncio
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from api_client import MedicalAPIClient
from keyboards import BotKeyboards
from datetime import datetime

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv('BOT_TOKEN')
API_BASE_URL = os.getenv('API_BASE_URL')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Временное хранение токенов пользователей
user_tokens = {}

class LoginState(StatesGroup):
    waiting_for_credentials = State()

class BookingState(StatesGroup):
    selecting_doctor = State()
    selecting_time = State()

@dp.message(CommandStart())
async def start_handler(message: types.Message):
    """Handle /start command with main menu"""
    user_name = message.from_user.first_name or "Пользователь"
    
    welcome_text = (
        f"🏥 **Добро пожаловать в медицинский центр!**\n\n"
        f"Привет, {user_name}! 👋\n\n"
        f"Я помогу вам:\n"
        f"• 📅 Записаться к врачу\n"
        f"• 📋 Управлять записями\n"
        f"• 👤 Управлять профилем\n\n"
        f"Выберите действие из меню ниже:"
    )
    
    await message.answer(
        welcome_text,
        reply_markup=BotKeyboards.main_menu(),
        parse_mode="Markdown"
    )

@dp.message(Command("menu"))
async def menu_handler(message: types.Message):
    """Show main menu"""
    await message.answer(
        "🏠 **Главное меню**\n\nВыберите нужное действие:",
        reply_markup=BotKeyboards.main_menu(),
        parse_mode="Markdown"
    )

# ==================== MAIN MENU HANDLERS ====================

@dp.callback_query(F.data == "main_menu")
async def main_menu_callback(callback: types.CallbackQuery):
    """Return to main menu"""
    await callback.message.edit_text(
        "🏠 **Главное меню**\n\nВыберите нужное действие:",
        reply_markup=BotKeyboards.main_menu(),
        parse_mode="Markdown"
    )
    await callback.answer()

@dp.callback_query(F.data == "doctors_list")
async def doctors_list_callback(callback: types.CallbackQuery):
    """Show doctors menu"""
    await callback.message.edit_text(
        "👨⚕️ **Наши врачи**\n\n"
        "Выберите специализацию или просмотрите всех врачей:",
        reply_markup=BotKeyboards.doctors_menu(),
        parse_mode="Markdown"
    )
    await callback.answer()

@dp.callback_query(F.data.startswith("spec_"))
async def specialization_callback(callback: types.CallbackQuery):
    """Handle specialization selection"""
    spec_map = {
        "spec_cardiology": "Кардиология ❤️",
        "spec_neurology": "Неврология 🧠",
        "spec_ophthalmology": "Офтальмология 👁️",
        "spec_dentistry": "Стоматология 🦷",
        "spec_therapy": "Терапия 🩺",
        "spec_surgery": "Хирургия 🔬"
    }
    
    specialization = spec_map.get(callback.data, "Неизвестная специализация")
    
    await callback.message.edit_text(
        f"👨⚕️ **{specialization}**\n\n"
        f"Загружаю список врачей...\n"
        f"(Здесь будет список врачей из API)\n\n"
        f"🔍 Для получения актуального списка врачей\n"
        f"необходимо авторизоваться в системе.",
        reply_markup=BotKeyboards.doctors_menu(),
        parse_mode="Markdown"
    )
    await callback.answer()

@dp.callback_query(F.data == "my_appointments")
async def my_appointments_callback(callback: types.CallbackQuery):
    """Show appointments menu"""
    user_id = callback.from_user.id
    
    if user_id not in user_tokens:
        await callback.message.edit_text(
            "❌ **Требуется авторизация**\n\n"
            "Для просмотра записей необходимо войти в систему.",
            reply_markup=BotKeyboards.back_to_main(),
            parse_mode="Markdown"
        )
        await callback.answer()
        return
    
    await callback.message.edit_text(
        "📋 **Мои записи**\n\n"
        "Управление вашими записями к врачам:",
        reply_markup=BotKeyboards.appointments_menu(),
        parse_mode="Markdown"
    )
    await callback.answer()

@dp.callback_query(F.data == "book_appointment")
async def book_appointment_callback(callback: types.CallbackQuery):
    """Handle appointment booking"""
    user_id = callback.from_user.id
    
    if user_id not in user_tokens:
        await callback.message.edit_text(
            "❌ **Требуется авторизация**\n\n"
            "Для записи к врачу необходимо войти в систему.",
            reply_markup=BotKeyboards.back_to_main(),
            parse_mode="Markdown"
        )
        await callback.answer()
        return
    
    await callback.message.edit_text(
        "📅 **Запись к врачу**\n\n"
        "Выберите удобное время для записи:",
        reply_markup=BotKeyboards.time_slots(),
        parse_mode="Markdown"
    )
    await callback.answer()

@dp.callback_query(F.data == "login")
async def login_callback(callback: types.CallbackQuery):
    """Handle login button"""
    await callback.message.edit_text(
        "🔐 **Вход в систему**\n\n"
        "Отправьте ваши данные в формате:\n"
        "`email:password`\n\n"
        "Например: `patient@example.com:password123`",
        reply_markup=BotKeyboards.back_to_main(),
        parse_mode="Markdown"
    )
    await callback.answer()

@dp.callback_query(F.data == "register")
async def register_callback(callback: types.CallbackQuery):
    """Handle register button"""
    await callback.message.edit_text(
        "📝 **Регистрация**\n\n"
        "Для регистрации обратитесь к администратору клиники\n"
        "или используйте веб-сайт: http://localhost:8000/docs\n\n"
        "📞 Телефон: +375 (29) 123-45-67\n"
        "📧 Email: admin@medical.com",
        reply_markup=BotKeyboards.back_to_main(),
        parse_mode="Markdown"
    )
    await callback.answer()





# ==================== TIME SLOTS HANDLERS ====================

@dp.callback_query(F.data.startswith("time_"))
async def time_slot_callback(callback: types.CallbackQuery):
    """Handle time slot selection"""
    time_slot = callback.data.replace("time_", "")
    
    await callback.message.edit_text(
        f"⏰ **Выбрано время: {time_slot}**\n\n"
        f"Теперь выберите врача для записи.\n"
        f"(Здесь будет список доступных врачей на это время)\n\n"
        f"🔍 Для завершения записи необходимо\n"
        f"выбрать врача и подтвердить запись.",
        reply_markup=BotKeyboards.back_to_main(),
        parse_mode="Markdown"
    )
    await callback.answer(f"✅ Время {time_slot} выбрано")

# ==================== LOGIN HANDLER ====================

@dp.message(F.text.contains(":"))
async def handle_login_credentials(message: types.Message):
    """Handle login credentials in format email:password"""
    try:
        email, password = message.text.split(":", 1)
        
        async with MedicalAPIClient() as api_client:
            token = await api_client.authenticate_user(email.strip(), password.strip())
            
            if token:
                user_tokens[message.from_user.id] = {
                    "token": token,
                    "email": email.strip()
                }
                
                await message.answer(
                    "✅ **Успешный вход в систему!**\n\n"
                    "Теперь вам доступны все функции бота.\n"
                    "Используйте меню для навигации:",
                    reply_markup=BotKeyboards.main_menu(),
                    parse_mode="Markdown"
                )
            else:
                await message.answer(
                    "❌ **Ошибка входа**\n\n"
                    "Неверный email или пароль.\n"
                    "Попробуйте еще раз:",
                    reply_markup=BotKeyboards.back_to_main(),
                    parse_mode="Markdown"
                )
    except ValueError:
        await message.answer(
            "❌ **Неверный формат данных**\n\n"
            "Используйте формат: `email:password`\n"
            "Например: `patient@example.com:password123`",
            reply_markup=BotKeyboards.back_to_main(),
            parse_mode="Markdown"
        )

async def set_bot_commands():
    """Set bot commands for menu"""
    commands = [
        BotCommand(command="start", description="🏠 Главное меню"),
        BotCommand(command="menu", description="📋 Показать меню"),
        BotCommand(command="help", description="❓ Помощь"),
    ]
    
    await bot.set_my_commands(commands)
    logger.info("Bot commands set successfully")

async def main():
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN не найден в .env файле")
        return
    
    try:
        # Устанавливаем команды бота
        await set_bot_commands()
        
        logger.info("🤖 Medical Bot started with navigation system!")
        logger.info("Available features:")
        logger.info("  📋 Inline keyboard navigation")
        logger.info("  🔐 User authentication")
        logger.info("  👨⚕️ Doctors management")
        logger.info("  📅 Appointments booking")
        logger.info("  📊 Visit history")
        logger.info("  👤 Profile management")
        logger.info("  ❓ Help and support")
        
        # Запускаем polling
        await dp.start_polling(bot)
        
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())
@dp.callback_query(F.data == "search_doctors")
async def search_doctors_callback(callback: types.CallbackQuery):
    """Show search doctors menu"""
    await callback.message.edit_text(
        "🔍 **Поиск врачей**\n\n"
        "Выберите специализацию для поиска врачей:",
        reply_markup=BotKeyboards.search_specializations(),
        parse_mode="Markdown"
    )
    await callback.answer()

@dp.callback_query(F.data.startswith("search_"))
async def search_specialization_callback(callback: types.CallbackQuery):
    """Handle specialization search"""
    specialization_map = {
        "search_cardiology": "Кардиология",
        "search_neurology": "Неврология", 
        "search_ophthalmology": "Офтальмология",
        "search_dentistry": "Стоматология",
        "search_therapy": "Терапия",
        "search_surgery": "Хирургия",
        "search_all_doctors": "all"
    }
    
    spec_key = callback.data
    if spec_key not in specialization_map:
        return
    
    specialization = specialization_map[spec_key]
    user_id = callback.from_user.id
    
    # Get access token if user is logged in
    access_token = None
    if user_id in user_tokens:
        access_token = user_tokens[user_id]["token"]
    
    async with MedicalAPIClient() as api_client:
        doctors = await api_client.get_doctors_by_specialization(
            specialization if specialization != "all" else None, 
            access_token
        )
        
        if not doctors:
            await callback.message.edit_text(
                f"❌ **Врачи не найдены**\n\n"
                f"По специализации '{specialization}' врачи не найдены.",
                reply_markup=BotKeyboards.search_specializations(),
                parse_mode="Markdown"
            )
            await callback.answer()
            return
        
        # Format doctors list
        doctors_text = f"👨‍⚕️ **Врачи"
        if specialization != "all":
            doctors_text += f" - {specialization}"
        doctors_text += ":**\n\n"
        
        for i, doctor in enumerate(doctors[:10], 1):  # Show max 10 doctors
            name = f"{doctor.get('name', 'Неизвестно')} {doctor.get('surname', '')}"
            spec = doctor.get('specialization', 'Не указано')
            experience = doctor.get('experience_years', 'Не указано')
            
            doctors_text += (
                f"**{i}. {name}**\n"
                f"🏥 Специализация: {spec}\n"
                f"📅 Опыт: {experience} лет\n\n"
            )
        
        if len(doctors) > 10:
            doctors_text += f"... и еще {len(doctors) - 10} врачей\n\n"
        
        doctors_text += "Для записи к врачу используйте главное меню."
        
        await callback.message.edit_text(
            doctors_text,
            reply_markup=BotKeyboards.search_specializations(),
            parse_mode="Markdown"
        )
    
    await callback.answer()