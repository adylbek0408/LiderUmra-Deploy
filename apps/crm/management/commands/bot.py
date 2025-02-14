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
        logger.error("Invalid callback data")
        return

    try:
        with transaction.atomic():
            # Lock client row and related manager
            client = Client.objects.select_for_update().get(id=client_id)
            manager = Manager.objects.select_for_update().get(
                telegram_id=str(query.from_user.id)
            )

            if client.status != 'new':
                query.edit_message_text("⚠️ Заявка уже принята другим менеджером!")
                return

            # Update client status
            client.status = 'processing'
            client.manager = manager
            client.save()

            # Update message in Telegram
            accept_text = (
                f"✅ Принято менеджером: {manager}\n" 
                f"⏱ Время принятия: {client.updated_at.strftime('%Y-%m-%d %H:%M')}"
                )
            query.edit_message_text(
                text=f"{accept_text}\n\n{query.message.text}",
                reply_markup=None
            )

            # Send confirmation to manager
            context.bot.send_message(
                chat_id=manager.telegram_id,
                text=f"Вы успешно приняли заявку:\n{client.full_name}\nТел: {client.phone}"
            )

    except Client.DoesNotExist:
        query.edit_message_text("❌ Заявка не найдена!")
        logger.error(f"Client not found: {client_id}")
    except Manager.DoesNotExist:
        query.edit_message_text("❌ Вы не зарегистрированы как менеджер!")
        logger.error(f"Manager not found: {query.from_user.id}")
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        query.edit_message_text("❗ Произошла ошибка, попробуйте позже")


class Command(BaseCommand):
    help = 'Run Telegram bot'

    def handle(self, *args, **options):
        updater = Updater(
            settings.TELEGRAM_BOT_TOKEN,
            use_context=True
        )
        
        # Add error handler
        updater.dispatcher.add_error_handler(self.error_handler)

        dp = updater.dispatcher
        dp.add_handler(CallbackQueryHandler(handle_accept, pattern='^accept_'))

        self.stdout.write("✅ Бот успешно запущен")
        updater.start_polling()
        updater.idle()

    def error_handler(self, update, context):
        logger.error(f'Update {update} caused error: {context.error}')
