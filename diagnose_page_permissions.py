"""
Script para diagnosticar permissoes da pagina e conexoes com a conta de anuncios
"""
import sys
import os
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from dotenv import load_dotenv
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.user import User
import json

load_dotenv()

print("\nDIAGNOSTICO DE PERMISSOES E CONFIGURACOES")
print("=" * 70)

# Inicializar API
FacebookAdsApi.init(
    app_id=os.getenv('META_APP_ID'),
    app_secret=os.getenv('META_APP_SECRET'),
    access_token=os.getenv('META_ACCESS_TOKEN')
)

print("\n[1] Verificando informacoes do usuario...")
print("-" * 70)
try:
    me = User(fbid='me')
    user_info = me.api_get(fields=['id', 'name'])
    print(f"Usuario: {user_info.get('name')} (ID: {user_info.get('id')})")
except Exception as e:
    print(f"ERRO ao obter informacoes do usuario: {e}")

print("\n[2] Verificando permissoes do token de acesso...")
print("-" * 70)
try:
    me = User(fbid='me')
    permissions = me.api_get(fields=['permissions'])

    if 'permissions' in permissions:
        granted = [p['permission'] for p in permissions['permissions']['data'] if p['status'] == 'granted']
        declined = [p['permission'] for p in permissions['permissions']['data'] if p['status'] == 'declined']

        print(f"\nPermissoes CONCEDIDAS ({len(granted)}):")
        for perm in sorted(granted):
            print(f"  - {perm}")

        if declined:
            print(f"\nPermissoes NEGADAS ({len(declined)}):")
            for perm in sorted(declined):
                print(f"  - {perm}")

        # Verificar permissoes criticas
        critical_perms = ['ads_management', 'pages_read_engagement', 'pages_manage_ads', 'business_management']
        missing = [p for p in critical_perms if p not in granted]

        if missing:
            print(f"\nALERTA: Permissoes criticas faltando:")
            for perm in missing:
                print(f"  - {perm}")
    else:
        print("Nao foi possivel obter permissoes")

except Exception as e:
    print(f"ERRO ao verificar permissoes: {e}")

print("\n[3] Verificando paginas do usuario...")
print("-" * 70)
try:
    me = User(fbid='me')
    accounts = me.get_accounts(fields=['id', 'name', 'access_token', 'tasks'])

    print(f"\nPaginas encontradas: {len(list(accounts))}")
    accounts = me.get_accounts(fields=['id', 'name', 'access_token', 'tasks'])  # Re-fetch

    for page in accounts:
        print(f"\n  Pagina: {page.get('name')}")
        print(f"  ID: {page.get('id')}")
        print(f"  Tarefas (roles): {page.get('tasks', [])}")

        if page.get('id') == os.getenv('META_PAGE_ID'):
            print("  >>> ESTA E A PAGINA CONFIGURADA NO .env <<<")

            # Verificar se tem access_token da pagina
            if 'access_token' in page:
                print("  Token de acesso da pagina: Disponivel")
            else:
                print("  Token de acesso da pagina: NAO disponivel")

except Exception as e:
    print(f"ERRO ao listar paginas: {e}")

print("\n[4] Verificando configuracoes da conta de anuncios...")
print("-" * 70)
try:
    ad_account = AdAccount(os.getenv('META_AD_ACCOUNT_ID'))
    account_info = ad_account.api_get(fields=[
        'id',
        'name',
        'account_status',
        'currency',
        'timezone_name',
        'business'
    ])

    print(f"\nConta de Anuncios: {account_info.get('name')}")
    print(f"ID: {account_info.get('id')}")
    print(f"Status: {account_info.get('account_status')}")
    print(f"Moeda: {account_info.get('currency')}")
    print(f"Fuso Horario: {account_info.get('timezone_name')}")

    if 'business' in account_info:
        print(f"Business ID: {account_info['business'].get('id')}")
        print(f"Business Nome: {account_info['business'].get('name')}")

except Exception as e:
    print(f"ERRO ao verificar conta de anuncios: {e}")

print("\n[5] Verificando se a pagina esta conectada a conta de anuncios...")
print("-" * 70)
try:
    # Tentar obter informacoes especificas da pagina configurada
    from facebook_business.adobjects.page import Page

    page_id = os.getenv('META_PAGE_ID')
    page = Page(fbid=page_id)

    try:
        page_info = page.api_get(fields=['id', 'name', 'is_published'])
        print(f"\nPagina ID {page_id}:")
        print(f"Nome: {page_info.get('name')}")
        print(f"Publicada: {page_info.get('is_published')}")
        print("Acesso a pagina: OK")
    except Exception as e:
        print(f"\nERRO ao acessar pagina {page_id}: {e}")
        print("Isso pode indicar que o token nao tem permissao para acessar esta pagina")

except Exception as e:
    print(f"ERRO ao verificar pagina: {e}")

print("\n" + "=" * 70)
print("DIAGNOSTICO COMPLETO")
print("=" * 70)
print("\nPROXIMOS PASSOS:")
print("1. Verifique se todas as permissoes criticas foram concedidas")
print("2. Verifique se a pagina aparece na lista de paginas do usuario")
print("3. Se a pagina nao aparece, pode ser necessario:")
print("   - Adicionar a pagina a conta de anuncios no Business Manager")
print("   - Gerar um novo token com permissoes de pagina")
print("   - Verificar se voce tem role de administrador na pagina")
print("=" * 70)
