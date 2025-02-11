import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler
from bot.validators import validate_renavam, validate_placa
from bot.scraper import SefazScraper

# Estados da conversa
RENAVAM, PLACA = range(2)

__all__ = ["start", "handle_renavam", "handle_placa", "cancel", "RENAVAM", "PLACA"]

# Configurar logging
logger = logging.getLogger(__name__)


async def start(update: Update, context: CallbackContext) -> int:
    """Inicia a conversa."""
    await update.message.reply_text(
        "🚗 Bem-vindo ao consultor de IPVA da SEFAZ-CE!\n"
        "Por favor, digite o número do RENAVAM (11 dígitos):"
    )
    return RENAVAM


async def handle_renavam(update: Update, context: CallbackContext) -> int:
    """Valida e armazena o RENAVAM."""
    renavam = update.message.text.strip()
    if not validate_renavam(renavam):
        await update.message.reply_text(
            "Formato inválido! O RENAVAM deve conter 11 dígitos. Tente novamente:"
        )
        return RENAVAM

    context.user_data["renavam"] = renavam
    await update.message.reply_text(
        "Ótimo! Agora digite a placa do veículo (formato Mercosul ou antigo):"
    )
    return PLACA


async def handle_placa(update: Update, context: CallbackContext) -> int:
    """Valida e armazena a placa."""
    placa = update.message.text.strip().upper()
    if not validate_placa(placa):
        await update.message.reply_text(
            "Formato inválido! Use o formato Mercosul (ABC1D23) ou antigo (ABC1234). Tente novamente:"
        )
        return PLACA

    context.user_data["placa"] = placa
    return await consultar_ipva(update, context)


async def consultar_ipva(update: Update, context: CallbackContext) -> int:
    """Consulta o IPVA e exibe os resultados."""
    user_data = context.user_data
    scraper = SefazScraper()
    resultado = scraper.consultar_ipva(user_data["renavam"], user_data["placa"])

    if not resultado:
        await update.message.reply_text(
            "Serviço indisponível no momento. Tente novamente mais tarde."
        )
        return ConversationHandler.END

    # Montar resposta
    message = (
        f"📄 **Consulta IPVA - SEFAZ-CE**\n"
        f"🔢 RENAVAM: {user_data['renavam']}\n"
        f"🚘 Placa: {user_data['placa']}\n\n"
        f"💵 *Valor à vista:* {resultado['ipva_vista']}\n"
        f"📅 *Valor parcelado:* {resultado['ipva_parcelado']}\n"
        f"📌 *Status:* {resultado['status']}\n"
    )

    if resultado["divida_ativa"]:
        message += "\n⚠️ **ATENÇÃO:** Há débitos em dívida ativa! Procure um despachante ou posto da SEFAZ."

    keyboard = [
        [
            InlineKeyboardButton("Pagamento à Vista", callback_data="vista"),
            InlineKeyboardButton("Parcelamento", callback_data="parcelado"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        message, parse_mode="Markdown", reply_markup=reply_markup
    )
    return ConversationHandler.END


async def cancel(update: Update, context: CallbackContext) -> int:
    """Cancela a conversa."""
    await update.message.reply_text("Consulta cancelada.")
    return ConversationHandler.END
