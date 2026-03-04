from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import json
import os

# Bot token (हम Render में Environment Variable से set करेंगे)
TOKEN = os.getenv("TOKEN")  # Render में TOKEN डालेंगे

DATA_FILE = "data.json"

# Load old data
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        invite_data = json.load(f)
else:
    invite_data = {}

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(invite_data, f)

# New member join
async def new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        inviter = update.message.from_user
        inviter_id = str(inviter.id)

        if inviter_id not in invite_data:
            invite_data[inviter_id] = {
                "name": inviter.first_name,
                "count": 0
            }

        invite_data[inviter_id]["count"] += 1
        save_data()

        await update.message.reply_text(
            f"🎉 Welcome {member.first_name} 😄\n"
            f"💪 Added by: {inviter.first_name}\n"
            f"🔥 Total invites: {invite_data[inviter_id]['count']}"
        )

# Top command
async def top(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not invite_data:
        await update.message.reply_text("Abhi koi data nahi hai 😢")
        return

    sorted_data = sorted(invite_data.values(), key=lambda x: x["count"], reverse=True)
    text = "🏆 Top Inviters:\n\n"

    for i, user in enumerate(sorted_data[:5], start=1):
        text += f"{i}. {user['name']} - {user['count']} invites\n"

    await update.message.reply_text(text)

# My invites command
async def my(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    if user_id in invite_data:
        count = invite_data[user_id]["count"]
        await update.message.reply_text(f"🔥 Tere total invites: {count}")
    else:
        await update.message.reply_text("Abhi tak tune kisi ko add nahi kiya 😢")

# Bot setup
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_member))
app.add_handler(CommandHandler("top", top))
app.add_handler(CommandHandler("my", my))

app.run_polling()
