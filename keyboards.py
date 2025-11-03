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
        

        keyboard.row(
            InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")
        )
        
        return keyboard.as_markup()
    
    @staticmethod
    def appointments_menu() -> InlineKeyboardMarkup:
        """Appointments menu keyboard"""
        keyboard = InlineKeyboardBuilder()
        
        keyboard.row(
            InlineKeyboardButton(text="📅 Посмотреть записи", callback_data="view_appointments")
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
    @staticmethod
    def doctors_for_booking(doctors_list) -> InlineKeyboardMarkup:
        """Doctors selection for booking"""
        keyboard = InlineKeyboardBuilder()
        
        for doctor in doctors_list[:8]:  # Show max 8 doctors
            name = f"{doctor.get('name', 'Неизвестно')} {doctor.get('surname', '')}"
            specialization = doctor.get('specialization', '')
            button_text = f"👨⚕️ {name} - {specialization}"
            
            keyboard.row(
                InlineKeyboardButton(
                    text=button_text[:64],  # Telegram button text limit
                    callback_data=f"select_doctor_{doctor['id']}"
                )
            )
        
        keyboard.row(
            InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")
        )
        
        return keyboard.as_markup()
    
    @staticmethod
    def booking_time_slots() -> InlineKeyboardMarkup:
        """Available time slots for booking"""
        keyboard = InlineKeyboardBuilder()
        
        # Available times
        times = ["09:00", "10:00", "11:00", "14:00", "15:00", "16:00", "17:00"]
        
        # Create rows of 3 buttons
        for i in range(0, len(times), 3):
            row_times = times[i:i+3]
            buttons = []
            for time in row_times:
                buttons.append(
                    InlineKeyboardButton(
                        text=f"⏰ {time}",
                        callback_data=f"select_time_{time}"
                    )
                )
            keyboard.row(*buttons)
        
        keyboard.row(
            InlineKeyboardButton(text="🔙 Назад", callback_data="book_appointment"),
            InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")
        )
        
        return keyboard.as_markup()
    
    @staticmethod
    def booking_confirmation(doctor_name, specialization, date, time) -> InlineKeyboardMarkup:
        """Booking confirmation keyboard"""
        keyboard = InlineKeyboardBuilder()
        
        keyboard.row(
            InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm_booking"),
            InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_booking")
        )
        keyboard.row(
            InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")
        )
        
        return keyboard.as_markup()