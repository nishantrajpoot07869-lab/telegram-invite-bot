import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Token environment se aayega (GitHub me visible nahi hoga)
BOT_TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.from_user.first_name
    await update.message.reply_text(f"👋 Hello {name}! Main tumhara bot hoon 😎")

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    name = update.message.from_user.first_name

    if "hi" in text or "hello" in text:
        await update.message.reply_text(f"Hello {name} 😄")
    elif "kaise ho" in text:
        await update.message.reply_text(f"Main mast hoon {name} 😎 tum batao?")
    elif "bye" in text:
        await update.message.reply_text(f"Bye {name} 👋")
    else:
        await update.message.reply_text("Samajh nahi aaya 🤔 /help try karo")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Commands:\n/start\n/help")

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_cmd))
app.add_handler(MessageHandler(filters.TEXT, reply))

print("Bot chal raha hai 🚀")
app.run_polling()
