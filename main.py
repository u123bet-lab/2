import os
import random
import time
import logging

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# ========== Basic Configuration ==========
BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


# ========== Menus ==========
def main_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("🌤 Daily Start", callback_data="menu_day")],
        [
            InlineKeyboardButton("✅ Habits & Small Goals", callback_data="menu_habit"),
            InlineKeyboardButton("😊 Mood & Emotions", callback_data="menu_mood"),
        ],
        [
            InlineKeyboardButton("🧠 Mini Quizzes & Q&A", callback_data="menu_quiz"),
            InlineKeyboardButton("📚 Light Reading & Quotes", callback_data="menu_read"),
        ],
        [
            InlineKeyboardButton("🎲 Random Mini Tools", callback_data="menu_random"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def day_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("📅 Today's Quote", callback_data="day_sentence"),
            InlineKeyboardButton("📋 Today's Tip", callback_data="day_tip"),
        ],
        [
            InlineKeyboardButton("🧭 Today's Direction", callback_data="day_direction"),
        ],
        [InlineKeyboardButton("⬅ Back to Home", callback_data="menu_main")],
    ]
    return InlineKeyboardMarkup(keyboard)


def habit_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("✅ Generate Small Goal", callback_data="habit_goal"),
            InlineKeyboardButton("🔁 Habit Micro-Action", callback_data="habit_action"),
        ],
        [
            InlineKeyboardButton("🧹 Small Tidy-Up", callback_data="habit_clean"),
            InlineKeyboardButton("🚶 Micro Exercise", callback_data="habit_move"),
        ],
        [InlineKeyboardButton("⬅ Back to Home", callback_data="menu_main")],
    ]
    return InlineKeyboardMarkup(habit_menu)


def mood_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("💬 Mood Quote", callback_data="mood_text"),
            InlineKeyboardButton("🎨 Mood Color", callback_data="mood_color"),
        ],
        [
            InlineKeyboardButton("🧘 Simple Relaxation", callback_data="mood_relax"),
            InlineKeyboardButton("❤️ Self-Care", callback_data="mood_selfcare"),
        ],
        [InlineKeyboardButton("⬅ Back to Home", callback_data="menu_main")],
    ]
    return InlineKeyboardMarkup(keyboard)


def quiz_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("🧠 Thinking Question", callback_data="quiz_think"),
            InlineKeyboardButton("🔢 Number Challenge", callback_data="quiz_number"),
        ],
        [
            InlineKeyboardButton("👀 Reaction Speed", callback_data="quiz_reaction"),
        ],
        [InlineKeyboardButton("⬅ Back to Home", callback_data="menu_main")],
    ]
    return InlineKeyboardMarkup(quiz_menu)


def read_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("📖 Gentle Quotes", callback_data="read_soft"),
            InlineKeyboardButton("💡 Idea Sparks", callback_data="read_idea"),
        ],
        [
            InlineKeyboardButton("📝 Reflection Questions", callback_data="read_question"),
        ],
        [InlineKeyboardButton("⬅ Back to Home", callback_data="menu_main")],
    ]
    return InlineKeyboardMarkup(read_menu)


def random_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("🎲 Random Number", callback_data="rand_number"),
            InlineKeyboardButton("😊 Random Emoji", callback_data="rand_emoji"),
        ],
        [
            InlineKeyboardButton("📌 Random Mini Task", callback_data="rand_task"),
            InlineKeyboardButton("✨ Random Inspiration", callback_data="rand_inspire"),
        ],
        [InlineKeyboardButton("⬅ Back to Home", callback_data="menu_main")],
    ]
    return InlineKeyboardMarkup(random_menu)


# ========== /start /help /about ==========
START_TEXT = (
    "👋 Welcome to **Light Moments · Life Hub**!\n\n"
    "This is a Chinese-language bot focused on *daily small goals, emotional care, "
    "light quizzes, and random inspiration*.\n\n"
    "Here you can:\n"
    "🌤 View small tips to start your day\n"
    "✅ Generate simple goals and habit micro-actions\n"
    "😊 Express your mood with a sentence or a color\n"
    "🧠 Do a few light thinking tasks and mini tests\n"
    "📚 Read gentle quotes and reflection questions\n"
    "🎲 Get random numbers, emojis, tasks, or inspiration\n\n"
    "This bot only provides light, healthy text interactions. "
    "It does not involve money, rewards, gambling, investment, or sensitive content.\n\n"
    "👇 Use the buttons below to choose what you'd like to explore right now:"
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text(
            START_TEXT, reply_markup=main_menu(), parse_mode="Markdown"
        )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📝 How to Use\n\n"
        "• Send /start to open the main menu\n"
        "• Use the buttons to enter different modules: Daily Start / Habits & Goals / "
        "Mood Tools / Mini Quizzes / Light Reading / Random Tools\n"
        "• Each button provides corresponding text content or interactions\n"
        "• If the interface gets stuck, send /start again to return to the home page\n"
    )
    await update.message.reply_text(text)


