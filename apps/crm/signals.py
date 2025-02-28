# apps/crm/signals.py
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
                logger.error("Client %d has no package assigned", instance.id)
                return

            branch = instance.package.place
            chat_id = settings.TELEGRAM_GROUP_IDS.get(branch)
            
            if not chat_id:
                logger.error("No group chat for branch %s", branch)
                return

            message = (
                f"📣 Новая заявка ({branch})❗️\n"
                f"👤 Имя: {instance.full_name}\n"
                f"📞 Телефон: {instance.phone}\n"
                f"🌍 Место: {instance.country}, {instance.city}\n"
                f"📦 Пакет: {instance.package.name or 'Не указан'}"
            )

            keyboard = [[
                InlineKeyboardButton(
                    "✅ Принять заявку",
                    callback_data=f"accept_{instance.id}"
                )
            ]]

            sent_message = bot.send_message(
                chat_id=chat_id,
                text=message,
                reply_markup=InlineKeyboardMarkup(keyboard),
                timeout=30
            )

            instance.notification_chat_id = chat_id
            instance.notification_message_id = sent_message.message_id
            instance.save(update_fields=['notification_chat_id', 'notification_message_id'])

        except Exception as e:
            logger.exception("Critical error: %s", str(e))
    