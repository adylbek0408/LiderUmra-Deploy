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
    logger.info(f"Signal triggered for Client {instance.id}. Created: {created}, Status: {instance.status}")
    
    if created and instance.status == 'new':
        logger.info("New client detected. Starting notification process...")
        try:
            logger.info("Initializing Telegram bot")
            bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
            
            if not instance.package:
                logger.error("Client %d has no package assigned", instance.id)
                return
                
            branch = instance.package.place
            logger.info("Branch: %s", branch)
            
            managers = Manager.objects.filter(branch=branch)
            logger.info("Managers found: %d", managers.count())
            
            if not managers.exists():
                logger.error("No managers in branch %s", branch)
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
                    logger.info("Notifying manager %s", manager.telegram_id)
                    bot.send_message(
                        chat_id=manager.telegram_id,
                        text=message,
                        reply_markup=InlineKeyboardMarkup(keyboard),
                        timeout=30
                    )
                    logger.info("Notification sent to %s", manager.telegram_id)
                except telegram.error.Unauthorized:
                    logger.error("Manager %s blocked the bot", manager.telegram_id)
                except Exception as e:
                    logger.error("Failed to notify %s: %s", manager.telegram_id, str(e))

        except Exception as e:
            logger.exception("Critical error in notification system: %s", str(e))
            