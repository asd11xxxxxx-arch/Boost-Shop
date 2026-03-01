import telebot
from telebot import types
import random

# ================= CONFIG =================
TOKEN = "8547877777:AAGmQN8gGru3LauuoYS-ULPaSut1W175DdU"
CHANNEL_ID = -1003793281342
ADMIN_ID = 8528450237

bot = telebot.TeleBot(TOKEN)

# ================= MEMORY =================
users = set()
waiting_payment = {}
waiting_info = {} 
broadcast_mode = set()
user_selected_platform = {}

# ================= START =================
@bot.message_handler(commands=['start'])
def start(message):
    users.add(message.from_user.id)
    if message.from_user.id in waiting_info: del waiting_info[message.from_user.id]
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("\U0001F4E6 ဝယ်ယူရန်"))
    markup.add(types.KeyboardButton("\U0001F4DE ဆက်သွယ်ရန်"), types.KeyboardButton("\U00002B50 လမ်းညွှန်"))
    
    if message.from_user.id == ADMIN_ID:
        markup.add(types.KeyboardButton("\U00002699 Admin Panel"))

    welcome_text = (
        "<b>Boost Seller</b> မှ ကြိုဆိုလိုက် ပါတယ်ခင်ဗျ။\n\n"
        "\U0000231B ဆိုင်ဖွင့်ချိန်သည် <b>မနက် 9 နာရီမှ ည 10 နာရီ</b> ထိသာဖြစ်သည်\n\n"
        "တခုခုဆို သိရဖို့ @tiktok_boost_shop Join ထားဖို့ မမေ့နဲ့နော်"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode="HTML", reply_markup=markup)

# ================= CONTACT & GUIDE =================
@bot.message_handler(func=lambda m: m.text == "\U0001F4DE ဆက်သွယ်ရန်")
def contact_admin(message):
    bot.send_message(message.chat.id, "လူကြီးမင်းတို့၏ အခက်အခဲများအတွက် @RAW1112 သို့ တိုက်ရိုက်ဆက်သွယ်မေးမြန်းနိုင်ပါသည်။")

@bot.message_handler(func=lambda m: m.text == "\U00002B50 လမ်းညွှန်")
def guide_text(message):
    text = (
        "<b>လမ်းညွှန်ချက်များ</b>\n\n"
        "\U0001F517 ကိုယ်တိုးချင်တဲ့ Posts/Video/Channel/ လင့်ကို ပို့ပေးပါ။\n\n"
        "\U0001F4E2 TG Sub တိုးလျှင် Invite Link ပို့ပေးပါ။\n"
        "\U0001F4B5 ဝယ်ယူမဲ့ ပမာဏ နဲ့ လွဲရမဲ့ငွေ ကိုသေချာပို့ပေးပါ။"
    )
    bot.send_message(message.chat.id, text, parse_mode="HTML")

