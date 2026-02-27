import json
import os
import django
from django.conf import settings
import telebot
import requests
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from tour.models import Tour  # برای لیست تورها

TOKEN = "8492141161:AAFdBFuDuELinq1rziIdn4GsSJ3KuwuLABw"
ADMIN_ID = 1222901932
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

API_URL = "http://127.0.0.1/tour/api/paid_bookings/"


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

    try:
        response = requests.get(API_URL, params={"tour_id": tour_id})
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

    # اگر تور خاصی انتخاب شده فیلتر کن
    if tour_id:
        bookings = [b for b in bookings if str(b["tour_id"]) == str(tour_id)]

    if not bookings:
        bot.reply_to(message, "رزروی برای این تور وجود ندارد ❌")
        return

    for b in bookings:

        text = (
            f"📋 <b>رزرو جدید</b>\n\n"
            f"👤 نام: {b['full_name']}\n"
            f"📞 تلفن: {b['phone_number']}\n"
            f"📅 تاریخ: {b['tour_date']}\n"
            f"⏰ ساعت: {b['tour_time']}\n"
            f"👥 تعداد: {b['number_of_people']}\n"
            f"💰 مبلغ کل: {b['total_price']}\n"
            f"🏷️ تور: {b['tour_title']}\n"
        )
        from urllib.parse import urlparse

        receipt_url = b.get("payment_receipt")

        if receipt_url:
            try:
                # اگر URL کامل بود (http://...)
                if receipt_url.startswith("http"):
                    parsed_url = urlparse(receipt_url)
                    clean_path = parsed_url.path  # /media/receipts/xxx.png
                else:
                    clean_path = receipt_url

                # حذف /media/ از اول مسیر
                clean_path = clean_path.replace("/media/", "")

                file_path = os.path.join(settings.MEDIA_ROOT, clean_path)

                with open(file_path, "rb") as photo:
                    bot.send_photo(
                        message.chat.id,
                        photo=photo,
                        caption=text
                    )

            except Exception as e:
                bot.send_message(
                    message.chat.id,
                    text + f"\n\n⚠️ خطا در ارسال تصویر: {e}"
                )
        else:
            bot.send_message(message.chat.id, text)


# ----------------- RUN BOT -----------------
if __name__ == "__main__":
    print("🤖 Bot is running...")
    bot.infinity_polling(skip_pending=True)
