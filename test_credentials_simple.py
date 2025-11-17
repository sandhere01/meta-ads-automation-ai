"""
Script para testar as credenciais - Versao Windows
"""
import os
import sys
from dotenv import load_dotenv

# Configurar encoding UTF-8 para Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("Testando Credenciais...\n")
print("="*60)

# Carregar variaveis de ambiente
load_dotenv()

# Verificar se as variaveis existem
print("\nVERIFICANDO VARIAVEIS DE AMBIENTE:")
print("-"*60)

credentials = {
    'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
    'ANTHROPIC_API_KEY': os.getenv('ANTHROPIC_API_KEY'),
    'META_APP_ID': os.getenv('META_APP_ID'),
    'META_APP_SECRET': os.getenv('META_APP_SECRET'),
    'META_ACCESS_TOKEN': os.getenv('META_ACCESS_TOKEN'),
    'META_AD_ACCOUNT_ID': os.getenv('META_AD_ACCOUNT_ID'),
}

for key, value in credentials.items():
    if value and not value.startswith('your-'):
        masked = f"{value[:15]}...{value[-10:]}" if len(value) > 25 else "***"
        print(f"[OK] {key}: {masked}")
    else:
        print(f"[X] {key}: NAO CONFIGURADO")

print("\n" + "="*60)
print("\nTESTANDO APIS:")
print("-"*60)

# Teste 1: OpenAI API
print("\n1. Testando OpenAI API...")
try:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Say 'test ok' in Portuguese"}],
        max_tokens=10
    )

    result = response.choices[0].message.content
    print(f"   [OK] OpenAI API funcionando!")
    print(f"   Resposta: {result}")

except Exception as e:
    print(f"   [ERRO] {str(e)}")
    print(f"   Configure a OPENAI_API_KEY no arquivo .env")

# Teste 2: Meta Ads API
print("\n2. Testando Meta Ads API...")
try:
    meta_app_id = os.getenv('META_APP_ID')
    meta_app_secret = os.getenv('META_APP_SECRET')
    meta_access_token = os.getenv('META_ACCESS_TOKEN')
    meta_account_id = os.getenv('META_AD_ACCOUNT_ID')

    if not meta_app_id or meta_app_id.startswith('your-'):
        print(f"   [AVISO] META_APP_ID nao configurado")
    elif not meta_app_secret or meta_app_secret.startswith('your-'):
        print(f"   [AVISO] META_APP_SECRET nao configurado")
    elif not meta_account_id or meta_account_id.startswith('act_your'):
        print(f"   [AVISO] META_AD_ACCOUNT_ID nao configurado")
    else:
        from facebook_business.api import FacebookAdsApi
        from facebook_business.adobjects.adaccount import AdAccount

        # Inicializar API
        FacebookAdsApi.init(
            app_id=meta_app_id,
            app_secret=meta_app_secret,
            access_token=meta_access_token
        )

        # Tentar acessar a conta
        account = AdAccount(meta_account_id)
        account_info = account.api_get(fields=['name', 'account_status'])

        print(f"   [OK] Meta Ads API funcionando!")
        print(f"   Conta: {account_info.get('name', 'N/A')}")
        print(f"   Status: {account_info.get('account_status', 'N/A')}")

except ImportError:
    print(f"   [AVISO] Biblioteca facebook-business nao instalada")
    print(f"   Execute: pip install -r requirements.txt")
except Exception as e:
    error_msg = str(e)
    print(f"   [ERRO] {error_msg}")

    if "Invalid OAuth" in error_msg:
        print(f"   Token invalido ou expirado. Gere um novo em:")
        print(f"   https://developers.facebook.com/tools/explorer/")
    elif "Permissions" in error_msg:
        print(f"   Faltam permissoes. Adicione no Graph API Explorer:")
        print(f"   - ads_management")
        print(f"   - business_management")

# Resumo Final
print("\n" + "="*60)
print("RESUMO DOS TESTES")
print("="*60)
print("""
[OK] = Funcionando corretamente
[AVISO] = Precisa configuracao
[ERRO] = Erro encontrado

PROXIMOS PASSOS:

1. Se OpenAI esta OK:
   -> Voce pode gerar imagens com DALL-E 3!

2. Se Meta Ads esta OK:
   -> Execute: python example_real_estate.py
   -> Seus anuncios serao criados automaticamente!

3. Se houver erros:
   -> Leia o arquivo CONFIGURACAO_META.md
   -> Execute este teste novamente
""")
print("="*60)
