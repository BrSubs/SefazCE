from telegram import Update
from telegram.ext import CallbackContext

async def handle_payment_choice(update: Update, context: CallbackContext):
    """Processa a escolha de pagamento"""
    query = update.callback_query
    await query.answer()
    
    try:
        ipva_data = context.user_data['ipva_data']
        response_text = (
            "💰 *DADOS DO IPVA* 💰\n\n"
            f"🔢 Valor Total: R$ {ipva_data.get('valor', 'N/A')}\n"
            f"📅 Vencimento: {ipva_data.get('vencimento', 'N/A')}\n"
            f"📊 Parcelas: {', '.join(ipva_data.get('parcelas', []))}\n\n"
            "✅ Realize o pagamento no site oficial:\n"
            "https://ipva.sefaz.ce.gov.br"
        )
        
        await query.message.reply_text(response_text, parse_mode='Markdown')
        
    except Exception as e:
        await query.message.reply_text("❌ Erro ao processar pagamento")
    
    return ConversationHandler.END