async def about_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "ℹ️ About **Light Moments · Life Hub**\n\n"
        "This is a small bot designed to help you relax during short breaks:\n"
        "• Encourage tiny changes through small goals and micro tasks\n"
        "• Take care of your mood with emotional tools\n"
        "• Activate your mind with mini quizzes and light reading\n"
        "All content is healthy, non-commercial, and free of sensitive information."
    )
    await update.message.reply_text(text)


# ========== Button Router ==========
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    await query.answer()

    # Menu navigation
    if data == "menu_main":
        await query.edit_message_text("🏠 Back to Home:", reply_markup=main_menu())
        return
    if data == "menu_day":
        await query.edit_message_text("🌤 Daily Start:", reply_markup=day_menu())
        return
    if data == "menu_habit":
        await query.edit_message_text("✅ Habits & Small Goals:", reply_markup=habit_menu())
        return
    if data == "menu_mood":
        await query.edit_message_text("😊 Mood & Emotions:", reply_markup=mood_menu())
        return
    if data == "menu_quiz":
        await query.edit_message_text("🧠 Mini Quizzes & Q&A:", reply_markup=quiz_menu())
        return
    if data == "menu_read":
        await query.edit_message_text("📚 Light Reading & Quotes:", reply_markup=read_menu())
        return
    if data == "menu_random":
        await query.edit_message_text("🎲 Random Mini Tools:", reply_markup=random_menu())
        return

    # ===== Daily Start =====
    if data == "day_sentence":
        sentences = [
            "You can take things slowly today, just don't stop.",
            "Setting a very small goal for today is enough.",
            "Even eating one good meal is a way of living seriously.",
        ]
        await query.edit_message_text(
            "📅 Today's Quote:\n\n" + random.choice(sentences),
            reply_markup=day_menu(),
        )
        return

    if data == "day_tip":
        tips = [
            "Try using your phone a little less today and keep some time for yourself.",
            "Pick a small corner you've wanted to tidy and spend 3 minutes on it.",
            "If today is busy, try sorting tasks into 'must-do' and 'can wait'.",
        ]
        await query.edit_message_text(
            "📋 Today's Tip:\n\n" + random.choice(tips),
            reply_markup=day_menu(),
        )
        return

    if data == "day_direction":
        directions = [
            "Treat today as a 'foundation day' and do small things that matter long-term.",
            "Treat today as a 'reset day' and allow yourself to slow down.",
            "Treat today as a 'try something new' day with a small unfamiliar action.",
        ]
        await query.edit_message_text(
            "🧭 Today's Direction:\n\n" + random.choice(directions),
            reply_markup=day_menu(),
        )
        return

    # ===== Habits & Small Goals =====
    if data == "habit_goal":
        goals = [
            "Complete one small goal that takes only 5 minutes.",
            "Focus on just one thing you care about today.",
            "Set a goal where 'done is enough, not perfect'.",
        ]
        await query.edit_message_text(
            "✅ Small Goal Suggestion:\n\n" + random.choice(goals),
            reply_markup=habit_menu(),
        )
        return

    if data == "habit_action":
        actions = [
            "Drink a glass of water and say 'good job' to yourself.",
            "Stand up and stretch your shoulders and neck for 30 seconds.",
            "Put away one item on your desk that you don't use often.",
        ]
        await query.edit_message_text(
            "🔁 Habit Micro-Action:\n\n" + random.choice(actions),
            reply_markup=habit_menu(),
        )
        return

    if data == "habit_clean":
        texts = [
            "Pick one drawer or folder and spend 2 minutes deleting or discarding items.",
            "Neatly group scattered items on your desk to make it visually calmer.",
        ]
        await query.edit_message_text(
            "🧹 Small Tidy-Up:\n\n" + random.choice(texts),
            reply_markup=habit_menu(),
        )
        return

    if data == "habit_move":
        moves = [
            "Walk lightly in place for 30 seconds.",
            "Take 10 slow deep breaths while shrugging your shoulders to relax.",
            "Stand up, walk to another room, and come back as a 'mini walk'.",
        ]
        await query.edit_message_text(
            "🚶 Micro Exercise:\n\n" + random.choice(moves),
            reply_markup=habit_menu(),
        )
        return

    # ===== Mood & Emotions =====
    if data == "mood_text":
        moods = [
            "It's okay to feel tired — it means you've been trying.",
            "Emotions rise and fall, but you always deserve kindness.",
            "It's okay to allow yourself a not-so-great day.",
        ]
        await query.edit_message_text(
            "💬 Mood Quote:\n\n" + random.choice(moods),
            reply_markup=mood_menu(),
        )
        return

    if data == "mood_color":
        colors = [
            "🔵 Blue mood: good for quiet time and organizing thoughts.",
            "🟢 Green mood: good for relaxing and listening to music.",
            "🟡 Yellow mood: good for chatting with friends.",
            "🟣 Purple mood: good for writing or brainstorming.",
        ]
        await query.edit_message_text(
            "🎨 Mood Color Tip:\n\n" + random.choice(colors),
            reply_markup=mood_menu(),
        )
        return

    if data == "mood_relax":
        text = (
            "🧘 Simple Relaxation Exercise:\n\n"
            "1️⃣ Sit in a comfortable position\n"
            "2️⃣ Take 5 slow, deep breaths\n"
            "3️⃣ With each exhale, imagine releasing a bit of tension\n"
        )
        await query.edit_message_text(text, reply_markup=mood_menu())
        return

    if data == "mood_selfcare":
        texts = [
            "You can be a little more gentle with yourself — perfection isn't required.",
            "Try giving yourself a small compliment, like 'I did my best today'.",
        ]
        await query.edit_message_text(
            "❤️ Self-Care:\n\n" + random.choice(texts),
            reply_markup=mood_menu(),
        )
        return

    # ===== Mini Quizzes & Q&A =====
    if data == "quiz_think":
        qs = [
            "🧠 Think About It:\n\nIf you had to give today a title, what would it be?",
            "🧠 Think About It:\n\nWhat's one small improvement you've noticed recently?",
        ]
        await query.edit_message_text(
            random.choice(qs),
            reply_markup=quiz_menu(),
        )
        return

    if data == "quiz_number":
        number = random.randint(10, 99)
        text = (
            f"🔢 Number Challenge:\n\nStart from {number} in your head and subtract 3 each time. "
            "How far can you go?"
        )
        await query.edit_message_text(text, reply_markup=quiz_menu())
        return

    if data == "quiz_reaction":
        context.user_data["reaction_start"] = time.time()
        keyboard = [
            [InlineKeyboardButton("⚡ Click Now!", callback_data="quiz_reaction_click")],
            [InlineKeyboardButton("⬅ Back", callback_data="menu_quiz")],
        ]
        await query.edit_message_text(
            "Click the button as soon as you see it to test your reaction speed:",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return

    if data == "quiz_reaction_click":
        start = context.user_data.get("reaction_start")
        if not start:
            msg = "Test data expired. Please start again from the menu."
        else:
            ms = int((time.time() - start) * 1000)
            msg = f"🎯 Your reaction time: {ms} ms."
        await query.edit_message_text(msg, reply_markup=quiz_menu())
        return

    # ===== Light Reading & Quotes =====
    if data == "read_soft":
        sentences = [
            "You don't have to be amazing all the time — just remember to like yourself sometimes.",
            "Many things don't need to be done all at once; little by little is fine.",
        ]
        await query.edit_message_text(
            "📖 Gentle Quote:\n\n" + random.choice(sentences),
            reply_markup=read_menu(),
        )
        return

    if data == "read_idea":
        ideas = [
            "Try noting one small thing today that felt 'nice'.",
            "Write one single line to your future self a month from now.",
        ]
        await query.edit_message_text(
            "💡 Idea Spark:\n\n" + random.choice(ideas),
            reply_markup=read_menu(),
        )
        return

    if data == "read_question":
        qs = [
            "📝 Reflection:\n\nIf the past week were weather, what would it be like?",
            "📝 Reflection:\n\nWhat is something you're already doing much better than before?",
        ]
        await query.edit_message_text(
            random.choice(qs),
            reply_markup=read_menu(),
        )
        return

    # ===== Random Mini Tools =====
    if data == "rand_number":
        n = random.randint(0, 100)
        await query.edit_message_text(
            f"🎲 Random Number (0–100): {n}",
            reply_markup=random_menu(),
        )
        return

    if data == "rand_emoji":
        emojis = ["😀", "😆", "😎", "🥳", "🤩", "🤗", "🙌", "🌈", "⭐", "✨", "🍀"]
        seq = " ".join(random.sample(emojis, 5))
        await query.edit_message_text(
            "😊 Random Emoji Combo:\n\n" + seq,
            reply_markup=random_menu(),
        )
        return

    if data == "rand_task":
        tasks = [
            "Take a photo of something in front of you that feels 'nice'.",
            "Find one small thing you can finish in 3 minutes and do it now.",
            "Put your phone down for 2 minutes and just daydream.",
        ]
        await query.edit_message_text(
            "📌 Random Mini Task:\n\n" + random.choice(tasks),
            reply_markup=random_menu(),
        )
        return

    if data == "rand_inspire":
        ins = [
            "Pick a theme word for today, like: slow / reset / light.",
            "Think of one small thing that could make you feel better in 5 minutes.",
        ]
        await query.edit_message_text(
            "✨ Random Inspiration:\n\n" + random.choice(ins),
            reply_markup=random_menu(),
        )
        return

    # Fallback
    await query.edit_message_text(
        "This action is not supported. Please send /start to return home.",
        reply_markup=main_menu(),
    )


# ========== Main Entry ==========
def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN environment variable is not set!")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("about", about_cmd))
    app.add_handler(CallbackQueryHandler(button_handler))

    logger.info("Light Moments · Life Hub Bot has started")
    app.run_polling()


if __name__ == "__main__":
    main()
