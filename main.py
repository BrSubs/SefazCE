from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler
from bot.handlers import start, handle_renavam, handle_placa, cancel, RENAVAM, PLACA
import os
import logging

# Configurações
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # URL do webhook no Render
PORT = int(os.getenv("PORT", 8443))  # Porta padrão do Render

# Configurar logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def post_init(application: Application) -> None:
    """Configura o webhook após a inicialização do bot."""
    await application.bot.set_webhook(WEBHOOK_URL)
    logger.info(f"Webhook configurado com sucesso: {WEBHOOK_URL}")


def main() -> None:
    """Inicia o bot."""
    application = Application.builder().token(TOKEN).post_init(post_init).build()

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

    # Iniciar o bot com webhook
    # application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=WEBHOOK_URL,
    )


if __name__ == "__main__":
    main()
