import os
import logging
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, ConversationHandler, MessageHandler, filters, CallbackQueryHandler
from bot.handlers import data_input, payment, ocr_handler
from bot.handlers.states import BotStates

load_dotenv()

# Configuração de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def create_application():
    """Factory para criar a aplicação com configurações essenciais"""
    return ApplicationBuilder().token(os.getenv('TELEGRAM_TOKEN')).build()

def setup_conversation_handler(application):
    """Configura o fluxo principal da conversação"""
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', data_input.start)],
        states={
            BotStates.AWAITING_INPUT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, data_input.handle_text),
                MessageHandler(filters.PHOTO, ocr_handler.handle_photo)
            ],
            BotStates.CONFIRM_DATA: [
                CallbackQueryHandler(data_input.handle_confirmation)
            ],
            BotStates.PAYMENT_CHOICE: [
                CallbackQueryHandler(payment.handle_payment_choice)
            ]
        },
        fallbacks=[CommandHandler('cancel', data_input.cancel)],
        per_message=True  # Resolve o warning do PTB
    )
    application.add_handler(conv_handler)

def run_application(application):
    """Inicia a aplicação conforme o ambiente"""
    if os.getenv('RENDER'):
        application.run_webhook(
            listen="0.0.0.0",
            port=int(os.getenv('PORT', 10000)),
            webhook_url=f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/{os.getenv('TELEGRAM_TOKEN')}",
            drop_pending_updates=True
        )
    else:
        application.run_polling(drop_pending_updates=True)

def main():
    try:
        application = create_application()
        setup_conversation_handler(application)
        run_application(application)
    except Exception as e:
        logger.critical(f"Falha crítica na inicialização: {str(e)}")

if __name__ == '__main__':
    main()
