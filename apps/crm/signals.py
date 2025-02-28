# crm/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
import logging
from .models import Client, Manager

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Client)
def notify_new_client(sender, instance, created, **kwargs):
    logger.info(f"Signal triggered for Client {instance.id}, created: {created}, status: {instance.status}")
    
    if created and instance.status == 'new':
        logger.info("New client created and status is 'new'")
        try:
            bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
            logger.info("Bot instance created successfully")
            
            # Check if the client has a package and branch
            if not instance.package:
                logger.error("Client has no package assigned.")
                return
            branch = instance.package.place
            logger.info(f"Client branch: {branch}")
            
            # Find managers in the same branch
            managers = Manager.objects.filter(branch=branch)
            if not managers:
                logger.error(f"No managers found for branch: {branch}")
                return
            logger.info(f"Managers found: {managers.count()}")
            
            # Prepare message and button
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
                f"📦 Пакет: {instance.package.name if instance.package else 'Не указан'}"
            )
            
            # Send notification to each manager in the branch
            for manager in managers:
                try:
                    bot.send_message(
                        chat_id=manager.telegram_id,
                        text=message,
                        reply_markup=InlineKeyboardMarkup(keyboard)
                    )
                    logger.info(f"Notification sent to manager {manager.telegram_id}")
                except Exception as e:
                    logger.error(f"Failed to notify manager {manager}: {e}")
            
        except Exception as e:
            logger.error(f"Error sending notifications: {e}")
