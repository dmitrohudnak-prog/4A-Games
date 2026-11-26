import random

import telebot
from telebot.types import KeyboardButton, ReplyKeyboardMarkup

from config import BOT_TOKEN

bot = telebot.TeleBot(BOT_TOKEN)

ADVICE_BUTTON = "Попросити пораду в дорогу"
DIRECTION_BUTTON = "Запитати про напрямок"

GUIDE_REPLIES = [
    "Туман розвіється, варто лише зробити перший крок у невідоме. Куди прямуєш сьогодні?",
    "Цікава думка, подорожній.",
    "Зірки підказують, що відповідь ближче, ніж здається.",
    "Навіть найдовша дорога починається з одного впевненого кроку.",
]

ADVICE_REPLIES = [
    "Порада в дорогу: візьми з собою тишу. Вона підкаже більше, ніж будь-яка мапа.",
    "Не питай стежку, чи вона коротка. Питай, чи веде вона туди, де ти станеш собою.",
    "Якщо дорога роздвоюється — обери ту, що кличе, а не ту, що кричить.",
    "Утома — не ворог. Це знак сісти біля вогню й послухати власне серце.",
]

DIRECTION_REPLIES = [
    "Напрямок ближче за горизонт: іди туди, де твоє питання стає тихішим.",
    "Північ кличе тих, хто шукає ясність. Південь — тих, хто шукає тепло. Обидва шляхи правдиві, якщо йдеш усвідомлено.",
    "Зірки не вказують одну стежку. Вони лише нагадують: ти вже стоїш на початку.",
    "Якщо не знаєш, куди йти — зроби крок у бік світла, яке ще не згасло.",
]

MOOD_REPLIES = {
    "сум": "Сум — теж частина дороги. Пройди його повільно, і він стане тихішим.",
    "радіс": "Радість, яку ти несеш, освітлює стежку краще за будь-який ліхтар.",
    "щаст": "Щастя не чекає наприкінці шляху. Воно вже йде поруч, якщо ти його помічаєш.",
    "страх": "Страх — лише туман перед першим кроком. Назви його, і він втратить силу.",
    "бою": "Те, чого боїшся, меншає, коли дивишся на нього спокійно.",
    "втом": "Втома каже: сядь біля вогню. Дорога нікуди не зникне.",
    "злість": "Злість — гарячий вітер. Дай йому пройти, не йди за ним.",
    "гнів": "Гнів засліплює компас. Зачекай, поки вода в душі знову стане прозорою.",
    "тривог": "Тривога малює тіні попереду. Більшість із них зникає, коли підходиш ближче.",
    "самот": "Самотність — не порожнеча. Це тиша, в якій чути власний крок.",
}

START_TEXT = (
    "Вітаю тебе, мандрівнику.\n\n"
    "Я — Мудрий провідник. Туман доріг мені знайомий, і я завжди поруч: "
    "поділись будь-якою думкою, і я відповім спокійно, без поспіху.\n\n"
    "Якщо шлях ще не обрано — попроси пораду в дорогу або запитай про напрямок."
)


def guide_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton(ADVICE_BUTTON))
    markup.add(KeyboardButton(DIRECTION_BUTTON))
    return markup


def send_guide_reply(chat_id, replies):
    bot.send_message(chat_id, random.choice(replies), reply_markup=guide_menu())


def command_name(text):
    if not text.startswith("/"):
        return ""
    return text.split()[0].split("@")[0].lower()


def mood_reply(text):
    lowered = text.lower()
    for mood, reply in MOOD_REPLIES.items():
        if mood in lowered:
            return reply
    return None


@bot.message_handler(content_types=["text"])
def handle_text(message):
    text = (message.text or "").strip()
    lowered = text.lower()

    if command_name(lowered) == "/start":
        bot.send_message(message.chat.id, START_TEXT, reply_markup=guide_menu())
        return

    if lowered == ADVICE_BUTTON.lower():
        send_guide_reply(message.chat.id, ADVICE_REPLIES)
        return

    if lowered == DIRECTION_BUTTON.lower():
        send_guide_reply(message.chat.id, DIRECTION_REPLIES)
        return

    reply = mood_reply(lowered)
    if reply:
        bot.send_message(message.chat.id, reply, reply_markup=guide_menu())
        return

    bot.send_message(message.chat.id, random.choice(GUIDE_REPLIES), reply_markup=guide_menu())


if __name__ == "__main__":
    print("Бот успішно запущений і слухає повідомлення...")
    bot.polling(skip_pending=True)