# ================= ORDER MENU =================
@bot.message_handler(func=lambda m: m.text == "\U0001F4E6 ဝယ်ယူရန်")
def select_platform(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("TikTok", "Telegram", "Facebook")
    markup.add("\U00002B05 Back")
    bot.send_message(message.chat.id, "<b>ဝယ်ယူလိုသည့် Platform ကို ရွေးချယ်ပေးပါ-</b>", parse_mode="HTML", reply_markup=markup)

# ================= SUB-MENUS =================
@bot.message_handler(func=lambda m: m.text in ["TikTok", "Facebook"])
def tiktok_fb_menu(message):
    platform = message.text
    user_selected_platform[message.from_user.id] = platform
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("\U0001F441 Views", "\U0001F464 Follower", "\U00002764 Like")
    markup.add("\U00002B05 Back")
    bot.send_message(message.chat.id, f"<b>{platform} အတွက် ဝန်ဆောင်မှု ရွေးချယ်ပါ-</b>", parse_mode="HTML", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "Telegram")
def telegram_menu(message):
    user_selected_platform[message.from_user.id] = "Telegram"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("\U0001F441 Views", "\U0001F465 Subs", "\U0001F31F REC")
    markup.add("\U00002B05 Back")
    bot.send_message(message.chat.id, "<b>Telegram အတွက် ဝန်ဆောင်မှု ရွေးချယ်ပါ-</b>", parse_mode="HTML", reply_markup=markup)

# ================= INFO REQUEST =================
@bot.message_handler(func=lambda m: any(word in m.text for word in ["Views", "Follower", "Like", "Subs", "REC"]))
def ask_info(message):
    service = message.text
    platform = user_selected_platform.get(message.from_user.id, "Unknown")
    price_text = ""
    
    if platform == "TikTok":
        if "Views" in service: price_text = "View 1K လျှင် 500 Ks သာကျမည်"
        elif "Follower" in service: price_text = "Follower 100 သာလျှင် 1500 Ks သာကျမည်"
        elif "Like" in service: price_text = "Like 500 သာလျှင် 1500 Ks သာကျမည်"
    elif platform == "Facebook":
        if "Views" in service: price_text = "Views 1K သာလျှင် 1000 Ks သာကျမည်"
        elif "Follower" in service: price_text = "Follower 1k သာ လျှင် 2500 Ks သာကျမည်"
        elif "Like" in service: price_text = "Like 1K သာလျှင် 2500 Ks သာကျမည်"
    elif platform == "Telegram":
        if "Views" in service: price_text = "View 1k လျှင် 500 Ks သာကျမည်"
        elif "Subs" in service: price_text = "Subs 1K သာလျှင် 3000 Ks သာကျမည်"
        elif "REC" in service: price_text = "Rec 1k သာ လျှင် 300 Ks သာကျမည်"

    text = (
        f"<b>{platform} - {service}</b>\n"
        f"\U0001F4B0 {price_text}\n\n"
        "<b>ဝယ်ယူလိုတဲ့ ပမာဏ ကို အရင်ပို့ပြီး Link ကို အောက်ကပို့ပေးပါ။</b>\n\n"
        "<i>နမူနာပုံစံ -</i>\n"
        "<code>500\nhttps://...</code>"
    )
    waiting_info[message.from_user.id] = {"service": service, "platform": platform}
    bot.send_message(message.chat.id, text, parse_mode="HTML")

# ================= PAYMENT INFO =================
@bot.message_handler(func=lambda m: m.from_user.id in waiting_info)
def show_payment(message):
    if "Back" in message.text:
        del waiting_info[message.from_user.id]
        return select_platform(message)

    info = waiting_info[message.from_user.id]
    raw_text = message.text
    del waiting_info[message.from_user.id]

    lines = raw_text.split('\n')
    qty = lines[0].strip() if len(lines) > 0 else "မသိရ"
    link = lines[1].strip() if len(lines) > 1 else "Link မပါရှိပါ"

    order_id = random.randint(1000, 9999)
    waiting_payment[message.from_user.id] = {
        "service": info["service"], 
        "platform": info["platform"],
        "qty": qty, 
        "link": link, 
        "id": order_id
    }

    payment_text = (
        f"<b>{info['platform']} - {info['service']}</b>\n"
        f"<b>ပမာဏ - {qty}</b>\n"
        f"<b>Link - {link}</b>\n\n"
        "<u>ငွေလွဲရမည့် ဖုန်းနံပါတ် (နှိပ်ပြီး Copy ကူးပါ)</u>\n"
        "ငွေလွဲပြီး Ss ကို ပို့ပေးပါ\n\n"
        f"Wave - <code>09752477315</code>\n"
        f"K Pay - <code>09450109718</code>\n\n"
        "မှတ်ချက် မှာ <b>RAW</b> လို့ရေးပေးပါ။\n\n"
        f"Order ID: <code>#{order_id}</code>"
    )
    bot.send_message(message.chat.id, payment_text, parse_mode="HTML")

# ================= RECEIVE PHOTO =================
@bot.message_handler(content_types=['photo'])
def payment_photo(message):
    user_id = message.from_user.id
    if user_id not in waiting_payment: return
    order = waiting_payment[user_id]
    del waiting_payment[user_id]
    caption = (
        f"\U0001F4E9 <b>NEW ORDER #{order['id']}</b>\n\n"
        f"<b>Platform:</b> {order['platform']}\n"
        f"<b>Service:</b> {order['service']}\n"
        f"<b>ပမာဏ:</b> {order['qty']}\n"
        f"<b>လင့်:</b> {order['link']}\n"
        f"\U0001F464 User: {message.from_user.first_name}\n"
        f"\U0001F194 ID: <code>{user_id}</code>\n\n"
        "Status: Pending"
    )
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("\U00002705 Accept", callback_data=f"accept_{order['id']}_{user_id}"),
        types.InlineKeyboardButton("\U0000274C Cancel", callback_data=f"cancel_{order['id']}_{user_id}")
    )
    bot.send_photo(CHANNEL_ID, message.photo[-1].file_id, caption=caption, parse_mode="HTML", reply_markup=markup)
    bot.send_message(user_id, "\U00002705 Order & Payment received! စစ်ဆေးပြီးပါက အကြောင်းကြားပေးပါမည်။")

