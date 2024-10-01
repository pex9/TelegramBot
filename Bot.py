from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from common import token_code
from Group import groups
# Define the command handler for the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard=[]
    for group in groups:
        keyboard.append([InlineKeyboardButton(group['name'], url=group['url'])])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Welcome to the Menu Bot! Please choose an group to see:', reply_markup=reply_markup)


def main():
    # Replace 'YOUR_TOKEN' with your actual bot token
    application = ApplicationBuilder().token(token_code).build()

    # Register the /start command handler
    application.add_handler(CommandHandler('start', start))
    

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
