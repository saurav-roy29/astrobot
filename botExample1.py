import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, Application

# Replace with your bot token
BOT_TOKEN = "8146509754:AAHLIr9CT_IQrDBC-NtynBkikiDWqoSDdmw"

# Aztro API Horoscope Function
def get_horoscope(sign: str) -> str:
    url = f"https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily?sign={sign}"
    response = requests.get(url)
    data = response.json()["data"]
    
    return f"🔮 {data['horoscope_data']}"

# Telegram Bot Commands
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "✨ *Welcome to AstroBot!* ✨\n\n"
        "Get your daily horoscope with /horoscope <sign>\n"
        "Example: `/horoscope aries`\n\n"
        "Available signs: aries, taurus, gemini, cancer, leo, virgo, libra, scorpio, sagittarius, capricorn, aquarius, pisces",
        parse_mode="Markdown"
    )

async def horoscope_command(update: Update, context: CallbackContext):
    if not context.args:
        await update.message.reply_text("Please specify your zodiac sign! Example: `/horoscope aries`", parse_mode="Markdown")
        return
    
    sign = context.args[0]
    valid_signs = [
        "aries", "taurus", "gemini", "cancer", "leo", "virgo",
        "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"
    ]
    
    if sign.lower() not in valid_signs:
        await update.message.reply_text("❌ Invalid zodiac sign! Use /horoscope <sign>")
        return
    
    try:
        horoscope_text = get_horoscope(sign)
        await update.message.reply_text(horoscope_text, parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text("🔮 Error fetching horoscope. Try again later!")

# Main Bot Setup (Updated for PTB v20+)
def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("horoscope", horoscope_command))
    
    application.run_polling()

if __name__ == "__main__":
    main()