# ================= ADMIN HANDLERS =================
@bot.message_handler(func=lambda m: m.text == "\U00002699 Admin Panel")
def admin_panel(message):
    if message.from_user.id == ADMIN_ID:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("\U0001F4E2 Broadcast", "\U0001F4CA Stats")
        markup.add("\U00002B05 Back")
        bot.send_message(message.chat.id, "<b>⚙️ Admin Panel</b>", parse_mode="HTML", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "\U0001F4CA Stats")
def show_stats(message):
    if message.from_user.id == ADMIN_ID:
        bot.send_message(message.chat.id, f"စုစုပေါင်းအသုံးပြုသူ: {len(users)} ယောက်")

@bot.message_handler(func=lambda m: m.text == "\U0001F4E2 Broadcast")
def broadcast_req(message):
    if message.from_user.id == ADMIN_ID:
        broadcast_mode.add(message.from_user.id)
        bot.send_message(message.chat.id, "📢 ပို့လိုသည့် စာသားကို ရိုက်ထည့်ပါ။")

@bot.message_handler(func=lambda m: m.from_user.id in broadcast_mode)
def do_broadcast(message):
    broadcast_mode.remove(message.from_user.id)
    count = 0
    for uid in users:
        try:
            bot.send_message(uid, message.text)
            count += 1
        except: pass
    bot.send_message(message.chat.id, f"✅ ပို့ဆောင်ပြီးစီး ({count} ဦး)")

@bot.message_handler(func=lambda m: m.text in ["\U00002B05 Back", "Back"])
def back_to_start(message): start(message)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    data = call.data.split("_")
    action, order_id, user_id = data[0], data[1], int(data[2])
    if action == "accept":
        bot.edit_message_caption(f"{call.message.caption}\n\n\U00002705 <b>ACCEPTED</b>", call.message.chat.id, call.message.message_id, parse_mode="HTML")
        bot.send_message(user_id, f"\U00002705 သင်၏ Order #{order_id} ကို လက်ခံပြီးပါပြီ။")
    elif action == "cancel":
        bot.edit_message_caption(f"{call.message.caption}\n\n\U0000274C <b>CANCELED</b>", call.message.chat.id, call.message.message_id, parse_mode="HTML")
        bot.send_message(user_id, f"\U0000274C သင်၏ Order #{order_id} ကို ပယ်ဖျက်လိုက်ပါသည်။")

print("Bot Is Online...")
bot.infinity_polling()

