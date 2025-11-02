from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

class BotKeyboards:
    """Class for creating inline keyboards for the medical bot"""
    
    @staticmethod
    def main_menu() -> InlineKeyboardMarkup:
        """Main menu keyboard"""
        keyboard = InlineKeyboardBuilder()
        
        # First row
        keyboard.row(
            InlineKeyboardButton(text="🔐 Войти", callback_data="login"),
            InlineKeyboardButton(text="👨⚕️ Список врачей", callback_data="doctors_list")
        )
        
        # Second row
        keyboard.row(
            InlineKeyboardButton(text="📅 Записаться к врачу", callback_data="book_appointment"),
            InlineKeyboardButton(text="📋 Мои записи", callback_data="my_appointments")
        )
        
        # Third row
        keyboard.row(
            InlineKeyboardButton(text="🔍 Поиск врачей", callback_data="search_doctors"),
            InlineKeyboardButton(text="📝 Регистрация", callback_data="register")
        )
        
        return keyboard.as_markup()
    
    @staticmethod
    def doctors_menu() -> InlineKeyboardMarkup:
        """Doctors menu keyboard"""
        keyboard = InlineKeyboardBuilder()
        
        # Specializations
        keyboard.row(
            InlineKeyboardButton(text="❤️ Кардиолог", callback_data="spec_cardiology"),
            InlineKeyboardButton(text="🧠 Невролог", callback_data="spec_neurology")
        )
        keyboard.row(
            InlineKeyboardButton(text="👁️ Офтальмолог", callback_data="spec_ophthalmology"),
            InlineKeyboardButton(text="🦷 Стоматолог", callback_data="spec_dentistry")
        )
        keyboard.row(
            InlineKeyboardButton(text="🩺 Терапевт", callback_data="spec_therapy"),
            InlineKeyboardButton(text="🔬 Хирург", callback_data="spec_surgery")
        )
        
        # Navigation
        keyboard.row(
            InlineKeyboardButton(text="📋 Все врачи", callback_data="all_doctors"),
            InlineKeyboardButton(text="🔍 Поиск", callback_data="search_doctor")
        )
        keyboard.row(
            InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")
        )
        
        return keyboard.as_markup()
    
    @staticmethod
    def appointments_menu() -> InlineKeyboardMarkup:
        """Appointments menu keyboard"""
        keyboard = InlineKeyboardBuilder()
        
        keyboard.row(
            InlineKeyboardButton(text="📅 Активные записи", callback_data="active_appointments"),
            InlineKeyboardButton(text="📋 Все записи", callback_data="all_appointments")
        )
        keyboard.row(
            InlineKeyboardButton(text="📊 История посещений", callback_data="visit_history"),
            InlineKeyboardButton(text="📈 Статистика", callback_data="appointment_stats")
        )
        keyboard.row(
            InlineKeyboardButton(text="❌ Отменить запись", callback_data="cancel_appointment"),
            InlineKeyboardButton(text="🔄 Перенести запись", callback_data="reschedule_appointment")
        )
        keyboard.row(
            InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")
        )
        
        return keyboard.as_markup()
    
    @staticmethod
    def back_to_main() -> InlineKeyboardMarkup:
        """Simple back to main menu button"""
        keyboard = InlineKeyboardBuilder()
        keyboard.row(
            InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")
        )
        return keyboard.as_markup()
    
    @staticmethod
    def time_slots() -> InlineKeyboardMarkup:
        """Time slots for appointment booking"""
        keyboard = InlineKeyboardBuilder()
        
        # Morning slots
        keyboard.row(
            InlineKeyboardButton(text="🌅 09:00", callback_data="time_09:00"),
            InlineKeyboardButton(text="🌅 10:00", callback_data="time_10:00"),
            InlineKeyboardButton(text="🌅 11:00", callback_data="time_11:00")
        )
        
        # Afternoon slots
        keyboard.row(
            InlineKeyboardButton(text="☀️ 12:00", callback_data="time_12:00"),
            InlineKeyboardButton(text="☀️ 13:00", callback_data="time_13:00"),
            InlineKeyboardButton(text="☀️ 14:00", callback_data="time_14:00")
        )
        
        # Evening slots
        keyboard.row(
            InlineKeyboardButton(text="🌆 15:00", callback_data="time_15:00"),
            InlineKeyboardButton(text="🌆 16:00", callback_data="time_16:00"),
            InlineKeyboardButton(text="🌆 17:00", callback_data="time_17:00")
        )
        
        keyboard.row(
            InlineKeyboardButton(text="🔙 Назад", callback_data="book_appointment"),
            InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")
        )
        
        return keyboard.as_markup()
    @staticmethod
    def search_specializations() -> InlineKeyboardMarkup:
        """Search by specialization keyboard"""
        keyboard = InlineKeyboardBuilder()
        
        # Specializations
        keyboard.row(
            InlineKeyboardButton(text="❤️ Кардиология", callback_data="search_cardiology"),
            InlineKeyboardButton(text="🧠 Неврология", callback_data="search_neurology")
        )
        keyboard.row(
            InlineKeyboardButton(text="👁️ Офтальмология", callback_data="search_ophthalmology"),
            InlineKeyboardButton(text="🦷 Стоматология", callback_data="search_dentistry")
        )
        keyboard.row(
            InlineKeyboardButton(text="🩺 Терапия", callback_data="search_therapy"),
            InlineKeyboardButton(text="🔬 Хирургия", callback_data="search_surgery")
        )
        keyboard.row(
            InlineKeyboardButton(text="📋 Все врачи", callback_data="search_all_doctors")
        )
        keyboard.row(
            InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")
        )
        
        return keyboard.as_markup()