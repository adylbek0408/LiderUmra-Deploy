# crm/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
import logging
from .models import Client

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Client)
def notify_new_client(sender, instance, created, **kwargs):
    if created and instance.status == 'new':
        try:
            bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
            keyboard = [
                [InlineKeyboardButton(
                    "✅ Принять заявку",
                    callback_data=f"accept_{instance.id}"
                )]
            ]
            message = (
                f"📣 Новая заявка❗️❗️❗️\n"
                f"\n"
                f"👤Имя: {instance.full_name}\n"
                
                f"📞Телефон номер: {instance.phone}\n"
                f"🌍Место: {instance.country}, {instance.city}\n"
                f"📩 Пакет: {instance.package.name if instance.package else 'Не указан'}"
            )
            bot.send_message(
                chat_id=settings.TELEGRAM_GROUP_CHAT_ID,
                text=message,
                reply_markup=InlineKeyboardMarkup(keyboard)
            )  # Added missing closing parenthesis here
        except Exception as e:
            logger.error(f"Error sending Telegram notification: {e}")
        
        