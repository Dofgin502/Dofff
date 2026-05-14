import os
import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

TOKEN = os.getenv("TOKEN")

# ===== КОМАНДЫ =====

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот работает ✅")

async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if update.message.reply_to_message:
            await update.message.reply_to_message.delete()

        await update.message.delete()

    except:
        pass

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("pong 🏓")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start - запуск\n"
        "/ping - проверка\n"
        "/delete - удалить сообщение ответом"
    )

# ===== ЗАПУСК =====

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("delete", delete))
    app.add_handler(CommandHandler("help", help_cmd))

    print("Бот запущен ✅")

    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
