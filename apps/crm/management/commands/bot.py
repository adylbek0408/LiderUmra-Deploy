# apps/crm/management/commands/bot.py
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
    except (IndexError, ValueError) as e:
        logger.error("Invalid callback data: %s | Error: %s", query.data, str(e))
        return

    try:
        with transaction.atomic():
            client = Client.objects.select_related('package').get(id=client_id)
            manager = Manager.objects.get(telegram_id=str(query.from_user.id))

            if client.status != 'new':
                logger.warning("Client %d already processed. Status: %s", client_id, client.status)
                query.edit_message_text("⚠️ Заявка уже принята другим менеджером!")
                return

            if manager.branch != client.package.place:
                logger.error("Branch mismatch: Manager %s vs Client %s", manager.branch, client.package.place)
                query.edit_message_text("❌ Эта заявка не для вашего филиала!")
                return

            client.status = 'processing'
            client.manager = manager
            client.save(update_fields=['status', 'manager', 'updated_at'])
            
            accept_text = (
                f"✅ Принято менеджером: {manager}\n" 
                f"⏱ Время принятия: {client.updated_at.astimezone().strftime('%Y-%m-%d %H:%M')}"
            )
            
            query.edit_message_text(
                text=f"{accept_text}\n\n{query.message.text}",
                reply_markup=None
            )
            
            context.bot.send_message(
                chat_id=manager.telegram_id,
                text=f"Вы приняли заявку:\n{client.full_name}\nТел: {client.phone}"
            )
            logger.info("Successfully processed client %d by manager %s", client_id, manager.telegram_id)

    except Client.DoesNotExist:
        logger.error("Client %d not found", client_id)
        query.edit_message_text("❌ Заявка не найдена!")
    except Manager.DoesNotExist:
        logger.error("Manager with Telegram ID %s not found", query.from_user.id)
        query.edit_message_text("❌ Вы не зарегистрированы как менеджер!")
    except Exception as e:
        logger.exception("Critical error: %s", str(e))
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
