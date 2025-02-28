# crm/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
import telegram
import logging
from .models import Client, Manager

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Client)
def notify_new_client(sender, instance, created, **kwargs):
    if created and instance.status == 'new':
        try:
            bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
            
            if not instance.package:
                return
                
            branch = instance.package.place
            managers = Manager.objects.filter(branch=branch)

            keyboard = [[InlineKeyboardButton("✅ Принять заявку", callback_data=f"accept_{instance.id}")]]
            message = (
                f"📣 Новая заявка ({branch})❗️\n"
                f"👤 Имя: {instance.full_name}\n"
                f"📞 Телефон: {instance.phone}\n"
                f"🌍 Место: {instance.country}, {instance.city}\n"
                f"📦 Пакет: {instance.package.name or 'Не указан'}"
            )

            for manager in managers:
                try:
                    # Verify chat is possible
                    bot.get_chat(chat_id=manager.telegram_id)
                    bot.send_message(
                        chat_id=manager.telegram_id,
                        text=message,
                        reply_markup=InlineKeyboardMarkup(keyboard)
                    )
                except telegram.error.Unauthorized:
                    logger.error(f"Manager {manager} hasn't started chat with bot")
                except Exception as e:
                    logger.error(f"Error messaging manager {manager}: {str(e)}")

        except Exception as e:
            logger.error(f"Notification system error: {str(e)}")
