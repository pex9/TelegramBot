from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters, ConversationHandler
from common import token_code
from Group import *
from utils import is_valid_link
# Define states for the conversation
SELECTING_CATEGORY, GETTING_GROUP_NAME, GETTING_GROUP_LINK = range(3)
# Define the command handler for the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Create the main menu keyboard based on the Category list
    keyboard = [[InlineKeyboardButton(group["name"], callback_data=group["value"])] for group in Category]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Welcome to the Pex Bot! Please choose an option:', reply_markup=reply_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Create the text to show commands
    commands_text = (
        "Here are the available commands:\n"
        "/start - Start the bot\n"
        "/help - See the list of commands\n"
        "/add - Add a group to a category\n"
        "/cancel - Cancel an operation\n"
    )
    
    await update.message.reply_text(commands_text)

async def return_to_main_menu(query):
    # Recreate the main menu using the Category list
    keyboard = [[InlineKeyboardButton(group["name"], callback_data=group["value"])] for group in Category]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text('Welcome to the Menu Bot! Please choose an option:', reply_markup=reply_markup)
# Define the start of the /add conversation
async def add_group(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [[InlineKeyboardButton(group["name"], callback_data=group["value"])] for group in Category]
    keyboard.append([InlineKeyboardButton("back", callback_data='start')])  # Cancel option
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Please select a category to add the group:', reply_markup=reply_markup)
    return SELECTING_CATEGORY
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
# Handle category selection
async def category_selected(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    selected_category = next((group for group in Category if group["value"] == query.data), None)
    
    if selected_category:
        context.user_data['selected_category'] = selected_category
        await query.edit_message_text(text=f"You selected: {selected_category['name']}. Now please send the group name.")
        return GETTING_GROUP_NAME

# Get the group name from the user
async def get_group_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    group_name = update.message.text
    context.user_data['group_name'] = group_name
    await update.message.reply_text(f'Group name "{group_name}" received. Now, please send the group link.')
    return GETTING_GROUP_LINK

# Get the group link from the user
async def get_group_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    group_link = update.message.text
    selected_category = context.user_data['selected_category']
    group_name = context.user_data['group_name']
    if await is_valid_link(group_link) is False:
        await update.message.reply_text('Invalid link. Please try again.')
        return GETTING_GROUP_LINK
    # Add the new group to the selected category
    selected_category['group'].append({"name": group_name, "url": group_link})
    
    await update.message.reply_text(f'Group "{group_name}" added successfully with link: {group_link}')
    
    return ConversationHandler.END
# Handle cancellation
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('Operation cancelled.')
    return ConversationHandler.END
def main():
    # Initialize the bot with the token from common.py
    application = ApplicationBuilder().token(token_code).build()

    # Register the /start command handler
    application.add_handler(CommandHandler('start', start))

    # Register the /help command handler
    application.add_handler(CommandHandler('help', help_command))

     # Set up a conversation handler for adding a group
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('add', add_group)],
        states={
            SELECTING_CATEGORY: [CallbackQueryHandler(category_selected, pattern='^(' + '|'.join([cat['value'] for cat in Category]) + ')$')],
            GETTING_GROUP_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_group_name)],
            GETTING_GROUP_LINK: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_group_link)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    application.add_handler(conv_handler)
    
    # Create a pattern that matches all 'value' fields in the Category list, plus 'back_to_main'
    category_values = [group['value'] for group in Category]
    pattern = f"^({'|'.join(category_values + ['back_to_main'])})$"
    
    # Register the callback query handler with the dynamic pattern
    application.add_handler(CallbackQueryHandler(show_groups, pattern=pattern))

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
