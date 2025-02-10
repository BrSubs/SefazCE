# Bot Brasil Emplacamentos CE

Bot oficial para consulta e emissão de DAE do IPVA no Ceará.

## 📥 Instalação

### Requisitos
- Windows 10/11
- Python 3.10+
- Google Chrome
- 2GB de espaço livre

### Passo a Passo

#### 1. Instalar Python:
- Baixe em [python.org](https://python.org)
- Marque ✅ "Add to PATH" durante a instalação

#### 2. Instalar Tesseract OCR:
- Baixe [v5.3.1](https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.1.20230401.exe)
- Marque ✅ "Portuguese" e ✅ "Add to PATH"

#### 3. Configurar ChromeDriver:
- Verifique sua versão do Chrome em `chrome://version/`
- Baixe a versão correspondente em [Chromedriver](https://chromedriver.chromium.org/)
- Coloque `chromedriver.exe` na pasta `drivers`

#### 4. Configurar Ambiente:
```powershell
cd Desktop\BotIPVA
python -m pip install -r requirements.txt
```

#### 5. Criar arquivo .env:
```
TELEGRAM_TOKEN="SEU_TOKEN_AQUI"
TESSERACT_PATH="C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
CHROME_DRIVER_PATH="./drivers/chromedriver.exe"
```

## ▶️ Execução

Duplo-clique em `start.bat` ou execute no PowerShell:
```powershell
python main.py
```

## 📲 Como Usar

1. Inicie o bot com `/start`
2. Envie uma das opções:
   - 📝 Texto: `CHASSI 9BGRD08X04G117974` ou `PLACA ABC1D34 RENAVAM 12345678901`
   - 📷 Foto do documento do veículo
3. Confirme os dados
4. Escolha a forma de pagamento
5. Receba o boleto em PDF

## 🛠 Suporte Técnico

Problemas comuns:

- **Erro no ChromeDriver:** Atualize para a mesma versão do Chrome
- **OCR falhou:** Foto precisa estar nítida e bem iluminada
- **Site lento:** O bot tentará novamente após 30 segundos

📩 Contato: [@suporte_emplacamentos](https://t.me/suporte_emplacamentos) no Telegram

