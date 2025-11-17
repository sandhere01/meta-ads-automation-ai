"""
Teste com o Page ID corrigido para verificar se resolve o problema
"""
import sys
import os
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from dotenv import load_dotenv
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adcreative import AdCreative

load_dotenv()

print("\nTESTE COM PAGE ID CORRIGIDO")
print("=" * 60)

# Inicializar API
FacebookAdsApi.init(
    app_id=os.getenv('META_APP_ID'),
    app_secret=os.getenv('META_APP_SECRET'),
    access_token=os.getenv('META_ACCESS_TOKEN')
)

ad_account = AdAccount(os.getenv('META_AD_ACCOUNT_ID'))
page_id = os.getenv('META_PAGE_ID')

print(f"\nConta de Anuncios: {ad_account.get_id()}")
print(f"Page ID configurado: {page_id}")
print(f"Nome da pagina: Treinamento de I.A. Para Corretores de Imoveis")

# Usar um hash de imagem que ja foi feito upload antes
# (do teste anterior)
image_hash = "05b5ee799139dbc049d019c57e7ad2c7"

print(f"\nTestando criacao de criativo com Page ID correto...")
print("-" * 60)

try:
    creative_params = {
        'name': 'Teste Page Corrigido',
        'object_story_spec': {
            'page_id': page_id,
            'link_data': {
                'image_hash': image_hash,
                'link': 'https://www.chatbotimoveis.com.br',
                'message': 'Teste com pagina correta - Treinamento de IA para Corretores',
                'name': 'Teste Page ID',
                'call_to_action': {
                    'type': 'LEARN_MORE',
                    'value': {
                        'link': 'https://www.chatbotimoveis.com.br'
                    }
                }
            }
        }
    }

    creative = ad_account.create_ad_creative(params=creative_params)
    print(f"\n✅ SUCESSO! Creative criado com ID: {creative.get_id()}")
    print("\nO problema era apenas o Page ID incorreto!")
    print("Agora voce pode executar run_automation.py para criar os anuncios completos.")

except Exception as e:
    print(f"\n❌ ERRO: {str(e)}")
    print("\nPossiveis causas:")
    print("1. Token ainda sem permissao 'pages_manage_ads'")
    print("2. Pagina nao conectada a conta de anuncios")
    print("\nVeja o arquivo SOLUCAO_PAGINA.md para instrucoes completas.")

print("\n" + "=" * 60)
