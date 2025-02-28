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
            # Lock client and related data
            client = Client.objects.select_for_update().select_related('package').get(id=client_id)
            manager = Manager.objects.select_for_update().get(
                telegram_id=str(query.from_user.id)
            )

            # Check if client is already taken
            if client.status != 'new':
                query.edit_message_text("⚠️ Заявка уже принята другим менеджером!")
                return

            # Verify manager's branch matches the client's branch
            if manager.branch != client.package.place:
                query.edit_message_text("❌ Эта заявка не для вашего филиала!")
                logger.error(f"Manager {manager} tried to accept client from another branch")
                return

            # Update client
            client.status = 'processing'
            client.manager = manager
            client.save()

            # Notify manager and update message
            accept_text = (
                f"✅ Принято менеджером: {manager}\n"
                f"⏱ Время принятия: {client.updated_at.strftime('%Y-%m-%d %H:%M')}"
            )
            query.edit_message_text(
                text=f"{accept_text}\n\n{query.message.text}",
                reply_markup=None
            )
            context.bot.send_message(
                chat_id=manager.telegram_id,
                text=f"Вы приняли заявку:\n{client.full_name}\nТел: {client.phone}"
            )

    except (Client.DoesNotExist, Manager.DoesNotExist) as e:
        query.edit_message_text("❌ Ошибка: данные не найдены!")
        logger.error(str(e))
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        query.edit_message_text("❗ Ошибка, попробуйте позже")


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
