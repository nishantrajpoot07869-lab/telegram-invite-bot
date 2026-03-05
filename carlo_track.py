from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import json
import os

TOKEN = os.getenv("BOT_TOKEN")

DATA_FILE = "invites.json"

# Load data
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        invites = json.load(f)
else:
    invites = {}

def save():
    with open(DATA_FILE, "w") as f:
        json.dump(invites, f)

# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    if context.args:
        inviter_id = context.args[0]

        if inviter_id != str(user.id):

            if inviter_id not in invites:
                invites[inviter_id] = 0

            invites[inviter_id] += 1
            save()

    await update.message.reply_text(
        "👋 Welcome!\nUse /help to see commands."
    )

# HELP
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """
🤖 Bot Commands

/start - Start bot
/invite - Get your invite link
/myinvites - Check your invites
/top - Top inviters
/help - Show commands
"""

    await update.message.reply_text(text)

# INVITE LINK
async def invite(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    bot_username = context.bot.username

    link = f"https://t.me/{bot_username}?start={user_id}"

    await update.message.reply_text(
        f"🔗 Your Invite Link:\n{link}"
    )

# MY INVITES
async def myinvites(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = str(update.effective_user.id)

    count = invites.get(user_id, 0)

    await update.message.reply_text(
        f"🎯 Your total invites: {count}"
    )

# TOP
async def top(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not invites:
        await update.message.reply_text("No invites yet.")
        return

    sorted_users = sorted(invites.items(), key=lambda x: x[1], reverse=True)

    text = "🏆 Top Inviters\n\n"

    for i, (user, count) in enumerate(sorted_users[:10], start=1):
        text += f"{i}. User {user} - {count} invites\n"

    await update.message.reply_text(text)

# BOT START
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("invite", invite))
app.add_handler(CommandHandler("myinvites", myinvites))
app.add_handler(CommandHandler("top", top))

print("Bot Started...")

app.run_polling()