![Bot in Telegram](bot.png) 

# Telegram Bot Setup Guide

This guide will help you create your own Telegram bot using the BotFather, obtain the token, and set up your bot using the provided code.

## Step 1: Create Your Bot with BotFather

1. **Open Telegram**: Launch the Telegram app on your device or use the web version.

2. **Find BotFather**: In the search bar, type `@BotFather` and select the official BotFather bot.

3. **Start a Chat**: Click on the "Start" button or send `/start` to begin interacting with BotFather.

4. **Create a New Bot**:
   - Type `/newbot` and press Enter.
   - Follow the prompts to choose a name and a username for your bot.
   - The username must end with "bot" (e.g., `MySampleBot`).
   - You can also change the image using a specific /Edit bot pic

5. **Get Your Token**: After successfully creating your bot, BotFather will provide you with a token. It will look like this:

6. **Copy the Token**: Store this token securely; you will need it to configure your bot.

## Step 2: Set Up Your Project

1. **Clone or Download the Code**: Clone this repository or download the code files to your local machine.

2. **Create a Common File**:
- Inside your project directory, create a file named `common.py`.
- Open or create if not present `Common.py` in a text editor and add the following code:
  ```python
  token_code = 'YOUR_BOT_TOKEN_HERE'  # Replace with your actual bot token generated from Botfather
  ```

3. **Install Required Packages**:
Make sure you have Python installed, then install the required packages. You can do this by running:
```bash
pip install python-telegram-bot
```
## Step 3: Configure Groups and Categories

In your main bot script (where your bot code is located), modify the Category/groups  variable to include your own groups.

## Step 4: Run your own bot
```bash
python Bot.py  # Replace with the actual filename of your bot script
```
## Available Commands

Here are the commands you can use with the bot:

- **`/start`**: Start the bot and see the main menu.
- **`/help`**: View a list of available commands.
- **`/add`**: Add a group to a category.
  - After using this command, you will be prompted to select a category and provide the group name and link.
- **`/cancel`**: You can also cancel any operation at any point by typing this command.
- 
## Running Your Bot for Free on PythonAnywhere

If you want to run your bot for free, follow these steps to set it up on **[PythonAnywhere](https://www.pythonanywhere.com/)**:

1. **Register on PythonAnywhere**: Go to [www.pythonanywhere.com](https://www.pythonanywhere.com/) and create a free account.
2. **Open a Bash Console**:
   - After logging in, navigate to the **Consoles** tab and start a new **Bash console**.
3. **Install the required package**:
   - In the Bash console, run the following command to install the Telegram package:
   ```bash
   pip install python-telegram-bot[ext]
   ```
4 **Run your program**: 
Click on the run button on the console
Congratulations now your bot will now run 24/7 on PythonAnywhere!

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
