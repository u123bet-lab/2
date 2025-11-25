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

# ========== 基础配置 ==========
BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


# ========== 菜单结构 ==========

def main_menu() -> InlineKeyboardMarkup:
    """主菜单"""
    keyboard = [
        [
            InlineKeyboardButton("🎮 小游戏中心", callback_data="menu_games"),
        ],
        [
            InlineKeyboardButton("🌈 色彩互动", callback_data="menu_colors"),
            InlineKeyboardButton("🧠 脑力训练", callback_data="menu_brain"),
        ],
        [
            InlineKeyboardButton("✨ 娱乐工具", callback_data="menu_tools"),
            InlineKeyboardButton("⚔ 冒险任务", callback_data="menu_adventure"),
        ],
        [
            InlineKeyboardButton("📚 每日灵感", callback_data="menu_daily"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def games_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("✋ 石头剪刀布", callback_data="games_rps"),
            InlineKeyboardButton("🎲 掷骰子", callback_data="games_dice"),
        ],
        [
            InlineKeyboardButton("🔢 数字猜拳", callback_data="games_number_guess"),
            InlineKeyboardButton("😊 表情接龙", callback_data="games_emoji_chain"),
        ],
        [
            InlineKeyboardButton("⬅ 返回主菜单", callback_data="menu_main"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def colors_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("🎨 今日幸运色", callback_data="color_lucky"),
            InlineKeyboardButton("🔮 色彩心情", callback_data="color_mood"),
        ],
        [
            InlineKeyboardButton("🟦 随机色卡", callback_data="color_palette"),
            InlineKeyboardButton("💡 色彩小建议", callback_data="color_tip"),
        ],
        [
            InlineKeyboardButton("⬅ 返回主菜单", callback_data="menu_main"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def brain_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("🧠 今日脑力任务", callback_data="brain_task"),
        ],
        [
            InlineKeyboardButton("🔢 数字记忆训练", callback_data="brain_memory_start"),
            InlineKeyboardButton("🧩 逻辑小谜题", callback_data="brain_puzzle"),
        ],
        [
            InlineKeyboardButton("🎯 反应速度测试", callback_data="brain_reaction"),
        ],
        [
            InlineKeyboardButton("⬅ 返回主菜单", callback_data="menu_main"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def tools_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("🎲 随机数字", callback_data="tool_random_number"),
            InlineKeyboardButton("😊 随机表情", callback_data="tool_random_emoji"),
        ],
        [
            InlineKeyboardButton("📜 每日签文", callback_data="tool_today_quote"),
            InlineKeyboardButton("❓ 小决定助手", callback_data="tool_decision"),
        ],
        [
            InlineKeyboardButton("⬅ 返回主菜单", callback_data="menu_main"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def adventure_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("⚔ 今日冒险任务", callback_data="adv_today"),
        ],
        [
            InlineKeyboardButton("✨ 随机装备生成", callback_data="adv_equipment"),
            InlineKeyboardButton("🧱 随机关卡挑战", callback_data="adv_stage"),
        ],
        [
            InlineKeyboardButton("🎲 冒险骰子", callback_data="adv_dice"),
        ],
        [
            InlineKeyboardButton("⬅ 返回主菜单", callback_data="menu_main"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def daily_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("📝 今日问题", callback_data="daily_question"),
            InlineKeyboardButton("💡 今日灵感", callback_data="daily_idea"),
        ],
        [
            InlineKeyboardButton("📋 今日待办建议", callback_data="daily_todo"),
            InlineKeyboardButton("🧘 放松小提醒", callback_data="daily_relax"),
        ],
        [
            InlineKeyboardButton("⬅ 返回主菜单", callback_data="menu_main"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


# ========== 指令处理 ==========

START_TEXT = (
    "👋 欢迎使用 *UltimateFun 娱乐工具机器人* ！\n\n"
    "这里是一个专注“轻娱乐 & 小工具”的综合机器人，你可以在这里体验：\n\n"
    "🎮 *小游戏中心*\n"
    "• 石头剪刀布、掷骰子\n"
    "• 数字猜拳、表情接龙\n\n"
    "🌈 *色彩互动区*\n"
    "• 今日幸运色、色彩心情\n"
    "• 随机色卡、色彩小建议\n\n"
    "🧠 *脑力训练站*\n"
    "• 每日脑力任务\n"
    "• 数字记忆训练、逻辑小谜题\n"
    "• 反应速度小测试\n\n"
    "✨ *娱乐工具箱*\n"
    "• 随机数字、随机表情\n"
    "• 每日签文、小决定助手\n\n"
    "⚔ *冒险任务模式*\n"
    "• 冒险任务、装备生成\n"
    "• 关卡挑战、冒险骰子\n\n"
    "📚 *每日灵感区*\n"
    "• 今日问题、灵感、待办提示\n"
    "• 放松小提醒\n\n"
    "本机器人只提供轻量娱乐内容，不涉及任何金钱、奖励、博彩或敏感信息，适合所有用户使用。\n\n"
    "👇 点击下方菜单开始体验吧！"
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text(
            START_TEXT,
            reply_markup=main_menu(),
            parse_mode="Markdown",
        )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📝 *使用说明*\n\n"
        "• 使用 /start 打开主菜单\n"
        "• 通过底部按钮进入不同功能中心\n"
        "  - 小游戏、色彩互动、脑力训练\n"
        "  - 娱乐工具、冒险任务、每日灵感\n\n"
        "本机器人仅作为娱乐和放松的小工具：\n"
        "• 不包含任何现金奖励或真实奖品\n"
        "• 不提供投资、博彩、借贷等内容\n"
        "• 不收集敏感个人信息\n\n"
        "如果你在使用中遇到问题，可以尝试重新发送 /start。"
    )
    await update.message.reply_text(text, parse_mode="Markdown")


async def about_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "ℹ️ *关于本机器人*\n\n"
        "UltimateFun 是一个集合多种轻量娱乐工具的机器人：\n"
        "• 适合碎片时间放松\n"
        "• 适合和朋友一起玩\n"
        "• 内容健康、安全、无敏感信息\n\n"
        "你可以放心在群聊或私聊中使用它。"
    )
    await update.message.reply_text(text, parse_mode="Markdown")


# ========== 按钮回调总路由 ==========

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    await query.answer()

    # --- 菜单切换 ---
    if data == "menu_main":
        await query.edit_message_text("🏠 已返回主菜单：", reply_markup=main_menu())
        return
    if data == "menu_games":
        await query.edit_message_text("🎮 小游戏中心：", reply_markup=games_menu())
        return
    if data == "menu_colors":
        await query.edit_message_text("🌈 色彩互动区：", reply_markup=colors_menu())
        return
    if data == "menu_brain":
        await query.edit_message_text("🧠 脑力训练站：", reply_markup=brain_menu())
        return
    if data == "menu_tools":
        await query.edit_message_text("✨ 娱乐工具箱：", reply_markup=tools_menu())
        return
    if data == "menu_adventure":
        await query.edit_message_text("⚔ 冒险任务模式：", reply_markup=adventure_menu())
        return
    if data == "menu_daily":
        await query.edit_message_text("📚 每日灵感区：", reply_markup=daily_menu())
        return

    # --- 小游戏中心 ---
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

    # --- 色彩互动 ---
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

    # --- 脑力训练 ---
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

    # --- 娱乐工具 ---
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

    # --- 冒险任务 ---
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

    # --- 每日灵感 ---
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

    # 兜底
    await query.edit_message_text(
        "暂不支持的操作，请发送 /start 返回主菜单。",
        reply_markup=main_menu(),
    )


# ========== 小游戏功能实现 ==========

async def game_rps(query):
    keyboard = [
        [
            InlineKeyboardButton("✊ 石头", callback_data="games_rps_rock"),
            InlineKeyboardButton("✋ 布", callback_data="games_rps_paper"),
            InlineKeyboardButton("✌ 剪刀", callback_data="games_rps_scissors"),
        ],
        [
            InlineKeyboardButton("⬅ 返回小游戏中心", callback_data="menu_games"),
        ],
    ]
    await query.edit_message_text(
        "✋ 石头剪刀布！请选择你的出拳：",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def game_rps_result(query, data: str):
    user_choice = data.split("_")[-1]
    options = ["rock", "paper", "scissors"]
    bot_choice = random.choice(options)

    emoji_map = {
        "rock": "✊ 石头",
        "paper": "✋ 布",
        "scissors": "✌ 剪刀",
    }

    if user_choice == bot_choice:
        result = "平局，我们心有灵犀～ 😆"
    elif (
        (user_choice == "rock" and bot_choice == "scissors") or
        (user_choice == "scissors" and bot_choice == "paper") or
        (user_choice == "paper" and bot_choice == "rock")
    ):
        result = "你赢啦！今天手气不错 ✨"
    else:
        result = "我赢了！要不要再来一局？😉"

    text = (
        "✋ 石头剪刀布结果：\n\n"
        f"你出：{emoji_map[user_choice]}\n"
        f"我出：{emoji_map[bot_choice]}\n\n"
        f"{result}"
    )
    await query.edit_message_text(text, reply_markup=games_menu())


async def game_dice(query):
    n = random.randint(1, 6)
    await query.edit_message_text(
        f"🎲 你掷出了：{n} 点！\n\n可再次点击“掷骰子”体验不同结果。",
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
            InlineKeyboardButton("⬅ 返回小游戏中心", callback_data="menu_games"),
        ],
    ]
    await query.edit_message_text(
        "🔢 数字猜拳：\n\n我已经在 1~5 里想好了一个数字，你来猜猜看？",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def game_number_guess_result(query, context: ContextTypes.DEFAULT_TYPE, data: str):
    secret = context.user_data.get("guess_number")
    try:
        user = int(data.split("_")[-1])
    except ValueError:
        user = None

    if secret is None or user is None:
        text = "游戏数据已失效，请重新开始一次数字猜拳。"
    elif secret == user:
        text = f"🎉 你猜对了！我想的就是 {secret}。"
    else:
        text = f"😆 差一点！我其实想的是 {secret}。"

    await query.edit_message_text(text, reply_markup=games_menu())


async def game_emoji_chain(query):
    emojis = ["😀", "😆", "😎", "🥳", "🤩", "🤗", "🙌", "✨", "🔥", "🍀", "🌈", "⭐"]
    chain = " ".join(random.sample(emojis, k=5))
    text = (
        "😊 表情接龙灵感：\n\n"
        f"{chain}\n\n"
        "可以复制这一串表情去和朋友玩接龙～"
    )
    await query.edit_message_text(text, reply_markup=games_menu())


# ========== 色彩互动功能 ==========

async def color_lucky(query):
    colors = [
        ("#FF5733", "🔥 热情橙红：今天适合主动沟通和行动。"),
        ("#33A1FF", "💧 冷静蓝：适合整理思绪、做计划。"),
        ("#28B463", "🌿 生机绿：适合休息、恢复精力。"),
        ("#AF7AC5", "🔮 梦幻紫：灵感多多，适合想新点子。"),
        ("#F7DC6F", "🌟 明亮黄：保持好心情，会更顺利。"),
    ]
    c = random.choice(colors)
    text = f"🎨 今日幸运色：{c[0]}\n\n{c[1]}"
    await query.edit_message_text(text, reply_markup=colors_menu())


async def color_mood(query):
    moods = [
        "🔵 蓝色心情：安静、理性，适合阅读或思考。",
        "🟢 绿色心情：平和、放松，适合散步或听音乐。",
        "🟡 黄色心情：活跃、开朗，适合和朋友聊天。",
        "🟣 紫色心情：神秘、有创意，适合做点小创作。",
        "🔴 红色心情：热情、有冲劲，适合开始一件新事。",
    ]
    await query.edit_message_text(
        "🔮 色彩心情提示：\n\n" + random.choice(moods),
        reply_markup=colors_menu(),
    )


async def color_palette(query):
    palette = []
    for _ in range(3):
        r, g, b = [random.randint(0, 255) for _ in range(3)]
        palette.append(f"HEX: #{r:02X}{g:02X}{b:02X}   RGB: ({r}, {g}, {b})")
    text = "🟦 随机色卡（3 组色彩）：\n\n" + "\n".join(palette)
    await query.edit_message_text(text, reply_markup=colors_menu())


async def color_tip(query):
    tips = [
        "💡 小建议：选择两种互补色做一天的头像/主题，会很有趣。",
        "💡 小建议：今天可以试试穿一件和“幸运色”接近的颜色。",
        "💡 小建议：用你喜欢的颜色写下一句话，给今天打个标签。",
    ]
    await query.edit_message_text(
        random.choice(tips),
        reply_markup=colors_menu(),
    )


# ========== 脑力训练功能 ==========

async def brain_task(query):
    tasks = [
        "🧠 任务：用 30 秒时间在心里从 50 倒数到 1。",
        "🧠 任务：回想今天让你开心的三件小事。",
        "🧠 任务：尝试记住身边看到的 5 个物品。",
        "🧠 任务：找一个安静的位置坐 1 分钟，只关注呼吸。",
    ]
    await query.edit_message_text(
        "🧠 今日脑力任务：\n\n" + random.choice(tasks),
        reply_markup=brain_menu(),
    )


async def brain_memory_start(query, context: ContextTypes.DEFAULT_TYPE):
    number = random.randint(100, 9999)
    context.user_data["brain_memory_number"] = number
    keyboard = [
        [InlineKeyboardButton("我记住了，开始回答", callback_data=f"brain_memory_answer_{number}")],
        [InlineKeyboardButton("⬅ 返回脑力训练", callback_data="menu_brain")],
    ]
    await query.edit_message_text(
        f"🔢 数字记忆训练：\n\n请记住这个数字：\n\n👉 {number}\n\n准备好后点击按钮。",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def brain_memory_answer(query, context: ContextTypes.DEFAULT_TYPE, data: str):
    original = context.user_data.get("brain_memory_number")
    try:
        answer = int(data.split("_")[-1])
    except ValueError:
        answer = None

    if original is None or answer is None:
        text = "数字记忆数据已失效，请重新开始。"
    elif original == answer:
        text = f"🎉 正确！你记住了：{original}"
    else:
        text = f"😆 有点出入！正确数字是：{original}"

    await query.edit_message_text(text, reply_markup=brain_menu())


async def brain_puzzle(query):
    puzzles = [
        "🧩 谜题：\n有一个 3 升杯和一个 5 升杯，如何量出 4 升水？",
        "🧩 谜题：\n一个人向南走 10 公里，再向东走 10 公里，再向北走 10 公里又回到原点，他在哪儿？",
        "🧩 谜题：\n三个人分 3 块大小一样的饼，如何保证每个人分到一样多？",
    ]
    await query.edit_message_text(random.choice(puzzles), reply_markup=brain_menu())


async def brain_reaction(query, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["reaction_start"] = time.time()
    keyboard = [
        [InlineKeyboardButton("⚡ 立即点击！", callback_data="brain_reaction_click")],
        [InlineKeyboardButton("⬅ 返回脑力训练", callback_data="menu_brain")],
    ]
    await query.edit_message_text(
        "🎯 看到按钮后尽快点击，测试你的反应速度：",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def brain_reaction_click(query, context: ContextTypes.DEFAULT_TYPE):
    start = context.user_data.get("reaction_start")
    if not start:
        text = "测试数据已失效，请重新开始。"
    else:
        ms = int((time.time() - start) * 1000)
        text = f"🎯 你的反应时间是：{ms} ms\n\n可以再试几次看看有没有进步！"
    await query.edit_message_text(text, reply_markup=brain_menu())


# ========== 娱乐工具功能 ==========

async def tool_random_number(query):
    n = random.randint(0, 100)
    await query.edit_message_text(
        f"🎲 随机数字（0~100）：{n}",
        reply_markup=tools_menu(),
    )


async def tool_random_emoji(query):
    emojis = ["😀", "😆", "😎", "🥳", "🤩", "🤗", "🙌", "🫶", "✨", "🔥", "🍀", "🌈", "⭐"]
    e = random.choice(emojis)
    await query.edit_message_text(
        f"😊 随机表情：{e}",
        reply_markup=tools_menu(),
    )


async def tool_today_quote(query):
    quotes = [
        "📜 今日一句：慢一点没关系，坚持下去就好。",
        "📜 今日一句：别忘了给自己一点小小的鼓励。",
        "📜 今日一句：你已经比昨天的自己更进一步了。",
        "📜 今日一句：认真生活，本身就是一种很酷的能力。",
    ]
    await query.edit_message_text(random.choice(quotes), reply_markup=tools_menu())


async def tool_decision(query):
    options = [
        "✅ 去做！别犹豫了。",
        "⏸ 可以再想一想，给自己一点时间。",
        "❌ 先放一放，看看有没有更好的选择。",
        "🔁 换个角度思考之后再决定。",
    ]
    await query.edit_message_text(
        "❓ 小决定助手：\n\n" + random.choice(options),
        reply_markup=tools_menu(),
    )


# ========== 冒险任务功能 ==========

async def adv_today(query):
    tasks = [
        "⚔ 冒险任务：整理一个你一直想整理的角落（桌面/文件夹等）。",
        "⚔ 冒险任务：联系一位很久没聊天的朋友，打个招呼。",
        "⚔ 冒险任务：完成一件你拖延了一段时间的小事。",
        "⚔ 冒险任务：给自己准备一个小小的奖励，比如喝一杯喜欢的饮料。",
    ]
    await query.edit_message_text(
        "⚔ 今日冒险任务：\n\n" + random.choice(tasks),
        reply_markup=adventure_menu(),
    )


async def adv_equipment(query):
    prefixes = ["远古的", "闪亮的", "普通的", "轻便的", "神秘的"]
    types = ["长剑", "魔杖", "斗篷", "护符", "戒指", "手套", "头盔"]
    suffixes = ["勇气", "冷静", "耐心", "灵感", "专注", "好心情"]
    item = f"{random.choice(prefixes)}{random.choice(types)}（+{random.choice(suffixes)}）"
    await query.edit_message_text(
        f"✨ 随机装备生成：\n\n👉 {item}",
        reply_markup=adventure_menu(),
    )


async def adv_stage(query):
    stages = [
        "🧱 关卡：清晨小镇\n任务：看看窗外或身边的景色，找出 3 个细节。",
        "🧱 关卡：宁静森林\n任务：深呼吸 5 次，像角色恢复体力一样。",
        "🧱 关卡：回忆之路\n任务：回想一件让你很感激的事情。",
    ]
    await query.edit_message_text(
        "🧱 当前关卡挑战：\n\n" + random.choice(stages),
        reply_markup=adventure_menu(),
    )


async def adv_dice(query):
    n = random.randint(1, 6)
    text = (
        f"🎲 冒险骰子掷出：{n} 点！\n\n"
        "你可以给每个点数设定一种小行动，比如：\n"
        "1=喝水、2=伸懒腰、3=发消息给朋友……自行发挥想象力 😄"
    )
    await query.edit_message_text(text, reply_markup=adventure_menu())


# ========== 每日灵感功能 ==========

async def daily_question(query):
    questions = [
        "📝 问题：如果今天只能完成一件事，你最想完成什么？",
        "📝 问题：最近有什么让你感到开心的小瞬间？",
        "📝 问题：你想培养一个什么样的新习惯？",
    ]
    await query.edit_message_text(
        random.choice(questions),
        reply_markup=daily_menu(),
    )


async def daily_idea(query):
    ideas = [
        "💡 灵感：记录下今天冒出来的 3 个想法，无论大小。",
        "💡 灵感：尝试用一句话形容你今天的心情，把它写下来。",
        "💡 灵感：给未来的自己写一句简短的留言。",
    ]
    await query.edit_message_text(
        random.choice(ideas),
        reply_markup=daily_menu(),
    )


async def daily_todo(query):
    todos = [
        "📋 建议待办：\n• 一件必须完成的事\n• 一件想完成的事\n• 一件让自己放松的事",
        "📋 建议待办：\n• 花 5 分钟整理一个角落\n• 回复一条未读消息\n• 留一点时间发呆",
    ]
    await query.edit_message_text(
        random.choice(todos),
        reply_markup=daily_menu(),
    )


async def daily_relax(query):
    relax = [
        "🧘 放松提示：闭上眼睛，深呼吸 5 次，只关注呼吸进出。",
        "🧘 放松提示：听一首你喜欢的音乐，不看手机，只听完它。",
        "🧘 放松提示：做 10 秒钟的伸展运动，让身体活动一下。",
    ]
    await query.edit_message_text(
        random.choice(relax),
        reply_markup=daily_menu(),
    )


# ========== 主程序入口 ==========

def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN 环境变量未设置，请在运行环境中配置。")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # 指令
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("about", about_cmd))

    # 按钮
    app.add_handler(CallbackQueryHandler(button_handler))

    logger.info("UltimateFun TG Ads 审核加强版 Bot 已启动。")
    app.run_polling()


if __name__ == "__main__":
    main()
