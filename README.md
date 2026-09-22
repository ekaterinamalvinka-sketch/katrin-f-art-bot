# Katrin F Art Telegram Bot

Готовый каркас Telegram-бота для @KatrinF_Art_bot.

## Что уже работает
- /start — главное меню
- /gallery — раздел «Мои картины»
- /zodiac — 12 знаков зодиака
- /cosmos — космос и символы
- /about — обо мне
- /contact — связаться
- кнопка VK ведёт на https://vk.ru/club241340991
- Behance берётся из переменной BEHANCE_URL

## Важно
BOT_TOKEN — секрет. Не помещайте его в код, GitHub или чат. На Render добавьте его как Environment Variable.

## Развёртывание
1. Загрузите папку в GitHub.
2. На Render создайте Web Service из этого репозитория.
3. Build Command: pip install -r requirements.txt
4. Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
5. Добавьте:
   BOT_TOKEN = токен BotFather
   PUBLIC_URL = адрес сервиса Render, например https://katrin-f-art-bot.onrender.com
   BEHANCE_URL = ваша ссылка Behance
6. После запуска бот автоматически установит webhook.

Telegram Bot API использует HTTPS webhook для доставки обновлений на URL приложения.
