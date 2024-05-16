import os

import httpx
from dotenv import load_dotenv
from telegram import ForceReply, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

load_dotenv()
EDUHUB_URL = os.getenv("EDUHUB_URL")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """send a meassage whe the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"hi {user.mention_html()}!", reply_markup=ForceReply(selective=True)
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    user = update.effective_user

    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""

    await update.message.reply_text(update.message.text)


async def get_courses(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    courses_url = f"{ os.getenv('EDUHUB_URL') }courses/"
    client = httpx.AsyncClient()
    response = await client.get(courses_url)
    courses_data = response.json()
    await client.aclose()
    await update.message.reply_text(courses_data)


def main() -> None:
    """Start the bot."""

    # Create the Application and pass it your bot's token.

    application = Application.builder().token(os.getenv("EDUHUB_BOT_TOKEN")).build()

    # on different commands - answer in Telegram

    application.add_handler(CommandHandler("start", start))

    application.add_handler(CommandHandler("help", help_command))

    application.add_handler(CommandHandler("courses", get_courses))

    # on non command i.e message - echo the message on Telegram

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":

    main()
