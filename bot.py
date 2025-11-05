import os
import asyncio
from datetime import datetime, timedelta
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from api_client import MedicalAPIClient
from keyboards import BotKeyboards

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Временное хранение токенов пользователей
user_tokens = {}

# FSM состояния для записи к врачу
class BookingState(StatesGroup):
    selecting_doctor = State()
    selecting_time = State()
    confirming_appointment = State()

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
        f"• 🔍 Поиск врачей\n\n"
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
async def main_menu_callback(callback: types.CallbackQuery, state: FSMContext):
    """Return to main menu"""
    await state.clear()  # Clear any active states
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
async def book_appointment_callback(callback: types.CallbackQuery, state: FSMContext):
    """Start appointment booking process"""

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
    
    # Получаем список врачей
    access_token = user_tokens[user_id]["token"]
    
    async with MedicalAPIClient() as api_client:
        doctors = await api_client.get_doctors_by_specialization(None, access_token)
        
        if not doctors:
            await callback.message.edit_text(
                "❌ **Врачи не найдены**\n\n"
                "В данный момент нет доступных врачей.",
                reply_markup=BotKeyboards.back_to_main(),
                parse_mode="Markdown"
            )
            await callback.answer()
            return
        
        await callback.message.edit_text(
            "👨⚕️ **Выберите врача для записи:**\n\n"
            "Доступные врачи:",
            reply_markup=BotKeyboards.doctors_for_booking(doctors),
            parse_mode="Markdown"
        )
        
        await state.set_state(BookingState.selecting_doctor)
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

# ==================== BOOKING PROCESS HANDLERS ====================

@dp.callback_query(F.data.startswith("select_doctor_"))
async def select_doctor_callback(callback: types.CallbackQuery, state: FSMContext):
    """Handle doctor selection"""
    doctor_id = callback.data.replace("select_doctor_", "")
    
    # Save doctor info to state
    await state.update_data(doctor_id=doctor_id)
    
    # Get doctor info for display
    user_id = callback.from_user.id
    access_token = user_tokens[user_id]["token"]
    
    try:
        async with MedicalAPIClient() as api_client:
            doctor_info = await api_client.get_doctor_info(doctor_id, access_token)
            
            if doctor_info:
                doctor_name = f"{doctor_info['name']} {doctor_info['surname']}"
                specialization = doctor_info['specialization']
                
                await state.update_data(
                    doctor_name=doctor_name,
                    specialization=specialization
                )
                
                await callback.message.edit_text(
                    f"👨⚕️ **Выбран врач: {doctor_name}**\n\n"
                    f"🏥 Специализация: {specialization}\n\n"
                    f"⏰ **Выберите удобное время:**",
                    reply_markup=BotKeyboards.booking_time_slots(),
                    parse_mode="Markdown"
                )
                
                await state.set_state(BookingState.selecting_time)
            else:
                await callback.message.edit_text(
                    "❌ **Ошибка получения данных врача**\n\n"
                    "Попробуйте выбрать другого врача.",
                    reply_markup=BotKeyboards.back_to_main(),
                    parse_mode="Markdown"
                )
    except Exception as e:
        await callback.message.edit_text(
            "❌ **Ошибка системы**\n\n"
            f"Ошибка: {str(e)}",
            reply_markup=BotKeyboards.back_to_main(),
            parse_mode="Markdown"
        )
    
    await callback.answer()

@dp.callback_query(F.data.startswith("select_time_"))
async def select_time_callback(callback: types.CallbackQuery, state: FSMContext):
    """Handle time selection"""
    selected_time = callback.data.replace("select_time_", "")
    
    # Get tomorrow's date as default
    tomorrow = datetime.now() + timedelta(days=1)
    appointment_date = tomorrow.strftime("%Y-%m-%d")
    
    # Save time and date to state
    await state.update_data(
        time=selected_time,
        date=appointment_date
    )
    
    # Get saved data for confirmation
    data = await state.get_data()
    
    doctor_name = data.get('doctor_name', 'Неизвестный врач')
    specialization = data.get('specialization', 'Не указано')
    
    await callback.message.edit_text(
        f"✅ **Подтвердите запись:**\n\n"
        f"👨⚕️ Врач: {doctor_name}\n"
        f"🏥 Специализация: {specialization}\n"
        f"📅 Дата: {tomorrow.strftime('%d.%m.%Y')}\n"
        f"⏰ Время: {selected_time}\n\n"
        f"Подтвердить запись?",
        reply_markup=BotKeyboards.booking_confirmation(
            doctor_name, specialization, appointment_date, selected_time
        ),
        parse_mode="Markdown"
    )
    
    await state.set_state(BookingState.confirming_appointment)
    await callback.answer()

