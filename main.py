import os
import logging
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, ConversationHandler, MessageHandler, filters, CallbackQueryHandler
from bot.handlers import data_input, payment, ocr_handler

# Carregar variáveis de ambiente
load_dotenv()

# Configuração de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main():
    # Criar aplicação do bot
    application = ApplicationBuilder().token(os.getenv('TELEGRAM_TOKEN')).build()
    
    # Configurar handlers
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
    
    # Iniciar o bot
    application.run_polling()

if __name__ == '__main__':
    main()
