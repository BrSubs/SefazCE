from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext, MessageHandler, filters, CallbackQueryHandler
from bot.handlers.states import BotStates
from bot.services import sefaz_client
from bot.utils import validators
import logging

# Configuração de logging
logger = logging.getLogger(__name__)

async def start(update: Update, context: CallbackContext):
    """Handler para o comando /start"""
    try:
        await update.message.reply_text(
            "🚗 *Bem-vindo ao Brasil Emplacamentos CE Bot*\n\n"
            "Você pode consultar usando:\n"
            "• CHASSI (17 caracteres)\n"
            "• PLACA + RENAVAM\n"
            "• Foto do documento do veículo\n\n"
            "Envie os dados agora:",
            parse_mode='Markdown'
        )
        return BotStates.AWAITING_INPUT
    except Exception as e:
        logger.error(f"Erro no /start: {str(e)}")
        return ConversationHandler.END

async def handle_text(update: Update, context: CallbackContext):
    """Processa entrada de texto (CHASSI ou PLACA + RENAVAM)"""
    try:
        text = update.message.text
        result = validators.validate_text_input(text)
        
        if not result:
            await update.message.reply_text(
                "❌ Formato inválido! Use:\n\n"
                "• CHASSI: 9BGRD08X04G117974\n"
                "• PLACA + RENAVAM: ABC1D34 12345678901"
            )
            return BotStates.AWAITING_INPUT
        
        context.user_data['consult_data'] = result
        return await confirm_data(update, context)
        
    except Exception as e:
        logger.error(f"Erro ao processar texto: {str(e)}")
        await update.message.reply_text("❌ Ocorreu um erro ao processar seus dados. Tente novamente.")
        return BotStates.AWAITING_INPUT

async def confirm_data(update: Update, context: CallbackContext):
    """Confirma os dados extraídos antes de consultar a SEFAZ"""
    try:
        data = context.user_data['consult_data']
        message = "✅ *Dados validados:*\n"
        
        if 'chassi' in data:
            message += f"CHASSI: `{data['chassi']}`"
        else:
            message += f"PLACA: `{data['placa']}`\nRENAVAM: `{data['renavam']}`"
        
        await update.message.reply_text(
            message + "\n\nConfirma os dados?",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Sim ✅", callback_data='confirm_yes')],
                [InlineKeyboardButton("Não ❌", callback_data='confirm_no')]
            ]),
            parse_mode='Markdown'
        )
        return BotStates.CONFIRM_DATA
        
    except Exception as e:
        logger.error(f"Erro na confirmação de dados: {str(e)}")
        await update.message.reply_text("❌ Ocorreu um erro ao confirmar seus dados. Tente novamente.")
        return BotStates.AWAITING_INPUT

async def handle_confirmation(update: Update, context: CallbackContext):
    """Processa a confirmação dos dados e consulta a SEFAZ"""
    query = update.callback_query
    await query.answer()
    
    try:
        if query.data == 'confirm_yes':
            data = context.user_data['consult_data']
            sefaz = sefaz_client.SefazClient()
            ipva_data = sefaz.consultar_ipva(data)
            
            context.user_data['ipva_data'] = ipva_data
            await query.message.reply_text(
                f"💵 *Valores encontrados:*\n\n"
                f"À Vista: {ipva_data['valor']}\n"
                f"Parcelado: {', '.join(ipva_data['parcelas'])}\n\n"
                "Escolha a forma de pagamento:",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("À Vista", callback_data='vista')],
                    [InlineKeyboardButton("Parcelado", callback_data='parcelado')]
                ]),
                parse_mode='Markdown'
            )
            return BotStates.PAYMENT_CHOICE
        else:
            await query.message.reply_text("🔄 Por favor, envie os dados novamente.")
            return BotStates.AWAITING_INPUT
            
    except Exception as e:
        logger.error(f"Erro na consulta à SEFAZ: {str(e)}")
        await query.message.reply_text("❌ Ocorreu um erro ao consultar a SEFAZ. Tente novamente.")
        return BotStates.AWAITING_INPUT

async def cancel(update: Update, context: CallbackContext):
    """Cancela a operação atual"""
    await update.message.reply_text("Operação cancelada.")
    return ConversationHandler.END