@dp.callback_query(F.data == "confirm_booking")
async def confirm_booking_callback(callback: types.CallbackQuery, state: FSMContext):
    """Confirm and create appointment"""
    user_id = callback.from_user.id
    access_token = user_tokens[user_id]["token"]
    user_email = user_tokens[user_id]["email"]
    
    # Get booking data
    data = await state.get_data()
    doctor_id = data.get('doctor_id')
    date = data.get('date')
    time = data.get('time')
    doctor_name = data.get('doctor_name')
    
    async with MedicalAPIClient() as api_client:
        appointment = await api_client.create_appointment(
            doctor_id, date, time, user_email, access_token
        )
        
        if appointment:
            await callback.message.edit_text(
                f"🎉 **Запись успешно создана!**\n\n"
                f"📋 Номер записи: #{str(appointment.get('id', 'N/A'))[:8]}\n"
                f"👨⚕️ Врач: {doctor_name}\n"
                f"📅 Дата: {date}\n"
                f"⏰ Время: {time}\n\n"
                f"✅ Запись сохранена в системе!",
                reply_markup=BotKeyboards.back_to_main(),
                parse_mode="Markdown"
            )
        else:
            await callback.message.edit_text(
                "❌ **Ошибка создания записи**\n\n"
                "Проверьте:\n"
                "• Есть ли доступные кабинеты\n"
                "• Работает ли FastAPI сервер",
                reply_markup=BotKeyboards.back_to_main(),
                parse_mode="Markdown"
            )
    
    await state.clear()
    await callback.answer()

@dp.callback_query(F.data == "cancel_booking")
async def cancel_booking_callback(callback: types.CallbackQuery, state: FSMContext):
    """Cancel booking process"""
    await callback.message.edit_text(
        "❌ **Запись отменена**\n\n"
        "Вы можете начать новую запись в любое время.",
        reply_markup=BotKeyboards.back_to_main(),
        parse_mode="Markdown"
    )
    
    await state.clear()
    await callback.answer()

# ==================== OTHER HANDLERS ====================

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
        doctors_text = "👨⚕️ **Врачи"
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

@dp.callback_query(F.data == "view_appointments")
async def view_appointments_callback(callback: types.CallbackQuery):
    """Show user appointments"""
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
    
    access_token = user_tokens[user_id]["token"]
    user_email = user_tokens[user_id]["email"]
    
    async with MedicalAPIClient() as api_client:
        appointments = await api_client.get_user_appointments(user_email, access_token)
        
        if not appointments:
            await callback.message.edit_text(
                "📋 **Ваши записи**\n\n"
                "У вас пока нет записей к врачам.",
                reply_markup=BotKeyboards.back_to_main(),
                parse_mode="Markdown"
            )
            await callback.answer()
            return
        
        appointments_text = "📋 **Ваши записи:**\n\n"
        
        for i, appointment in enumerate(appointments[:5], 1):
            appointments_text += f"**{i}.** Запись #{appointment.get('id', 'N/A')}\n"
            appointments_text += f"📅 Дата: {appointment.get('date', 'Не указана')}\n\n"
        
        await callback.message.edit_text(
            appointments_text,
            reply_markup=BotKeyboards.back_to_main(),
            parse_mode="Markdown"
        )
    
    await callback.answer()

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

# ==================== CATCH-ALL HANDLERS (MUST BE LAST) ====================

@dp.callback_query()
async def unknown_callback_handler(callback: types.CallbackQuery):
    """Handle unknown callback queries"""
    await callback.answer("❓ Неизвестная команда")

@dp.message()
async def unknown_message_handler(message: types.Message):
    """Handle unknown messages"""
    await message.answer(
        "🤔 **Не понял ваше сообщение**\n\n"
        "Используйте кнопки меню для навигации.",
        reply_markup=BotKeyboards.main_menu(),
        parse_mode="Markdown"
    )

async def set_bot_commands():
    """Set bot commands for menu"""
    commands = [
        BotCommand(command="start", description="🏠 Главное меню"),
        BotCommand(command="menu", description="📋 Показать меню"),
    ]
    
    await bot.set_my_commands(commands)

async def main():
    if not BOT_TOKEN:
        print("BOT_TOKEN не найден в .env файле")
        return
    
    try:
        # Устанавливаем команды бота
        await set_bot_commands()
        
        # Запускаем polling
        await dp.start_polling(bot)
        
    except Exception as e:
        print(f"Error starting bot: {e}")
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())