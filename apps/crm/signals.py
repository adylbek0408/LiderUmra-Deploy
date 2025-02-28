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
                logger.warning("Client %d has no package", instance.id)
                return
                
            branch = instance.package.place
            managers = Manager.objects.filter(branch=branch)

            if not managers.exists():
                logger.error("No managers for branch: %s", branch)
                return

            keyboard = [[
                InlineKeyboardButton(
                    "✅ Принять заявку",
                    callback_data=f"accept_{instance.id}"
                )
            ]]
            
            message = (
                f"📣 Новая заявка ({branch})❗️\n"
                f"👤 Имя: {instance.full_name}\n"
                f"📞 Телефон: {instance.phone}\n"
                f"🌍 Место: {instance.country}, {instance.city}\n"
                f"📦 Пакет: {instance.package.name or 'Не указан'}"
            )

            for manager in managers:
                try:
                    # Check chat first
                    bot.get_chat(chat_id=manager.telegram_id)
                    
                    # Send message with 30s timeout
                    bot.send_message(
                        chat_id=manager.telegram_id,
                        text=message,
                        reply_markup=InlineKeyboardMarkup(keyboard),
                        read_timeout=30,
                        write_timeout=30,
                        connect_timeout=30
                    )
                except telegram.error.Unauthorized:
                    logger.error("Manager %s blocked the bot", manager.telegram_id)
                except telegram.error.TimedOut:
                    logger.warning("Timeout sending to manager %s", manager.telegram_id)
                except Exception as e:
                    logger.error("Failed to notify manager %s: %s", manager.telegram_id, str(e))

        except Exception as e:
            logger.exception("Critical error in notification system: %s", str(e))
    