from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext, MessageHandler, filters, CallbackQueryHandler, ConversationHandler
from bot.services import sefaz_client
from bot.utils import validators
import logging

# Estados da conversa
AWAITING_INPUT, CONFIRM_DATA = range(2)

async def start(update: Update, context: CallbackContext):
    """Inicia o fluxo de consulta"""
    await update.message.reply_text(
        "🚗 *Brasil Emplacamentos CE Bot*\n\n"
        "Envie:\n"
        "• CHASSI (17 caracteres)\n"
        "• PLACA + RENAVAM\n"
        "• Foto do documento do veículo",
        parse_mode='Markdown'
    )
    return AWAITING_INPUT

async def handle_text(update: Update, context: CallbackContext):
    """Processa entrada de texto"""
    text = update.message.text
    result = validators.validate_text_input(text)
    
    if not result:
        await update.message.reply_text(
            "❌ Formato inválido! Use:\n\n"
            "• CHASSI: 9BGRD08X04G117974\n"
            "• PLACA + RENAVAM: ABC1D34 12345678901"
        )
        return AWAITING_INPUT
    
    context.user_data['consult_data'] = result
    return await confirm_data(update, context)

async def confirm_data(update: Update, context: CallbackContext):
    """Confirma os dados extraídos"""
    data = context.user_data['consult_data']
    message = "✅ *Dados validados:*\n"
    
    if 'chassi' in data:
        message += f"CHASSI: `{data['chassi']}`"
    else:
        message += f"PLACA: `{data['placa']}`\nRENAVAM: `{data['renavam']}`"
    
    await update.message.reply_text(
        message + "\n\nConfirmar consulta?",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Sim", callback_data='confirm_yes')]]),
        parse_mode='Markdown'
    )
    return CONFIRM_DATA

async def handle_confirmation(update: Update, context: CallbackContext):
    """Processa confirmação dos dados"""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'confirm_yes':
        try:
            data = context.user_data['consult_data']
            sefaz = sefaz_client.SefazClient()
            ipva_data = sefaz.consultar_ipva(data)
            
            context.user_data['ipva_data'] = ipva_data
            await query.message.reply_text(f"Valor do IPVA: R$ {ipva_data['valor']}")
            return payment.PAYMENT_CHOICE
            
        except Exception as e:
            await query.message.reply_text(f"Erro na consulta: {str(e)}")
            return ConversationHandler.END

async def cancel(update: Update, context: CallbackContext):
    """Cancela a operação"""
    await update.message.reply_text("Operação cancelada.")
    return ConversationHandler.END
