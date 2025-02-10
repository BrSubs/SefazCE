from telegram import Update
from telegram.ext import CallbackContext
import pytesseract
from PIL import Image, ImageEnhance
import io
import requests
from bot.utils import validators
from bot.handlers import data_input

async def handle_photo(update: Update, context: CallbackContext):
    """Processa foto enviada pelo usuário"""
    try:
        # Baixa a imagem
        photo_file = await update.message.photo[-1].get_file()
        response = requests.get(photo_file.file_path)
        image = Image.open(io.BytesIO(response.content))
        
        # Pré-processamento
        image = image.convert('L')  # Escala de cinza
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2.0)
        
        # OCR
        text = pytesseract.image_to_string(image, lang='por')
        data = validators.extract_from_ocr(text)
        
        if not data:
            raise ValueError("Dados não encontrados na imagem")
        
        context.user_data['consult_data'] = data
        return await data_input.confirm_data(update, context)
        
    except Exception as e:
        await update.message.reply_text(f"❌ Erro no OCR: {str(e)}")
        return data_input.AWAITING_INPUT
