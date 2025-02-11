import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler
from bot.handlers import start, handle_renavam, handle_placa, cancel, RENAVAM, PLACA
import os

# Configurações
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Configurar logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def main() -> None:
    """Inicia o bot."""
    application = Application.builder().token(TOKEN).build()

    # Configurar handlers
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            RENAVAM: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_renavam)],
            PLACA: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_placa)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == "__main__":
    main()
