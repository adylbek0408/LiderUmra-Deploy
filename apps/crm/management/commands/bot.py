import logging
from django.core.management.base import BaseCommand
from telegram.ext import Updater, CallbackQueryHandler, CommandHandler
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from ...models import Client, Manager
import traceback

logger = logging.getLogger(__name__)


def build_notification_text(client, manager):
    """Build notification text for accepted client."""
    accept_time = timezone.localtime(client.updated_at).strftime('%Y-%m-%d %H:%M')

    return (
        f"✅ Принято менеджером: {manager.full_name}\n"
        f"⏱ Время принятия: {accept_time}\n\n"
        f"📣 Новая заявка ({client.package.place})❗️\n"
        f"👤 Имя: {client.full_name}\n"
        f"📞 Телефон: {client.phone}\n"
        f"🌍 Место: {client.country}, {client.city}\n"
        f"📦 Пакет: {client.package.name or 'Не указан'}"
    )


def handle_accept(update, context):
    """Handle accept button click."""
    query = update.callback_query
    query.answer()

    try:
        # Extract client ID from callback data
        client_id = int(query.data.split('_')[1])
        chat_id = query.message.chat.id
        message_id = query.message.message_id

        with transaction.atomic():
            # Fetch client with package and lock the row
            client = Client.objects.select_related('package') \
                .filter(package__isnull=False) \
                .select_for_update() \
                .get(id=client_id)

            # Verify manager exists
            manager = Manager.objects.get(telegram_id=str(query.from_user.id))

            # Validate package branch
            if not client.package.place:
                context.bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id,
                    text="❌ У пакета не указан филиал!",
                    reply_markup=None
                )
                return

            # Validate manager branch
            if manager.branch != client.package.place:
                context.bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id,
                    text="❌ Заявка не для вашего филиала!",
                    reply_markup=None
                )
                return

            # Validate client status
            if client.status != 'new':
                context.bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id,
                    text="⚠️ Заявка уже принята другим менеджером!",
                    reply_markup=None
                )
                return

            # Update client status and assign manager
            client.status = 'processing'
            client.manager = manager
            client.save(update_fields=['status', 'manager', 'updated_at'])

            # Edit original message to remove the button
            new_text = build_notification_text(client, manager)
            context.bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=new_text,
                reply_markup=None
            )

            # Notify manager privately
            context.bot.send_message(
                chat_id=manager.telegram_id,
                text=f"Вы приняли заявку:\n{client.full_name}\n{client.phone}"
            )

    except Client.DoesNotExist:
        logger.error(f"Client not found: {client_id}")
        query.edit_message_text("❌ Заявка не найдена!", reply_markup=None)
    except Manager.DoesNotExist:
        logger.error(f"Manager not found: {query.from_user.id}")
        query.edit_message_text("❌ Вы не зарегистрированы как менеджер!", reply_markup=None)
    except Exception as e:
        logger.error(f"Critical error: {str(e)}\n{traceback.format_exc()}")
        context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="❗ Ошибка, попробуйте позже",
            reply_markup=None
        )


def handle_start(update, context):
    """Handle /start command for manager registration."""
    try:
        user = update.effective_user

        # Create or update manager
        Manager.objects.update_or_create(
            telegram_id=str(user.id),
            defaults={
                'full_name': user.full_name,
                'branch': 'Bishkek'  # Default branch, can be updated later
            }
        )

        update.message.reply_text(
            "✅ Вы успешно зарегистрированы как менеджер!\n"
            f"Ваш ID: {user.id}\n"
            f"Филиал: Bishkek (по умолчанию)"
        )

    except Exception as e:
        logger.error(f"Error in /start command: {str(e)}")
        update.message.reply_text("❌ Ошибка при регистрации. Попробуйте позже.")


class Command(BaseCommand):
    help = 'Run Telegram bot'

    def handle(self, *args, **options):
        updater = Updater(settings.TELEGRAM_BOT_TOKEN, use_context=True)

        # Add handlers
        updater.dispatcher.add_handler(CommandHandler('start', handle_start))
        updater.dispatcher.add_handler(CallbackQueryHandler(handle_accept, pattern='^accept_'))
        updater.dispatcher.add_error_handler(self.error_handler)

        self.stdout.write("✅ Бот успешно запущен")
        updater.start_polling()
        updater.idle()

    def error_handler(self, update, context):
        """Handle errors in the bot."""
        logger.error('Update "%s" caused error: %s', update, context.error)
