from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from common import token_code
from Group import school_groups, animes

# Define the command handler for the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("School", callback_data='school')],
        [InlineKeyboardButton("Anime", callback_data='anime')],
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Welcome to the Pex Bot! Please choose an option:', reply_markup=reply_markup)
async def return_to_main_menu(query):
    keyboard = [
        [InlineKeyboardButton("School", callback_data='school')],
        [InlineKeyboardButton("Anime", callback_data='anime')],
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text('Welcome to the Menu Bot! Please choose an option:', reply_markup=reply_markup)

# Show groups based on the selection
async def show_groups(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()  # Acknowledge the callback query

    if query.data == 'school':
        keyboard = []
        for group in school_groups:
            keyboard.append([InlineKeyboardButton(group['name'], url=group['url'])])
        keyboard.append([InlineKeyboardButton("Back", callback_data='back_to_main')])  # Back option

        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text='Select a school group:', reply_markup=reply_markup)

    elif query.data == 'anime':
        keyboard = []
        for group in animes:
            keyboard.append([InlineKeyboardButton(group['name'], url=group['url'])])
        keyboard.append([InlineKeyboardButton("Back", callback_data='back_to_main')])  # Back option

        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text='Select an anime group:', reply_markup=reply_markup)

    elif query.data == 'back_to_main':
        await return_to_main_menu(query)

def main():
    # Initialize the bot with the token from common.py
    application = ApplicationBuilder().token(token_code).build()

    # Register the /start command handler
    application.add_handler(CommandHandler('start', start))
    
    # Register the callback query handler for button presses
    application.add_handler(CallbackQueryHandler(show_groups, pattern='^(school|anime|back_to_main)$'))

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
