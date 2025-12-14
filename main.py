import logging
import os
import random
import time

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


# ========== Menu Structure ==========

def main_menu() -> InlineKeyboardMarkup:
    """Main menu"""
    keyboard = [
        [
            InlineKeyboardButton("🎮 Mini Games Center", callback_data="menu_games"),
        ],
        [
            InlineKeyboardButton("🌈 Color Interaction", callback_data="menu_colors"),
            InlineKeyboardButton("🧠 Brain Training", callback_data="menu_brain"),
        ],
        [
            InlineKeyboardButton("✨ Fun Tools", callback_data="menu_tools"),
            InlineKeyboardButton("⚔ Adventure Tasks", callback_data="menu_adventure"),
        ],
        [
            InlineKeyboardButton("📚 Daily Inspiration", callback_data="menu_daily"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def games_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("✋ Rock Paper Scissors", callback_data="games_rps"),
            InlineKeyboardButton("🎲 Roll Dice", callback_data="games_dice"),
        ],
        [
            InlineKeyboardButton("🔢 Number Guess", callback_data="games_number_guess"),
            InlineKeyboardButton("😊 Emoji Chain", callback_data="games_emoji_chain"),
        ],
        [
            InlineKeyboardButton("⬅ Back to Mini Games", callback_data="menu_games"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def colors_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("🎨 Lucky Color Today", callback_data="color_lucky"),
            InlineKeyboardButton("🔮 Color Mood", callback_data="color_mood"),
        ],
        [
            InlineKeyboardButton("🟦 Random Color Palette", callback_data="color_palette"),
            InlineKeyboardButton("💡 Color Tips", callback_data="color_tip"),
        ],
        [
            InlineKeyboardButton("⬅ Back to Main Menu", callback_data="menu_main"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def brain_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("🧠 Brain Task of the Day", callback_data="brain_task"),
        ],
        [
            InlineKeyboardButton("🔢 Number Memory Training", callback_data="brain_memory_start"),
            InlineKeyboardButton("🧩 Logic Puzzle", callback_data="brain_puzzle"),
        ],
        [
            InlineKeyboardButton("🎯 Reaction Speed Test", callback_data="brain_reaction"),
        ],
        [
            InlineKeyboardButton("⬅ Back to Main Menu", callback_data="menu_main"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def tools_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("🎲 Random Number", callback_data="tool_random_number"),
            InlineKeyboardButton("😊 Random Emoji", callback_data="tool_random_emoji"),
        ],
        [
            InlineKeyboardButton("📜 Daily Quote", callback_data="tool_today_quote"),
            InlineKeyboardButton("❓ Decision Helper", callback_data="tool_decision"),
        ],
        [
            InlineKeyboardButton("⬅ Back to Main Menu", callback_data="menu_main"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def adventure_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("⚔ Today's Adventure Task", callback_data="adv_today"),
        ],
        [
            InlineKeyboardButton("✨ Random Equipment Generator", callback_data="adv_equipment"),
            InlineKeyboardButton("🧱 Random Stage Challenge", callback_data="adv_stage"),
        ],
        [
            InlineKeyboardButton("🎲 Adventure Dice", callback_data="adv_dice"),
        ],
        [
            InlineKeyboardButton("⬅ Back to Main Menu", callback_data="menu_main"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def daily_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("📝 Daily Question", callback_data="daily_question"),
            InlineKeyboardButton("💡 Daily Inspiration", callback_data="daily_idea"),
        ],
        [
            InlineKeyboardButton("📋 Daily To-Do Suggestion", callback_data="daily_todo"),
            InlineKeyboardButton("🧘 Relaxation Reminder", callback_data="daily_relax"),
        ],
        [
            InlineKeyboardButton("⬅ Back to Main Menu", callback_data="menu_main"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


# ========== Command Handlers ==========

START_TEXT = (
    "👋 Welcome to *UltimateFun Entertainment Bot*!\n\n"
    "This is a lightweight entertainment & utility bot.\n"
    "Here you can enjoy:\n\n"
    "🎮 *Mini Games Center*\n"
    "• Rock Paper Scissors, Dice Roll\n"
    "• Number Guessing, Emoji Chain\n\n"
    "🌈 *Color Interaction Zone*\n"
    "• Lucky Color Today, Color Mood\n"
    "• Random Palette, Color Tips\n\n"
    "🧠 *Brain Training Station*\n"
    "• Daily Brain Tasks\n"
    "• Number Memory Training, Logic Puzzles\n"
    "• Reaction Speed Test\n\n"
    "✨ *Fun Tools Box*\n"
    "• Random Numbers, Random Emojis\n"
    "• Daily Quotes, Decision Helper\n\n"
    "⚔ *Adventure Task Mode*\n"
    "• Adventure Tasks, Equipment Generator\n"
    "• Stage Challenges, Adventure Dice\n\n"
    "📚 *Daily Inspiration Zone*\n"
    "• Daily Questions, Ideas, To-Do Tips\n"
    "• Relaxation Reminders\n\n"
    "This bot provides light entertainment only.\n"
    "No money, rewards, gambling, or sensitive content is involved.\n\n"
    "👇 Tap the menu below to start!"
)
    if data == "menu_colors":
        await query.edit_message_text(
            "🌈 Color Interaction Area:",
            reply_markup=colors_menu()
        )
        return

    if data == "menu_brain":
        await query.edit_message_text(
            "🧠 Brain Training Station:",
            reply_markup=brain_menu()
        )
        return

    if data == "menu_tools":
        await query.edit_message_text(
            "✨ Fun Tools Box:",
            reply_markup=tools_menu()
        )
        return

    if data == "menu_adventure":
        await query.edit_message_text(
            "⚔ Adventure Task Mode:",
            reply_markup=adventure_menu()
        )
        return

    if data == "menu_daily":
        await query.edit_message_text(
            "📚 Daily Inspiration Area:",
            reply_markup=daily_menu()
        )
        return

    # --- Mini Games ---
    if data == "games_rps":
        await game_rps(query)
        return

    if data.startswith("games_rps_"):
        await game_rps_result(query, data)
        return

    if data == "games_dice":
        await game_dice(query)
        return

    if data == "games_number_guess":
        await game_number_guess(query, context)
        return

    if data.startswith("games_number_guess_"):
        await game_number_guess_result(query, context, data)
        return

    if data == "games_emoji_chain":
        await game_emoji_chain(query)
        return

    # --- Color Interaction ---
    if data == "color_lucky":
        await color_lucky(query)
        return

    if data == "color_mood":
        await color_mood(query)
        return

    if data == "color_palette":
        await color_palette(query)
        return

    if data == "color_tip":
        await color_tip(query)
        return

    # --- Brain Training ---
    if data == "brain_task":
        await brain_task(query)
        return

    if data == "brain_memory_start":
        await brain_memory_start(query, context)
        return

    if data.startswith("brain_memory_answer_"):
        await brain_memory_answer(query, context, data)
        return

    if data == "brain_puzzle":
        await brain_puzzle(query)
        return

    if data == "brain_reaction":
        await brain_reaction(query, context)
        return

    if data == "brain_reaction_click":
        await brain_reaction_click(query, context)
        return

    # --- Fun Tools ---
    if data == "tool_random_number":
        await tool_random_number(query)
        return

    if data == "tool_random_emoji":
        await tool_random_emoji(query)
        return

    if data == "tool_today_quote":
        await tool_today_quote(query)
        return

    if data == "tool_decision":
        await tool_decision(query)
        return

    # --- Adventure Tasks ---
    if data == "adv_today":
        await adv_today(query)
        return

    if data == "adv_equipment":
        await adv_equipment(query)
        return

    if data == "adv_stage":
        await adv_stage(query)
        return

    if data == "adv_dice":
        await adv_dice(query)
        return

    # --- Daily Inspiration ---
    if data == "daily_question":
        await daily_question(query)
        return

    if data == "daily_idea":
        await daily_idea(query)
        return

    if data == "daily_todo":
        await daily_todo(query)
        return

    if data == "daily_relax":
        await daily_relax(query)
        return

    # Fallback
    await query.edit_message_text(
        "Unsupported action. Please send /start to return to the main menu.",
        reply_markup=main_menu()
    )


# ========== Mini Games Implementation ==========

async def game_rps(query):
    keyboard = [
        [
            InlineKeyboardButton("✊ Rock", callback_data="games_rps_rock"),
            InlineKeyboardButton("✋ Paper", callback_data="games_rps_paper"),
            InlineKeyboardButton("✌ Scissors", callback_data="games_rps_scissors"),
        ],
        [
            InlineKeyboardButton("⬅ Back to Mini Games", callback_data="menu_games"),
        ],
    ]
    await query.edit_message_text(
        "✋ Rock Paper Scissors!\n\nPlease choose your move:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def game_rps_result(query, data: str):
    user_choice = data.split("_")[-1]
    options = ["rock", "paper", "scissors"]
    bot_choice = random.choice(options)

    emoji_map = {
        "rock": "✊ Rock",
        "paper": "✋ Paper",
        "scissors": "✌ Scissors",
    }

    if user_choice == bot_choice:
        result = "It's a draw! Great minds think alike 😆"
    elif (
        (user_choice == "rock" and bot_choice == "scissors") or
        (user_choice == "scissors" and bot_choice == "paper") or
        (user_choice == "paper" and bot_choice == "rock")
    ):
        result = "You win! Luck is on your side ✨"
    else:
        result = "I win! Want to try again? 😉"

    text = (
        "✋ Rock Paper Scissors Result:\n\n"
        f"You chose: {emoji_map[user_choice]}\n"
        f"I chose: {emoji_map[bot_choice]}\n\n"
        f"{result}"
    )
    await query.edit_message_text(text, reply_markup=games_menu())


async def game_dice(query):
    n = random.randint(1, 6)
    await query.edit_message_text(
        f"🎲 You rolled: {n}!\n\nTap again to roll another dice.",
        reply_markup=games_menu(),
    )


async def game_number_guess(query, context: ContextTypes.DEFAULT_TYPE):
    secret = random.randint(1, 5)
    context.user_data["guess_number"] = secret

    keyboard = [
        [
            InlineKeyboardButton("1", callback_data="games_number_guess_1"),
            InlineKeyboardButton("2", callback_data="games_number_guess_2"),
            InlineKeyboardButton("3", callback_data="games_number_guess_3"),
            InlineKeyboardButton("4", callback_data="games_number_guess_4"),
            InlineKeyboardButton("5", callback_data="games_number_guess_5"),
        ],
        [
            InlineKeyboardButton("⬅ Back to Mini Games", callback_data="menu_games"),
        ],
    ]
    await query.edit_message_text(
        "🔢 Number Guess Game:\n\nI've chosen a number between 1 and 5.\nCan you guess it?",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
# ========== Daily Inspiration Features ==========

async def daily_question(query):
    questions = [
        "📝 Question: If you could only finish one thing today, what would it be?",
        "📝 Question: What small moment recently made you feel happy?",
        "📝 Question: What new habit would you like to build?",
    ]
    await query.edit_message_text(
        random.choice(questions),
        reply_markup=daily_menu(),
    )


async def daily_idea(query):
    ideas = [
        "💡 Idea: Write down 3 ideas that came to your mind today, no matter how small.",
        "💡 Idea: Describe today’s mood in one sentence and write it down.",
        "💡 Idea: Leave a short message for your future self.",
    ]
    await query.edit_message_text(
        random.choice(ideas),
        reply_markup=daily_menu(),
    )


async def daily_todo(query):
    todos = [
        "📋 Suggested To-Do List:\n"
        "• One must-do task\n"
        "• One want-to-do task\n"
        "• One relaxing activity",
        "📋 Suggested To-Do List:\n"
        "• Spend 5 minutes organizing a corner\n"
        "• Reply to one unread message\n"
        "• Leave some time to do nothing",
    ]
    await query.edit_message_text(
        random.choice(todos),
        reply_markup=daily_menu(),
    )


async def daily_relax(query):
    relax = [
        "🧘 Relax Tip: Close your eyes and take 5 deep breaths, focusing only on breathing.",
        "🧘 Relax Tip: Listen to one song you like without looking at your phone.",
        "🧘 Relax Tip: Do 10 seconds of stretching to wake up your body.",
    ]
    await query.edit_message_text(
        random.choice(relax),
        reply_markup=daily_menu(),
    )


# ========== Main Entry Point ==========

def main():
    if not BOT_TOKEN:
        raise RuntimeError(
            "BOT_TOKEN environment variable is not set. Please configure it before running."
        )

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("about", about_cmd))

    # Buttons
    app.add_handler(CallbackQueryHandler(button_handler))

    logger.info("UltimateFun Telegram Bot (English Version) has started.")
    app.run_polling()


if __name__ == "__main__":
    main()
