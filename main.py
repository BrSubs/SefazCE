import os
import logging
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, ConversationHandler, MessageHandler, filters, CallbackQueryHandler
from bot.handlers import data_input, payment, ocr_handler

# Configuração do ambiente
load_dotenv()

# Constantes para deploy
PORT = int(os.environ.get('PORT', 10000))
RENDER_MODE = os.environ.get('RENDER')

# Configuração de logs
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def setup_handlers(application):
    """Configura todos os handlers do bot"""
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', data_input.start)],
        states={
            data_input.AWAITING_INPUT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, data_input.handle_text),
                MessageHandler(filters.PHOTO, ocr_handler.handle_photo)
            ],
            data_input.CONFIRM_DATA: [
                CallbackQueryHandler(data_input.handle_confirmation)
            ],
            payment.PAYMENT_CHOICE: [
                CallbackQueryHandler(payment.handle_payment_choice)
            ]
        },
        fallbacks=[CommandHandler('cancel', data_input.cancel)]
    )
    application.add_handler(conv_handler)

def main():
    application = ApplicationBuilder().token(os.getenv('TELEGRAM_TOKEN')).build()
    
    setup_handlers(application)
    
    # Modo produção no Render
    if RENDER_MODE:
        application.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            webhook_url=f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/{os.getenv('TELEGRAM_TOKEN')}"
        )
    else:
        # Modo desenvolvimento local
        application.run_polling()

if __name__ == '__main__':
    main()