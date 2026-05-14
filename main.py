from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8853810921:AAEnf4XjVgZ62_HZQtg2RlpZ1t4sovnHVzc"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот работает ✅")


async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Команда delete работает ✅")


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("delete", delete))

    print("Bot started")

    app.run_polling()


if __name__ == "__main__":
    main()
