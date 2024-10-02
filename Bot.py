from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from common import token_code
from Group import *

# Define the command handler for the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Create the main menu keyboard based on the Category list
    keyboard = [[InlineKeyboardButton(group["name"], callback_data=group["value"])] for group in Category]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Welcome to the Pex Bot! Please choose an option:', reply_markup=reply_markup)

async def return_to_main_menu(query):
    # Recreate the main menu using the Category list
    keyboard = [[InlineKeyboardButton(group["name"], callback_data=group["value"])] for group in Category]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text('Welcome to the Menu Bot! Please choose an option:', reply_markup=reply_markup)

# Show groups based on the selection
async def show_groups(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()  # Acknowledge the callback query
    
    # Find the selected category using a single loop
    selected_category = next((group for group in Category if group["value"] == query.data), None)

    # If a matching category is found
    if selected_category:
        groups = selected_category["group"]  # Get the list of groups associated with this category

        # Create a keyboard for the group selection
        keyboard = [[InlineKeyboardButton(group['name'], url=group['url'])] for group in groups]
        keyboard.append([InlineKeyboardButton("Back", callback_data='back_to_main')])  # Add the Back button
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=f'Select a group from {selected_category["name"]}:', reply_markup=reply_markup)

    elif query.data == 'back_to_main':
        await return_to_main_menu(query)

def main():
    # Initialize the bot with the token from common.py
    application = ApplicationBuilder().token(token_code).build()

    # Register the /start command handler
    application.add_handler(CommandHandler('start', start))
    
    # Create a pattern that matches all 'value' fields in the Category list, plus 'back_to_main'
    category_values = [group['value'] for group in Category]
    pattern = f"^({'|'.join(category_values + ['back_to_main'])})$"
    
    # Register the callback query handler with the dynamic pattern
    application.add_handler(CallbackQueryHandler(show_groups, pattern=pattern))

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
