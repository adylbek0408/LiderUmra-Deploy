import logging
from django.core.management.base import BaseCommand
from telegram.ext import Updater, CallbackQueryHandler
from django.conf import settings
from django.db import transaction
from ...models import Client, Manager

logger = logging.getLogger(__name__)

def handle_accept(update, context):
    query = update.callback_query
    query.answer()

    try:
        client_id = int(query.data.split('_')[1])
    except (IndexError, ValueError):
        logger.error("Invalid callback data: %s", query.data)
        return

    try:
        with transaction.atomic():
            client = Client.objects.select_related('package').get(id=client_id)
            manager = Manager.objects.get(telegram_id=str(query.from_user.id))

            if client.status != 'new':
                query.edit_message_text("⚠️ Заявка уже принята другим менеджером!")
                return

            # Update the client status and assign the manager
            client.status = 'processing'
            client.manager = manager
            client.save(update_fields=['status', 'manager', 'updated_at'])

            # Prepare the updated message text
            manager_name = manager.get_display_name()
            accept_text = (
                f"✅ Принято менеджером: {manager_name}\n"
                f"⏱ Время принятия: {client.updated_at.astimezone().strftime('%Y-%m-%d %H:%M')}"
            )
            original_message_text = (
                f"📣 Новая заявка ({client.package.place})❗️\n"
                f"👤 Имя: {client.full_name}\n"
                f"📞 Телефон: {client.phone}\n"
                f"🌍 Место: {client.country}, {client.city}\n"
                f"📦 Пакет: {client.package.name or 'Не указан'}"
            )
            new_text = f"{accept_text}\n\n{original_message_text}"

            # Edit the group message to remove the button and show acceptance info
            if client.notification_message_id:
                context.bot.edit_message_text(
                    chat_id=settings.TELEGRAM_GROUP_CHAT_ID,
                    message_id=client.notification_message_id,
                    text=new_text,
                    reply_markup=None
                )

            # Notify the manager privately (optional)
            context.bot.send_message(
                chat_id=manager.telegram_id,
                text=f"Вы приняли заявку:\n{client.full_name}\n{client.phone}"
            )

    except Client.DoesNotExist:
        logger.error("Client not found: %d", client_id)
        query.edit_message_text("❌ Заявка не найдена!")
    except Manager.DoesNotExist:
        logger.error("Manager not found: %s", query.from_user.id)
        query.edit_message_text("❌ Вы не зарегистрированы как менеджер!")
    except Exception as e:
        logger.exception("Critical error in handle_accept: %s", str(e))
        query.edit_message_text("❗ Ошибка, попробуйте позже")



class Command(BaseCommand):
    help = 'Run Telegram bot'

    def handle(self, *args, **options):
        updater = Updater(settings.TELEGRAM_BOT_TOKEN, use_context=True)
        updater.dispatcher.add_handler(CallbackQueryHandler(handle_accept, pattern='^accept_'))
        updater.dispatcher.add_error_handler(self.error_handler)
        self.stdout.write("✅ Бот успешно запущен")
        updater.start_polling()
        updater.idle()

    def error_handler(self, update, context):
        logger.error('Update "%s" caused error: %s', update, context.error)
    