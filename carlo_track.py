from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os, json

TOKEN = os.getenv("BOT_TOKEN")
invite_data_file = "invite_data.json"

if os.path.exists(invite_data_file):
    with open(invite_data_file, "r") as f:
        invite_data = json.load(f)
else:
    invite_data = {}

def save_data():
    with open(invite_data_file, "w") as f:
        json.dump(invite_data, f)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! 👋\nInvite bot working hai.\nUse /top to see leaderboard.")

async def new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        inviter = update.message.from_user
        inviter_id = str(inviter.id)

        if inviter_id not in invite_data:
            invite_data[inviter_id] = {"name": inviter.first_name, "count": 0}

        invite_data[inviter_id]["count"] += 1
        save_data()

        await update.message.reply_text(
            f"{member.first_name} welcome! 🎉\n"
            f"{inviter.first_name} ne invite kiya 💪\n"
            f"Total invites: {invite_data[inviter_id]['count']}"
        )

async def top(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not invite_data:
        await update.message.reply_text("Abhi koi data nahi hai 😢")
        return

    sorted_data = sorted(invite_data.values(), key=lambda x: x["count"], reverse=True)

    text = "🏆 Top Inviters:\n\n"
    for i, user in enumerate(sorted_data[:5], start=1):
        text += f"{i}. {user['name']} - {user['count']} invites\n"

    await update.message.reply_text(text)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("top", top))
app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_member))

app.run_polling()