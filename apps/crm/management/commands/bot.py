import logging
from django.core.management.base import BaseCommand
from telegram.ext import Updater, CallbackQueryHandler
from django.conf import settings
from django.db import transaction
from ...models import Client, Manager
from django.utils.timezone import localtime

logger = logging.getLogger(__name__)

def build_notification_text(client, manager):
    """Формирование текста уведомления после принятия заявки"""
    accept_time = client.updated_at.strftime("%Y-%m-%d %H:%M")
    place = f"{client.country}, {client.city}"
    package_place = client.package.get_place_display()
    
    return (
        f"✅ Принято менеджером: {manager.fio}\n"
        f"⏱ Время принятия: {accept_time}\n\n"
        f"📣 Новая заявка ({package_place})❗️\n"
        f"👤 Имя: {client.full_name}\n"
        f"📞 Телефон: {client.phone}\n"
        f"🌍 Место: {place}\n"
        f"📦 Пакет: {client.package.name}"
    )

def handle_accept(update, context):
    query = update.callback_query
    query.answer()

    try:
        client_id = int(query.data.split('_')[1])
        client = Client.objects.select_related('package').get(id=client_id)
        manager = Manager.objects.get(telegram_id=str(query.from_user.id))

        if client.status != 'new':
            query.edit_message_text("⚠️ Заявка уже принята другим менеджером!")
            return

        if manager.branch != client.package.place:
            query.edit_message_text("❌ Заявка не для вашего филиала!")
            return

        with transaction.atomic():
            client.status = 'processing'
            client.manager = manager
            client.save(update_fields=['status', 'manager', 'updated_at'])

            # Форматируем время с учетом часового пояса Django
            from django.utils.timezone import localtime
            local_time = localtime(client.updated_at)
            accept_time = local_time.strftime("%Y-%m-%d %H:%M")
            
            new_text = build_notification_text(client, manager)
            
            context.bot.edit_message_text(
                chat_id=settings.TELEGRAM_GROUP_IDS[client.package.place],
                message_id=query.message.message_id,
                text=new_text,
                reply_markup=None
            )

    except Client.DoesNotExist:
        logger.error(f"Client not found: {client_id}")
        query.edit_message_text("❌ Заявка не найдена!")

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

