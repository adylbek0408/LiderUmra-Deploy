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

            # Prepare the message
            message = (
                f"📣 Новая заявка ({instance.package.place})❗️\n"
                f"👤 Имя: {instance.full_name}\n"
                f"📞 Телефон: {instance.phone}\n"
                f"🌍 Место: {instance.country}, {instance.city}\n"
                f"📦 Пакет: {instance.package.name or 'Не указан'}"
            )

            # Prepare the inline keyboard
            keyboard = [[
                InlineKeyboardButton(
                    "✅ Принять заявку",
                    callback_data=f"accept_{instance.id}"
                )
            ]]

            # Send the message to the group
            sent_message = bot.send_message(
                chat_id=settings.TELEGRAM_GROUP_CHAT_ID,
                text=message,
                reply_markup=InlineKeyboardMarkup(keyboard),
                timeout=30
            )

            # Save the message ID to the client (optional, if you want to track it)
            instance.notification_message_id = sent_message.message_id
            instance.save(update_fields=['notification_message_id'])

        except Exception as e:
            logger.exception("Critical error in notification system: %s", str(e))
