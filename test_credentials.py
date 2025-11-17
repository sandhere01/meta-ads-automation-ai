"""
Script para testar as credenciais copiadas do projeto chatbot-imoveis
"""
import os
from dotenv import load_dotenv

print("🔍 Testando Credenciais...\n")
print("="*60)

# Carregar variáveis de ambiente
load_dotenv()

# Verificar se as variáveis existem
print("\n📋 VERIFICANDO VARIÁVEIS DE AMBIENTE:")
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
    if value and value != f"your-{key.lower().replace('_', '-')}-here":
        # Mostrar apenas primeiros e últimos caracteres
        masked = f"{value[:15]}...{value[-10:]}" if len(value) > 25 else "***"
        print(f"✅ {key}: {masked}")
    else:
        print(f"❌ {key}: NÃO CONFIGURADO")

print("\n" + "="*60)
print("\n🧪 TESTANDO APIS:")
print("-"*60)

# Teste 1: OpenAI API
print("\n1️⃣ Testando OpenAI API...")
try:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    # Fazer uma chamada simples
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Say 'test ok' in Portuguese"}],
        max_tokens=10
    )

    result = response.choices[0].message.content
    print(f"   ✅ OpenAI API funcionando!")
    print(f"   📝 Resposta: {result}")

except Exception as e:
    print(f"   ❌ Erro: {str(e)}")
    print(f"   💡 Configure a OPENAI_API_KEY no arquivo .env")

# Teste 2: Anthropic API (Claude)
print("\n2️⃣ Testando Anthropic API (Claude)...")
try:
    import anthropic
    client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

    # Fazer uma chamada simples
    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=10,
        messages=[{"role": "user", "content": "Say 'test ok' in Portuguese"}]
    )

    result = message.content[0].text
    print(f"   ✅ Anthropic API funcionando!")
    print(f"   📝 Resposta: {result}")

except Exception as e:
    print(f"   ❌ Erro: {str(e)}")
    print(f"   💡 Configure a ANTHROPIC_API_KEY no arquivo .env")

# Teste 3: Geração de Imagem com OpenAI DALL-E
print("\n3️⃣ Testando geração de imagem com DALL-E 3...")
try:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    print("   ⏳ Gerando imagem de teste (isso pode levar alguns segundos)...")
    response = client.images.generate(
        model="dall-e-3",
        prompt="A simple test image: white background with text 'OK'",
        size="1024x1024",
        quality="standard",
        n=1
    )

    image_url = response.data[0].url
    print(f"   ✅ Geração de imagem funcionando!")
    print(f"   🔗 URL da imagem: {image_url[:50]}...")

except Exception as e:
    print(f"   ❌ Erro: {str(e)}")
    print(f"   💡 Verifique sua OPENAI_API_KEY e saldo da conta")

# Teste 4: Meta Ads API
print("\n4️⃣ Testando Meta Ads API...")
try:
    meta_app_id = os.getenv('META_APP_ID')
    meta_app_secret = os.getenv('META_APP_SECRET')
    meta_access_token = os.getenv('META_ACCESS_TOKEN')
    meta_account_id = os.getenv('META_AD_ACCOUNT_ID')

    if not meta_app_id or meta_app_id.startswith('your-'):
        print(f"   ⚠️  META_APP_ID não configurado")
        print(f"   📖 Leia CONFIGURACAO_META.md para instruções")
    elif not meta_app_secret or meta_app_secret.startswith('your-'):
        print(f"   ⚠️  META_APP_SECRET não configurado")
        print(f"   📖 Leia CONFIGURACAO_META.md para instruções")
    elif not meta_account_id or meta_account_id.startswith('act_your'):
        print(f"   ⚠️  META_AD_ACCOUNT_ID não configurado")
        print(f"   📖 Leia CONFIGURACAO_META.md para instruções")
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

        print(f"   ✅ Meta Ads API funcionando!")
        print(f"   📊 Conta: {account_info.get('name', 'N/A')}")
        print(f"   📊 Status: {account_info.get('account_status', 'N/A')}")

except ImportError:
    print(f"   ⚠️  Biblioteca facebook-business não instalada")
    print(f"   💡 Execute: pip install -r requirements.txt")
except Exception as e:
    error_msg = str(e)
    print(f"   ❌ Erro: {error_msg}")

    if "Invalid OAuth" in error_msg:
        print(f"   💡 Token inválido ou expirado. Gere um novo em:")
        print(f"      https://developers.facebook.com/tools/explorer/")
    elif "Permissions" in error_msg:
        print(f"   💡 Faltam permissões. Adicione no Graph API Explorer:")
        print(f"      - ads_management")
        print(f"      - business_management")
    else:
        print(f"   📖 Leia CONFIGURACAO_META.md para configurar corretamente")

# Resumo Final
print("\n" + "="*60)
print("📊 RESUMO DOS TESTES")
print("="*60)
print("""
✅ = Funcionando corretamente
⚠️  = Precisa configuração
❌ = Erro encontrado

PRÓXIMOS PASSOS:

1. Se OpenAI está OK (✅):
   → Você pode gerar imagens com DALL-E 3!

2. Se Anthropic está OK (✅):
   → Você pode usar Claude para gerar textos de anúncios!

3. Se Meta Ads tem (⚠️):
   → Leia o arquivo CONFIGURACAO_META.md
   → Configure as credenciais do Meta Ads Manager
   → Execute este teste novamente

4. Quando tudo estiver OK:
   → Execute: python example_real_estate.py
   → Seus anúncios serão criados automaticamente!
""")
print("="*60)
