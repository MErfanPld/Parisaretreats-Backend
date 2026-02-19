from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import TourBooking
import telebot

TOKEN = "8492141161:AAFdBFuDuELinq1rziIdn4GsSJ3KuwuLABw"
ADMIN_ID = 1222901932
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

@receiver(pre_save, sender=TourBooking)
def notify_paid_booking(sender, instance, **kwargs):
    """
    وقتی رزرو جدید پرداخت شد، اطلاع بده
    """
    if not instance.pk:
        paid_now = instance.is_paid
    else:
        old_instance = TourBooking.objects.get(pk=instance.pk)
        paid_now = not old_instance.is_paid and instance.is_paid

    if paid_now:
        total_price = instance.tour.price * instance.number_of_people
        text = (
            f"🆕 <b>رزرو جدید پرداخت شد!</b>\n\n"
            f"👤 <b>نام:</b> {instance.full_name}\n\n"
            f"📞 <b>تلفن:</b> {instance.phone_number}\n\n"
            f"📅 <b>تاریخ:</b> {instance.tour_date.start_date}\n\n"
            f"⏰ <b>ساعت:</b> {instance.tour_time.time}\n\n"
            f"👥 <b>تعداد افراد:</b> {instance.number_of_people}\n\n"
            f"💰 <b>مبلغ کل:</b> {total_price}\n\n"
            f"🏷️ <b>تور:</b> {instance.tour.title}\n\n"
            "────────────────────────"
        )
        try:
            bot.send_message(ADMIN_ID, text)
        except Exception as e:
            print("ارسال پیام خودکار با خطا مواجه شد:", e)
