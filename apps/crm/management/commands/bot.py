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
        client = Client.objects.select_related('package').get(id=client_id)
        manager = Manager.objects.get(telegram_id=str(query.from_user.id))

        # Проверка принадлежности к филиалу
        if manager.branch != client.package.place:
            query.edit_message_text("❌ Заявка не для вашего филиала!")
            return

        # Остальная логика обработки...
        
        # Редактируем сообщение в правильной группе
        if client.notification_chat_id and client.notification_message_id:
            context.bot.edit_message_text(
                chat_id=client.notification_chat_id,
                message_id=client.notification_message_id,
                text=new_text,
                reply_markup=None
            )

    except Exception as e:
        logger.exception("Error: %s", str(e))


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
    