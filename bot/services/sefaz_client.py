import requests
from bs4 import BeautifulSoup

class SefazClient:
    def __init__(self):
        self.base_url = "https://ipva.sefaz.ce.gov.br"
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'Accept-Language': 'pt-BR,pt;q=0.9'
        }
        
    def _get_csrf_token(self):
        """Obtém token de segurança necessário para as requisições"""
        try:
            response = self.session.get(f"{self.base_url}/#/impostos/emitir-dae")
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup.find('meta', {'name': 'csrf-token'})['content']
        except Exception as e:
            raise Exception("Falha ao obter token CSRF")

    def consultar_ipva(self, data: dict):
        """Consulta oficial na SEFAZ-CE com tratamento de erros"""
        try:
            csrf_token = self._get_csrf_token()
            
            payload = {
                '_token': csrf_token,
                'tipo_consulta': 'chassi' if 'chassi' in data else 'placa',
                'chassi' if 'chassi' in data else 'placa': data['chassi'] if 'chassi' in data else data['placa'],
                'renavam': data.get('renavam', '')
            }
            
            response = self.session.post(
                f"{self.base_url}/api/consulta-ipva",
                json=payload,
                headers={'X-Requested-With': 'XMLHttpRequest'}
            )
            
            if response.status_code != 200:
                raise Exception(f"Erro HTTP {response.status_code}")
                
            return response.json()
            
        except Exception as e:
            raise Exception(f"Falha na consulta: {str(e)}")