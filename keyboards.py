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
            InlineKeyboardButton(text="📊 Моя статистика", callback_data="my_statistics")
        )
        
        # Fourth row
        keyboard.row(
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
            InlineKeyboardButton(text="📋 Все врачи", callback_data="view_all_doctors")
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
            InlineKeyboardButton(text="📅 Посмотреть записи", callback_data="view_appointments"),
            InlineKeyboardButton(text="❌ Отменить запись", callback_data="cancel_appointments")
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
            InlineKeyboardButton(text="🔙 Назад", callback_data="select_date"),
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
    
    @staticmethod
    def appointments_for_cancellation(appointments_list) -> InlineKeyboardMarkup:
        """Appointments list for cancellation"""
        keyboard = InlineKeyboardBuilder()
        
        for i, appointment in enumerate(appointments_list[:5], 1):  # Show max 5 appointments
            appointment_id = appointment.get('id', 'N/A')
            date = appointment.get('datetime', 'Не указана')[:10]  # Get date part
            time = appointment.get('datetime', 'Не указано')[11:16]  # Get time part
            
            button_text = f"❌ {i}. {date} в {time}"
            
            keyboard.row(
                InlineKeyboardButton(
                    text=button_text,
                    callback_data=f"cancel_appointment_{appointment_id}"
                )
            )
        
        keyboard.row(
            InlineKeyboardButton(text="🔙 Назад", callback_data="my_appointments"),
            InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")
        )
        
        return keyboard.as_markup()
    
    @staticmethod
    def calendar(year: int, month: int) -> InlineKeyboardMarkup:
        """Generate calendar for date selection"""
        import calendar
        from datetime import datetime, date
        
        keyboard = InlineKeyboardBuilder()
        
        # Month and year header
        month_names = [
            "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
            "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
        ]
        
        keyboard.row(
            InlineKeyboardButton(
                text=f"📅 {month_names[month-1]} {year}",
                callback_data="ignore"
            )
        )
        
        # Days of week header
        keyboard.row(
            InlineKeyboardButton(text="Пн", callback_data="ignore"),
            InlineKeyboardButton(text="Вт", callback_data="ignore"),
            InlineKeyboardButton(text="Ср", callback_data="ignore"),
            InlineKeyboardButton(text="Чт", callback_data="ignore"),
            InlineKeyboardButton(text="Пт", callback_data="ignore"),
            InlineKeyboardButton(text="Сб", callback_data="ignore"),
            InlineKeyboardButton(text="Вс", callback_data="ignore")
        )
        
        # Calendar days
        cal = calendar.monthcalendar(year, month)
        today = date.today()
        
        for week in cal:
            week_buttons = []
            for day in week:
                if day == 0:
                    week_buttons.append(
                        InlineKeyboardButton(text=" ", callback_data="ignore")
                    )
                else:
                    current_date = date(year, month, day)
                    if current_date < today:
                        # Past dates - disabled
                        week_buttons.append(
                            InlineKeyboardButton(text="❌", callback_data="ignore")
                        )
                    elif current_date.weekday() >= 5:  # Weekend
                        # Weekend - disabled
                        week_buttons.append(
                            InlineKeyboardButton(text="🔴", callback_data="ignore")
                        )
                    else:
                        # Available date
                        week_buttons.append(
                            InlineKeyboardButton(
                                text=str(day),
                                callback_data=f"date_{year}-{month:02d}-{day:02d}"
                            )
                        )
            keyboard.row(*week_buttons)
        
        # Navigation buttons
        keyboard.row(
            InlineKeyboardButton(text="◀️ Пред", callback_data=f"cal_prev_{year}_{month}"),
            InlineKeyboardButton(text="След ▶️", callback_data=f"cal_next_{year}_{month}")
        )
        
        keyboard.row(
            InlineKeyboardButton(text="🔙 Назад", callback_data="book_appointment"),
            InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")
        )
        
        return keyboard.as_markup()