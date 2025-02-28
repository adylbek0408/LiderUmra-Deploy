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

        # Проверка статуса заявки
        if client.status != 'new':
            query.edit_message_text("⚠️ Заявка уже принята другим менеджером!")
            return

        # Проверка филиала менеджера
        if manager.branch != client.package.place:
            query.edit_message_text("❌ Заявка не для вашего филиала!")
            return

        # Обновление заявки
        with transaction.atomic():
            client.status = 'processing'
            client.manager = manager
            client.save(update_fields=['status', 'manager', 'updated_at'])

            # Формирование сообщения
            new_text = build_notification_text(client, manager)  # Новая функция
            
            # Редактирование сообщения
            context.bot.edit_message_text(
                chat_id=settings.TELEGRAM_GROUP_IDS[client.package.place],
                message_id=query.message.message_id,
                text=new_text,
                reply_markup=None
            )

    except Client.DoesNotExist:
        logger.error(f"Client not found: {client_id}")
        query.edit_message_text("❌ Заявка не найдена!")
    except Manager.DoesNotExist:
        logger.error(f"Manager not found: {query.from_user.id}")
        query.edit_message_text("❌ Вы не зарегистрированы как менеджер!")
    except KeyError as e:
        logger.error(f"Group not found for branch: {e}")
        query.edit_message_text("❌ Ошибка группы филиала")
    except Exception as e:
        logger.exception(f"Critical error: {str(e)}")
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

