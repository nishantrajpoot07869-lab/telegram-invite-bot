import json
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")

DATA_FILE = "invites.json"

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        invites = json.load(f)
else:
    invites = {}

def save():
    with open(DATA_FILE, "w") as f:
        json.dump(invites, f)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Invite Counter Bot Ready!")

async def invites_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    count = invites.get(user_id, 0)

    await update.message.reply_text(f"📊 Tumhare invites: {count}")

async def new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    inviter = update.message.from_user

    for member in update.message.new_chat_members:
        user_id = str(inviter.id)

        if user_id not in invites:
            invites[user_id] = 0

        invites[user_id] += 1
        save()

        await update.message.reply_text(
            f"🎉 {inviter.first_name} ne {member.first_name} ko add kiya!\n"
            f"Total invites: {invites[user_id]}"
        )

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("invites", invites_cmd))
app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_member))

app.run_polling()