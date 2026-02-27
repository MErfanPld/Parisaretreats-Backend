import os
import django
from django.conf import settings
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# ----------------- Django Setup -----------------
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from tour.models import Tour, Booking  # مدل‌ها

# ----------------- Bot Config -----------------
TOKEN = "8492141161:AAFdBFuDuELinq1rziIdn4GsSJ3KuwuLABw"
ADMIN_ID = 1222901932
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# ----------------- START -----------------
@bot.message_handler(commands=['start'])
def start_message(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton("📋 مشاهده رزروها")
    markup.add(btn1)
    bot.send_message(
        message.chat.id,
        "سلام 👋\nبه پنل مدیریت رزرو خوش آمدید.",
        reply_markup=markup
    )

# ----------------- BUTTON HANDLER -----------------
@bot.message_handler(func=lambda message: message.text == "📋 مشاهده رزروها")
def handle_button(message):
    # اگر بخوای دسترسی محدود باشه uncomment کن
    # if message.from_user.id != ADMIN_ID:
    #     bot.reply_to(message, "شما دسترسی ندارید ❌")
    #     return

    tours = Tour.objects.all()
    if not tours.exists():
        bot.send_message(message.chat.id, "تور موجود نیست ❌")
        return

    markup = InlineKeyboardMarkup()
    for t in tours:
        markup.add(InlineKeyboardButton(t.title, callback_data=f"tour_{t.id}"))

    bot.send_message(message.chat.id, "یک تور را انتخاب کنید:", reply_markup=markup)

# ----------------- CALLBACK HANDLER -----------------
@bot.callback_query_handler(func=lambda call: call.data.startswith("tour_"))
def handle_tour_selection(call):
    tour_id = call.data.split("_")[1]
    show_bookings(call.message, tour_id=tour_id)

# ----------------- SHOW BOOKINGS -----------------
def show_bookings(message, tour_id=None):
    bookings = Booking.objects.filter(payment_status="paid")
    if tour_id:
        bookings = bookings.filter(tour_id=tour_id)

    if not bookings.exists():
        bot.reply_to(message, "رزروی پرداخت شده وجود ندارد ❌")
        return

    for b in bookings:
        text = (
            f"📋 <b>رزرو جدید</b>\n\n"
            f"👤 نام: {b.full_name}\n"
            f"📞 تلفن: {b.phone_number}\n"
            f"📅 تاریخ: {b.tour_date}\n"
            f"⏰ ساعت: {b.tour_time}\n"
            f"👥 تعداد: {b.number_of_people}\n"
            f"💰 مبلغ کل: {b.total_price}\n"
            f"🏷️ تور: {b.tour.title}\n"
        )

        # ارسال رسید اگر موجود باشد
        if b.payment_receipt:
            try:
                with open(b.payment_receipt.path, "rb") as photo:
                    bot.send_photo(message.chat.id, photo=photo, caption=text)
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
