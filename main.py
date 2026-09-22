import os
import secrets
from fastapi import FastAPI, Request, HTTPException
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.environ["BOT_TOKEN"]
PUBLIC_URL = os.environ["PUBLIC_URL"].rstrip("/")
WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", secrets.token_urlsafe(24))

VK_URL = "https://vk.ru/club241340991"
BEHANCE_URL = os.environ.get("BEHANCE_URL", "")

app = FastAPI()
bot_app = Application.builder().token(BOT_TOKEN).build()

def main_keyboard():
    rows = [
        [InlineKeyboardButton("🎨 Мои картины", callback_data="gallery")],
        [InlineKeyboardButton("♈ 12 знаков зодиака", callback_data="zodiac")],
        [InlineKeyboardButton("🌌 Космос и символы", callback_data="cosmos")],
        [InlineKeyboardButton("👩‍🎨 Обо мне", callback_data="about")],
        [InlineKeyboardButton("💚 VK", url=VK_URL)],
    ]
    if BEHANCE_URL:
        rows.append([InlineKeyboardButton("🎨 Behance", url=BEHANCE_URL)])
    rows.append([InlineKeyboardButton("💬 Связаться со мной", callback_data="contact")])
    return InlineKeyboardMarkup(rows)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "✨ Добро пожаловать в Katrin F Art!\n\n"
        "Здесь я собираю авторские иллюстрации о космосе, "
        "астрологии, символах и трансформации.\n\n"
        "Выберите раздел:"
    )
    await update.effective_message.reply_text(text, reply_markup=main_keyboard())

async def gallery(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        "🎨 Здесь будет моя галерея картин.\n\n"
        "Следующим этапом мы добавим сюда твои работы и описания.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("💚 Смотреть VK", url=VK_URL)],
            *([[InlineKeyboardButton("🎨 Смотреть Behance", url=BEHANCE_URL)]] if BEHANCE_URL else [])
        ])
    )

async def zodiac(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        "♈ 12 знаков зодиака\n\n"
        "Авторская серия Katrin F: славянская эстетика, "
        "космос, сакральная геометрия и эзотерические символы."
    )

async def cosmos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        "🌌 Космос и символы\n\n"
        "Иллюстрации о Вселенной, символах, архетипах и внутренней трансформации."
    )

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        "👩‍🎨 Katrin F\n\n"
        "Авторские иллюстрации и визуальные истории.\n"
        "Космос • астрология • символы • магия"
    )

async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        "💬 По вопросам сотрудничества и заказа иллюстраций "
        "напишите мне в личные сообщения Telegram."
    )

bot_app.add_handler(CommandHandler("start", start))
bot_app.add_handler(CommandHandler("gallery", gallery))
bot_app.add_handler(CommandHandler("zodiac", zodiac))
bot_app.add_handler(CommandHandler("cosmos", cosmos))
bot_app.add_handler(CommandHandler("about", about))
bot_app.add_handler(CommandHandler("contact", contact))

@app.on_event("startup")
async def startup():
    await bot_app.initialize()
    await bot_app.start()
    await bot_app.bot.set_webhook(
        url=f"{PUBLIC_URL}/telegram/{WEBHOOK_SECRET}",
        allowed_updates=Update.ALL_TYPES,
    )

@app.on_event("shutdown")
async def shutdown():
    await bot_app.stop()
    await bot_app.shutdown()

@app.get("/")
async def health():
    return {"ok": True, "bot": "Katrin F Art"}

@app.post("/telegram/{secret}")
async def telegram_webhook(secret: str, request: Request):
    if not secrets.compare_digest(secret, WEBHOOK_SECRET):
        raise HTTPException(status_code=403, detail="Forbidden")
    data = await request.json()
    update = Update.de_json(data, bot_app.bot)
    await bot_app.process_update(update)
    return {"ok": True}
