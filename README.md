# 🤖 Medical Telegram Bot

> Interactive Telegram bot for Medical Management System

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://python.org)
[![aiogram](https://img.shields.io/badge/aiogram-3.3.0-green.svg)](https://aiogram.dev)
[![FastAPI Integration](https://img.shields.io/badge/FastAPI-Integration-orange.svg)](https://github.com/aleks2008-dev/medical-app-fastapi)

## 🎯 Overview

Telegram bot interface for the Medical Management System, providing users with convenient access to medical services through Telegram messenger.

## 🚀 Features

- 👨⚕️ **Browse Doctors** - View available doctors and their specializations
- 📅 **Check Appointments** - View appointment schedules and availability
- 🔐 **Secure Authentication** - JWT-based login with medical app credentials
- 💬 **Interactive Interface** - User-friendly inline keyboards and FSM
- 🔄 **Real-time Integration** - Direct API communication with backend
- 🌐 **Multi-language Support** - Russian interface with emoji navigation

## 🛠️ Tech Stack

- **aiogram 3.3.0** - Modern async Telegram Bot framework
- **aiohttp** - Async HTTP client for API communication
- **python-dotenv** - Environment variables management
- **FSM (Finite State Machine)** - Advanced state management

## 📱 Bot Interface

### Main Menu
```
🏥 Добро пожаловать в медицинского бота!

Выберите действие:
[👨⚕️ Врачи] [📅 Записи] [🔐 Войти]
```

### Authentication Flow
```
User: /start
Bot: 🏥 Welcome message with menu
User: Clicks "🔐 Войти"
Bot: 🔐 Отправьте данные для входа в формате: email password
User: admin@example.com admin123
Bot: ✅ Успешный вход в систему!
```

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.12+
- Running Medical App backend
- Telegram Bot Token

### 1. Create Telegram Bot

1. Find [@BotFather](https://t.me/botfather) in Telegram
2. Send `/newbot` command
3. Choose bot name and username
4. Copy the provided bot token

### 2. Clone and Configure

```bash
git clone https://github.com/aleks2008-dev/medical-telegram-bot.git
cd medical-telegram-bot

# Create environment file
cp .env.example .env
```

Edit `.env` file:
```env
BOT_TOKEN=your_bot_token_from_botfather
API_BASE_URL=http://localhost:8000/api/v1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Bot

```bash
python bot.py
```

## 🏗️ Architecture

```
┌─────────────────┐    HTTP/JSON    ┌─────────────────┐
│  Telegram Bot   │ ←──────────────→ │   Medical API   │
│   (aiogram)     │                 │   (FastAPI)     │
└─────────────────┘                 └─────────────────┘
        ↑                                   ↑
   Telegram API                       PostgreSQL + Redis
```

### Components

- **bot.py** - Main bot application with handlers
- **api_client.py** - HTTP client for Medical API communication
- **FSM States** - User session and authentication state management

## 📁 Project Structure

```
medical-telegram-bot/
├── bot.py              # Main bot application
├── api_client.py       # Medical API client
├── requirements.txt    # Python dependencies
├── .env.example       # Environment template
├── .env              # Environment variables (create this)
├── Dockerfile        # Docker deployment
├── .gitignore        # Git ignore rules
└── README.md         # This documentation
```

## 🔐 Security Features

- **JWT Authentication** - Secure token-based auth
- **Session Management** - User state persistence
- **Input Validation** - Secure credential handling
- **Error Handling** - Graceful error responses
- **Token Storage** - Secure token management

## 🚀 Deployment

### Docker Deployment

```bash
# Build image
docker build -t medical-telegram-bot .

# Run container
docker run -d --name medical-bot \
  --env-file .env \
  medical-telegram-bot
```

### Docker Compose

```yaml
version: '3.8'
services:
  telegram-bot:
    build: .
    environment:
      - BOT_TOKEN=${BOT_TOKEN}
      - API_BASE_URL=${API_BASE_URL}
    restart: unless-stopped
```

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `BOT_TOKEN` | Telegram bot token from @BotFather | `123456:ABC-DEF...` |
| `API_BASE_URL` | Medical API base URL | `http://localhost:8000/api/v1` |

## 🔗 Integration

### Medical App Integration

This bot integrates with the [Medical FastAPI App](https://github.com/aleks2008-dev/medical-app-fastapi):

- **Authentication**: `POST /auth/login`
- **Doctors List**: `GET /doctors`
- **Appointments**: `GET /appointments`

### API Client Usage

```python
from api_client import MedicalAPIClient

client = MedicalAPIClient("http://localhost:8000/api/v1")

# Login
success = await client.login("user@example.com", "password")

# Get doctors
doctors = await client.get_doctors()

# Get appointments
appointments = await client.get_appointments()
```

## 🧪 Testing

```bash
# Run the bot in development mode
python bot.py

# Test commands in Telegram:
# /start - Initialize bot
# Click buttons to test functionality
```

## 📝 Usage Examples

### Basic User Flow

1. **Start Bot**: `/start`
2. **Login**: Click "🔐 Войти" → Send `email password`
3. **Browse Doctors**: Click "👨⚕️ Врачи"
4. **Check Appointments**: Click "📅 Записи"

### Admin Credentials (for testing)

```
Email: admin@example.com
Password: admin123
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Related Projects

- [Medical FastAPI Backend](https://github.com/aleks2008-dev/medical-app-fastapi) - Main backend application
- [aiogram Documentation](https://docs.aiogram.dev/) - Bot framework docs

## 👨‍💻 Author

**Aleks** - [GitHub Profile](https://github.com/aleks2008-dev)

---

⭐ **Star this repository if you found it helpful!**

## 📈 Features Highlights

- 🤖 **Modern Bot Framework** - aiogram 3.3.0 with async support
- 🔄 **FSM Integration** - Advanced state management
- 🔐 **Secure Authentication** - JWT token integration
- 💬 **Interactive UI** - Inline keyboards and user-friendly interface
- 🚀 **Production Ready** - Docker support and error handling
- 📱 **Mobile Optimized** - Perfect Telegram user experience