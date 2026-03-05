from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
import json, os

TOKEN = os.getenv("BOT_TOKEN")

DATA_FILE = "data.json"

if os.path.exists(DATA_FILE):
    with open(DATA_FILE) as f:
        data = json.load(f)
else:
    data = {}

def save():
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Invite Counter Bot Active!")

async def new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    inviter = update.message.from_user.id
    name = update.message.from_user.first_name

    if str(inviter) not in data:
        data[str(inviter)] = 0

    count = len(update.message.new_chat_members)
    data[str(inviter)] += count

    save()

    await update.message.reply_text(
        f"{name} added {count} member(s)\nTotal invites: {data[str(inviter)]}"
    )

async def invites(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user.id
    count = data.get(str(user), 0)
    await update.message.reply_text(f"You invited {count} members")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("invites", invites))
app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_member))

app.run_polling()