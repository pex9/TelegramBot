from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Define the command handler for the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Ciao Davide!')

def main():
    # Replace 'YOUR_TOKEN' with your actual bot token
    application = ApplicationBuilder().token("8192550968:AAG7OjregvS_WWTtDZUnX3PUCp5WatTBHvY").build()

    # Register the /start command handler
    application.add_handler(CommandHandler('start', start))

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
