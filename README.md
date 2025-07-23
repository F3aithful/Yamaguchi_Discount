# Telegram Auto Responder Bot 🤖

## 📌 Описание

Это Telegram-бот, который автоматически отвечает на часто задаваемые вопросы с помощью кнопок. Также он уведомляет владельца (админа), кто и что спрашивал.

## ⚙️ Настройка

1. Склонируй репозиторий:
   ```
   git clone https://github.com/yourusername/telegram-autobot.git
   ```

2. Установи зависимости:
   ```
   pip install -r requirements.txt
   ```

3. Создай `.env` файл и добавь переменные:
   ```
   BOT_TOKEN=твой_токен_бота
   ADMIN_CHAT_ID=твой_телеграм_ID
   ```

4. Запусти бота:
   ```
   python Bot.py
   ```

## 🚀 Развёртывание на Render

1. Создай новый Web Service на [Render](https://render.com/)
2. Укажи Build Command:
   ```
   pip install -r requirements.txt
   ```
3. Укажи Start Command:
   ```
   python Bot.py
   ```
4. Добавь переменные среды:
   - `BOT_TOKEN`
   - `ADMIN_CHAT_ID`

Готово ✅
