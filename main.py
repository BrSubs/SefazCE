import os
import logging
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, ConversationHandler, MessageHandler, filters, CallbackQueryHandler
from bot.handlers import data_input, payment, ocr_handler
from bot.handlers.states import BotStates

load_dotenv()

def setup_handlers(application):
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
        fallbacks=[CommandHandler('cancel', data_input.cancel)]
    )
    application.add_handler(conv_handler)

def main():
    application = ApplicationBuilder().token(os.getenv('TELEGRAM_TOKEN')).build()
    setup_handlers(application)
    
    if os.getenv('RENDER'):
        application.run_webhook(
            listen="0.0.0.0",
            port=int(os.getenv('PORT', 10000)),
            webhook_url=f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/{os.getenv('TELEGRAM_TOKEN')}"
        )
    else:
        application.run_polling()

if __name__ == '__main__':
    main()
