import json
import os
import django
import telebot
import requests
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from tour.models import Tour  # برای لیست تورها

TOKEN = "8492141161:AAFdBFuDuELinq1rziIdn4GsSJ3KuwuLABw"
ADMIN_ID = 1222901932
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

API_URL = "http://127.0.0.1:8000/tour/api/paid_bookings/"

# ----------------- START -----------------
@bot.message_handler(commands=['start'])
def start_message(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton("📋 مشاهده رزروها")
    markup.add(btn1)
    bot.send_message(message.chat.id, "سلام 👋\nبه پنل مدیریت رزرو خوش آمدید.", reply_markup=markup)

# ----------------- BUTTON HANDLER -----------------
@bot.message_handler(func=lambda message: message.text == "📋 مشاهده رزروها")
def handle_button(message):
    # if message.from_user.id != ADMIN_ID:
    #     bot.reply_to(message, "شما دسترسی ندارید ❌")
    #     return

    # لیست تورها رو بگیر
    tours = Tour.objects.all()
    markup = InlineKeyboardMarkup()
    for t in tours:
        # callback_data = id تور
        markup.add(InlineKeyboardButton(t.title, callback_data=f"tour_{t.id}"))

    bot.send_message(message.chat.id, "یک تور را انتخاب کنید:", reply_markup=markup)

# ----------------- CALLBACK HANDLER -----------------
@bot.callback_query_handler(func=lambda call: call.data.startswith("tour_"))
def handle_tour_selection(call):
    tour_id = call.data.split("_")[1]
    show_bookings(call.message, tour_id=tour_id)

# ----------------- SHOW BOOKINGS -----------------
def show_bookings(message, tour_id=None):
    # if message.from_user.id != ADMIN_ID:
    #     bot.reply_to(message, "شما دسترسی ندارید ❌")
    #     return

    # درخواست API
    try:
        response = requests.get(API_URL)
        data = response.json()
        if isinstance(data, str):
            bookings = json.loads(data)
        elif isinstance(data, dict) and 'results' in data:
            bookings = data['results']
        else:
            bookings = data
    except Exception as e:
        bot.reply_to(message, f"خطا در دریافت اطلاعات رزروها:\n{e}")
        return

    if not bookings:
        bot.reply_to(message, "رزروی پرداخت شده وجود ندارد ❌")
        return


    if not bookings:
        bot.reply_to(message, "رزروی پرداخت شده برای این تور وجود ندارد ❌")
        return

    text = "📋 <b>لیست رزروهای پرداخت شده:</b>\n\n"
    for b in bookings:
        text += (
            f"👤 نام: {b['full_name']}\n\n"
            f"📞 تلفن: {b['phone_number']}\n\n"
            f"📅 تاریخ: {b['tour_date']}\n\n"
            f"⏰ ساعت: {b['tour_time']}\n\n"
            f"👥 تعداد: {b['number_of_people']}\n\n"
            f"💰 مبلغ کل: {b['total_price']}\n\n"
            f"🏷️ تور: {b['tour']}\n\n"
            "────────────────────────\n\n"
        )

    bot.send_message(message.chat.id, text)

# ----------------- RUN BOT -----------------
if __name__ == "__main__":
    print("🤖 Bot is running...")
    bot.infinity_polling(skip_pending=True)
