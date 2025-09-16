import json
import os
import random
from telegram import Updatem
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

# ================== Config ==================
USERS_FILE = "users.json"
POOLS_FILE = "pools.json"
CHATS_FILE = "chats.json" 
ADMIN_USERNAME = "bluedeathqr"  # Only this username can upload/broadcast

# ================== Data Handling ==================
def load_data(file, default):
    if os.path.exists(file):
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
    return default

def save_data(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

users = load_data(USERS_FILE, {})
pools = load_data(POOLS_FILE, {})
chats = ["-1001991391529","1931535723","6464558791"]

def save_users(): save_data(USERS_FILE, users)
def save_pools(): save_data(POOLS_FILE, pools)
def save_chats(): save_data(CHATS_FILE, chats)

# ================== Chat Tracking ==================
async def track_chats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id not in chats:
        chats.append(chat_id)
        save_chats()

# ================== Badges & XP ==================
def get_badge(correct: int) -> str:
    if correct >= 100: return "👑 Legend"
    elif correct >= 50: return "🏆 Master"
    elif correct >= 25: return "🥇 Expert"
    elif correct >= 10: return "🥈 Intermediate"
    else: return "🥉 Beginner"

def calculate_xp_and_level(scores: dict):
    total_correct = sum(pool.get("correct",0) for pool in scores.values())
    total_wrong = sum(pool.get("wrong",0) for pool in scores.values())
    xp = total_correct*10 + total_wrong*2
    level = 1
    thresholds = [50,150,300,500,800,1200]
    for i,t in enumerate(thresholds,start=1):
        if xp>=t: level=i+1
    return xp, level, total_correct, total_wrong

def update_user_progress(user_id: str):
    if user_id not in users: return
    scores = users[user_id].get("scores",{})
    xp, level, total_correct, total_wrong = calculate_xp_and_level(scores)
    users[user_id].update({
        "xp":xp, "level":level,
        "total_correct":total_correct, "total_wrong":total_wrong
    })
    save_users()

def progress_bar(xp:int,level:int,bar_length:int=10)->str:
    thresholds=[50,150,300,500,800,1200]
    if level-1<len(thresholds):
        current_level_min = 0 if level==1 else thresholds[level-2]
        next_level_xp = thresholds[level-1]
    else:
        current_level_min = thresholds[-1]+(level-len(thresholds)-1)*500
        next_level_xp=current_level_min+500
    progress = xp - current_level_min
    required = next_level_xp - current_level_min
    filled = int(bar_length*progress/required)
    empty = bar_length-filled
    percent=int(progress/required*100)
    return f"[{'█'*filled}{'░'*empty}] {progress}/{required} XP ({percent}%)"

# ================== Command Handlers ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await track_chats(update, context)
    await update.message.reply_text("👋 Welcome!\nUse /help to see all commands.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    commands = (
        "/start – Welcome message\n"
        "/help – List all commands\n"
        "/signup <name> – Register\n"
        "/myscore – Show your score\n"
        "/quiz – Play a quiz (interactive)\n"
        "/listpools – Show available pools\n"
        "/leaderboard <pool_name> – Show pool leaderboard\n"
        "/topplayers – Show global leaderboard\n"
        "/uploadpool – Admin only: upload new pool\n"
        "/broadcast <message> – Admin only: broadcast message"
    )
    await update.message.reply_text(commands)

async def signup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id=str(update.effective_user.id)
    if user_id in users:
        await update.message.reply_text("✅ Already registered.")
        return
    if not context.args:
        await update.message.reply_text("Usage: /signup <Your Name>")
        return
    name=" ".join(context.args)
    users[user_id]={"name":name,"scores":{},"xp":0,"level":1,"total_correct":0,"total_wrong":0}
    save_users()
    await update.message.reply_text(f"🎉 Registered as {name}!")

async def myscore(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id=str(update.effective_user.id)
    if user_id not in users:
        await update.message.reply_text("❌ Not registered. Use /signup first.")
        return
    update_user_progress(user_id)
    u=users[user_id]
    badge=get_badge(u["total_correct"])
    bar=progress_bar(u["xp"],u["level"])
    details=[]
    for pool_name,result in u.get("scores",{}).items():
        details.append(f"{pool_name}: ✅ {result.get('correct',0)} | ❌ {result.get('wrong',0)}")
    msg="\n".join(details) if details else "No pool scores yet."
    await update.message.reply_text(
        f"👤 {u['name']}\n{msg}\n\n"
        f"Total: ✅ {u['total_correct']} | ❌ {u['total_wrong']}\n"
        f"🏅 Badge: {badge}\n⭐ XP: {u['xp']} | Level: {u['level']}\n{bar}"
    )

async def listpools(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not pools:
        await update.message.reply_text("No pools available.")
        return
    await update.message.reply_text("Available Pools:\n"+"\n".join(pools.keys()))

async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /leaderboard <pool_name>")
        return
    pool_name=" ".join(context.args)
    ranking=[]
    for uid,info in users.items():
        scores=info.get("scores",{})
        if pool_name in scores:
            s={pool_name:scores[pool_name]}
            xp,level,corr,wrong=calculate_xp_and_level(s)
            if corr+wrong>0: ranking.append((info["name"],corr,wrong,xp,level))
    if not ranking:
        await update.message.reply_text(f"No scores yet for '{pool_name}'.")
        return
    ranking.sort(key=lambda x:(x[1],x[3]),reverse=True)
    lines=[]
    for i,(name,corr,wrong,xp,level) in enumerate(ranking[:10],start=1):
        badge=get_badge(corr)
        bar=progress_bar(xp,level,bar_length=5)
        lines.append(f"{i}. {name} ✅{corr} ❌{wrong} {badge} ⭐{xp} (Lvl {level})\n{bar}")
    await update.message.reply_text(f"🏆 Leaderboard: {pool_name}\n"+"\n".join(lines))

async def topplayers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ranking=[]
    for uid,info in users.items():
        if info.get("total_correct",0)+info.get("total_wrong",0)>0:
            ranking.append((info["name"],info["total_correct"],info["total_wrong"],info["xp"],info["level"]))
    if not ranking:
        await update.message.reply_text("No users with scores yet.")
        return
    ranking.sort(key=lambda x:(x[1],x[3]),reverse=True)
    lines=[]
    for i,(name,corr,wrong,xp,level) in enumerate(ranking[:10],start=1):
        badge=get_badge(corr)
        bar=progress_bar(xp,level,bar_length=5)
        lines.append(f"{i}. {name} ✅{corr} ❌{wrong} {badge} ⭐{xp} (Lvl {level})\n{bar}")
    await update.message.reply_text("🌍 Global Leaderboard\n"+"\n".join(lines))

# ================== Interactive Quiz ==================
ASK_POOL = 1

async def start_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await track_chats(update, context)
    if not pools:
        await update.message.reply_text("❌ No pools available.")
        return ConversationHandler.END
    pool_list = "\n".join(pools.keys())
    await update.message.reply_text(f"Which pool do you want to play?\nAvailable pools:\n{pool_list}")
    return ASK_POOL

async def receive_pool(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pool_name = update.message.text
    if pool_name not in pools:
        await update.message.reply_text(f"❌ Pool '{pool_name}' not found. Try again.")
        return ASK_POOL  # Wait for valid input
    question = random.choice(pools[pool_name])
    await context.bot.send_poll(
        chat_id=update.effective_chat.id,
        question=question["question"],
        options=question["options"],
        type="quiz",
        correct_option_id=question["answer"],
        is_anonymous=False
    )
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Quiz cancelled.")
    return ConversationHandler.END
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.username != ADMIN_USERNAME:
        await update.message.reply_text("❌ Unauthorized.")
        return

    if not context.args:
        await update.message.reply_text("Usage: /broadcast <pool_name>")
        return

    pool_name = " ".join(context.args)  # join in case pool name has spaces

    if pool_name not in pools:
        await update.message.reply_text(f"❌ Pool '{pool_name}' not found.")
        return

    questions = pools[pool_name]

    await update.message.reply_text(f"📢 Broadcasting all questions from pool '{pool_name}' to all chats...")

    for chat_id in chats:
        for q in questions:
            try:
                await context.bot.send_poll(
                    chat_id=chat_id,
                    question=q["question"],
                    options=q["options"],
                    type="quiz",
                    correct_option_id=q["answer"],
                    is_anonymous= True
                )
            except Exception as e:
                print(f"⚠️ Could not send to {chat_id}: {e}")

    await update.message.reply_text("✅ Broadcast completed!")

# ================== Main ==================
def main():
    TOKEN = "6848914636:AAG3Fv30SQig1x9gqdlImhiOmK3mmaAYCHY"
    app = ApplicationBuilder().token(TOKEN).build()

    # Normal commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("signup", signup))
    app.add_handler(CommandHandler("myscore", myscore))
    app.add_handler(CommandHandler("listpools", listpools))
    app.add_handler(CommandHandler("leaderboard", leaderboard))
    app.add_handler(CommandHandler("topplayers", topplayers))
    app.add_handler(CommandHandler("broadcast",broadcast))
    # Interactive quiz
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("quiz", start_quiz)],
        states={
            ASK_POOL: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_pool)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    app.add_handler(conv_handler)
    # Track all chats
    app.add_handler(MessageHandler(filters.ALL, track_chats))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
