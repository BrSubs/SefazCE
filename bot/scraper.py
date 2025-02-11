import time
from typing import Optional, Dict
from lxml import html
import requests


class SefazScraper:
    """Classe para interagir com o site da SEFAZ-CE."""

    def __init__(self):
        self.base_url = "https://ipva.sefaz.ce.gov.br/#/impostos/emitir-dae"
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
        )

    def consultar_ipva(self, renavam: str, placa: str) -> Optional[Dict]:
        """Consulta o IPVA no site da SEFAZ-CE."""
        try:
            # Acessar a página inicial
            response = self.session.get(f"{self.base_url}/#/impostos/emitir-dae", timeout=10)
            response.raise_for_status()

            # Parsear o HTML
            tree = html.fromstring(response.content)

            # Preencher os campos de placa e RENAVAM
            placa_input = tree.xpath('//*[@id="md-input-3"]')[0]
            renavam_input = tree.xpath('//*[@id="md-input-5"]')[0]

            placa_input.value = placa
            renavam_input.value = renavam

            # Submeter o formulário
            form = tree.forms[0]
            response = self.session.submit_form(form)
            response.raise_for_status()

            # Parsear a resposta
            result_tree = html.fromstring(response.content)
            ipva_vista = result_tree.xpath('//div[@class="ipva-vista"]/text()')[0].strip()
            ipva_parcelado = result_tree.xpath('//div[@class="ipva-parcelado"]/text()')[0].strip()
            status = result_tree.xpath('//span[@class="status-pagamento"]/text()')[0].strip()
            divida = result_tree.xpath('//div[@class="divida-ativa"]/text()')

            return {
                "ipva_vista": ipva_vista,
                "ipva_parcelado": ipva_parcelado,
                "status": status,
                "divida_ativa": bool(divida),
            }

        except Exception as e:
            print(f"Erro durante a consulta: {e}")
            return None