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
            # Eager load related data
            client = Client.objects.select_related('package').get(id=client_id)
            manager = Manager.objects.get(telegram_id=str(query.from_user.id))

            # Validate client status FIRST
            if client.status != 'new':
                query.edit_message_text("⚠️ Заявка уже принята другим менеджером!")
                return

            # Verify branch match
            if manager.branch != client.package.place:
                logger.warning("Branch mismatch: manager %s vs client %s", 
                              manager.branch, client.package.place)
                query.edit_message_text("❌ Эта заявка не для вашего филиала!")
                return

            # Update client
            client.status = 'processing'
            client.manager = manager
            client.save(update_fields=['status', 'manager', 'updated_at'])

            # Format acceptance message
            accept_text = (
                f"✅ Принято менеджером: {manager.user.get_full_name() or manager.user.username}\n"
                f"⏱ Время принятия: {client.updated_at.astimezone().strftime('%Y-%m-%d %H:%M')}"
            )
            
            # Edit original message
            query.edit_message_text(
                text=f"{accept_text}\n\n{query.message.text}",
                reply_markup=None
            )
            
            # Send confirmation to manager
            context.bot.send_message(
                chat_id=manager.telegram_id,
                text=f"Вы приняли заявку:\n{client.full_name}\nТел: {client.phone}"
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
