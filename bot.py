import logging
import requests
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Telegram Bot Token (Replace with your bot token)
BOT_TOKEN = "7472949323:AAGUpJOIwfcowW1s5FjXCmP97FtPj__GlRI"

# Your Telegram Channel (Replace with your channel username)
CHANNEL_USERNAME = "@mdxhacker"

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: CallbackContext):
    """Handles the /start command."""
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id

    if is_user_in_channel(user_id):
        await update.message.reply_text("✅ You have joined the channel! Let's start the prediction.")
        await send_prediction(chat_id, context)
    else:
        await update.message.reply_text(f"❌ You must join {CHANNEL_USERNAME} to use this bot. Join and then press /start.")

def is_user_in_channel(user_id):
    """Checks if the user is a member of the required Telegram channel."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getChatMember?chat_id={CHANNEL_USERNAME}&user_id={user_id}"
    response = requests.get(url).json()

    if "result" in response and "status" in response["result"]:
        status = response["result"]["status"]
        return status in ["member", "administrator", "creator"]
    
    return False

def get_current_period():
    """Generates the current period number based on the given logic."""
    now = datetime.now()
    start_hour = 5
    start_minute = 29

    formatted_date = now.strftime("%Y%m%d")
    hours = now.hour
    minutes = now.minute

    # Calculate elapsed minutes since 5:29 AM
    elapsed_minutes = (hours * 60 + minutes) - (start_hour * 60 + start_minute)
    if elapsed_minutes < 0:
        elapsed_minutes = 0

    # Generate period number
    period_number = "10001" + str(elapsed_minutes).zfill(4)

    return formatted_date + period_number

def get_results():
    """Returns a random prediction (BIG or SMALL)."""
    return "BIGG" if requests.get("https://www.random.org/integers/?num=1&min=0&max=1&col=1&base=10&format=plain&rnd=new").text.strip() == "1" else "SMALL"

async def send_prediction(chat_id, context):
    """Sends the prediction result to the user."""
    current_period = get_current_period()
    prediction = get_results()

    message = f"📊 <b>Prediction Result</b>\n" \
              f"🔢 <b>Period:</b> {current_period}\n" \
              f"🎲 <b>Prediction:</b> {prediction}"

    await context.bot.send_message(chat_id=chat_id, text=message, parse_mode="HTML")

def main():
    """Main function to start the bot."""
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
