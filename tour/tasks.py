from celery import shared_task
import telebot

TOKEN = "8492141161:AAFdBFuDuELinq1rziIdn4GsSJ3KuwuLABw"
ADMIN_ID = 1222901932
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

@shared_task
def send_telegram_booking_notification(booking_id):
    from .models import TourBooking

    try:
        b = TourBooking.objects.get(id=booking_id)
    except TourBooking.DoesNotExist:
        return

    if b.is_paid:
        total_price = b.tour.price * b.number_of_people
        text = (
            f"🆕 <b>رزرو جدید پرداخت شد!</b>\n\n"
            f"👤 نام: {b.full_name}\n\n"
            f"📞 تلفن: {b.phone_number}\n\n"
            f"📅 تاریخ: {b.tour_date.start_date}\n\n"
            f"⏰ ساعت: {b.tour_time.time}\n\n"
            f"👥 تعداد: {b.number_of_people}\n\n"
            f"💰 مبلغ کل: {total_price}\n\n"
            f"🏷️ تور: {b.tour.title}\n\n"
            "────────────────────────"
        )
        try:
            bot.send_message(ADMIN_ID, text)
        except Exception as e:
            print("خطا در ارسال پیام تلگرام:", e)
