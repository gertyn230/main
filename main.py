from telegram import Update, ChatPermissions
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
import datetime

# Ваш токен бота
TOKEN = "7990211620:AAHN2ebAGkJHDq0gf2e9DS4B1SvO0AXZtsk"

# Получение ID бота для проверки
async def get_bot_id(context: ContextTypes.DEFAULT_TYPE) -> int:
    bot_info = await context.bot.get_me()
    return bot_info.id

# Функция для команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Привет! Я ваш Telegram-бот.")

# Функция для обработки сообщений с ответами
async def handle_reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.reply_to_message and update.message.text.lower() == "оу":
        replied_user = update.message.reply_to_message.from_user
        replied_username = (
            f"@{replied_user.username}" if replied_user.username else replied_user.full_name
        )
        await update.message.reply_text(f"{replied_username}, тёлочку на виренде Оу єс!")

# Проверка, что команда не применяется к самому боту
async def is_self(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int) -> bool:
    bot_id = await get_bot_id(context)
    return user_id == bot_id

# Команда /ban
async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.reply_to_message:
        user_to_ban = update.message.reply_to_message.from_user
        if await is_self(update, context, user_to_ban.id):
            await update.message.reply_text("Я не могу забанить самого себя!")
            return
        try:
            await context.bot.ban_chat_member(
                chat_id=update.effective_chat.id, user_id=user_to_ban.id
            )
            await update.message.reply_text(
                f"Пользователь {user_to_ban.full_name} был забанен 🚫"
            )
        except Exception as e:
            await update.message.reply_text(f"Ошибка: {e}")
    else:
        await update.message.reply_text("Эту команду нужно использовать как ответ на сообщение.")

# Команда /kick
async def kick(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.reply_to_message:
        user_to_kick = update.message.reply_to_message.from_user
        if await is_self(update, context, user_to_kick.id):
            await update.message.reply_text("Я не могу кикнуть самого себя!")
            return
        try:
            await context.bot.ban_chat_member(
                chat_id=update.effective_chat.id, user_id=user_to_kick.id
            )
            await context.bot.unban_chat_member(
                chat_id=update.effective_chat.id, user_id=user_to_kick.id
            )
            await update.message.reply_text(
                f"Пользователь {user_to_kick.full_name} был кикнут 🏃"
            )
        except Exception as e:
            await update.message.reply_text(f"Ошибка: {e}")
    else:
        await update.message.reply_text("Эту команду нужно использовать как ответ на сообщение.")

# Команда /mute
async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.reply_to_message:
        user_to_mute = update.message.reply_to_message.from_user
        if await is_self(update, context, user_to_mute.id):
            await update.message.reply_text("Я не могу замутить самого себя!")
            return
        try:
            duration_minutes = 10  # По умолчанию мут на 10 минут
            if context.args:  # Если указан аргумент времени
                try:
                    duration_minutes = int(context.args[0])
                except ValueError:
                    await update.message.reply_text("Пожалуйста, укажите корректное количество минут.")
                    return
            mute_time = datetime.timedelta(minutes=duration_minutes)
            until_date = datetime.datetime.utcnow() + mute_time  # Используем UTC вместо локального времени
            permissions = ChatPermissions(
                can_send_messages=False,
            )
            await context.bot.restrict_chat_member(
                chat_id=update.effective_chat.id,
                user_id=user_to_mute.id,
                permissions=permissions,
                until_date=until_date,
            )
            await update.message.reply_text(
                f"Пользователь {user_to_mute.full_name} был замучен на {duration_minutes} минут 🤐"
            )
        except Exception as e:
            await update.message.reply_text(f"Ошибка: {e}")
    else:
        await update.message.reply_text("Эту команду нужно использовать как ответ на сообщение.")

# Команда /unmute
async def unmute(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.reply_to_message:
        user_to_unmute = update.message.reply_to_message.from_user
        if await is_self(update, context, user_to_unmute.id):
            await update.message.reply_text("Я не могу размутить самого себя!")
            return
        try:
            permissions = ChatPermissions(
                can_send_messages=True,
            )
            await context.bot.restrict_chat_member(
                chat_id=update.effective_chat.id,
                user_id=user_to_unmute.id,
                permissions=permissions,
            )
            await update.message.reply_text(
                f"Пользователь {user_to_unmute.full_name} был размучен 🗣️"
            )
        except Exception as e:
            await update.message.reply_text(f"Ошибка: {e}")
    else:
        await update.message.reply_text("Эту команду нужно использовать как ответ на сообщение.")

# Основная функция, запускающая бота
def main():
    application = Application.builder().token(TOKEN).build()

    # Регистрируем обработчики команд и сообщений
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ban", ban))
    application.add_handler(CommandHandler("kick", kick))
    application.add_handler(CommandHandler("mute", mute))
    application.add_handler(CommandHandler("unmute", unmute))
    application.add_handler(MessageHandler(filters.REPLY, handle_reply))  # Обработка ответов

    application.run_polling()

# Запуск
if __name__ == "__main__":
    main()
