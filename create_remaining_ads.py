"""
Script para criar os anuncios restantes (2 e 3) com retry logic
"""
import sys
import os
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from dotenv import load_dotenv
from image_generator import ImageGenerator
from meta_ads_manager import MetaAdsManager
import time

load_dotenv()

print("\n" + "="*60)
print("CRIANDO ANUNCIOS RESTANTES (2 e 3)")
print("="*60)

print("\n[1/3] Inicializando APIs...")
image_gen = ImageGenerator()
meta_manager = MetaAdsManager()
print("      [OK] APIs inicializadas com sucesso!")

def create_ad_with_retry(ad_config, max_retries=3):
    """Cria um anuncio com retry logic para erros transientes"""
    for attempt in range(1, max_retries + 1):
        try:
            print(f"\n[Tentativa {attempt}/{max_retries}]")

            # Gerar imagem
            print(f"      Gerando imagem com IA...")
            image = image_gen.generate_image(
                prompt=ad_config['prompt'],
                save_path=ad_config['image_path']
            )
            print(f"      [OK] Imagem gerada: {image['local_path']}")

            # Criar anuncio completo
            print(f"      Criando anuncio na Meta...")
            result = meta_manager.create_complete_ad(
                campaign_name=ad_config['campaign_name'],
                ad_name=ad_config['ad_name'],
                image_path=image['local_path'],
                title=ad_config['title'],
                body=ad_config['body'],
                link_url=ad_config['link_url'],
                daily_budget=ad_config['daily_budget'],
                targeting=ad_config['targeting'],
                special_ad_categories=ad_config['special_ad_categories']
            )

            print(f"      [OK] Anuncio criado!")
            print(f"      Campaign ID: {result['campaign_id']}")
            print(f"      Ad ID: {result['ad_id']}")
            return result

        except Exception as e:
            error_msg = str(e)

            # Verificar se e erro transiente (500)
            if '"is_transient": true' in error_msg or 'code": 2' in error_msg:
                if attempt < max_retries:
                    wait_time = attempt * 5  # Espera crescente: 5s, 10s, 15s
                    print(f"      [AVISO] Erro transiente da Meta API")
                    print(f"      Aguardando {wait_time} segundos antes de tentar novamente...")
                    time.sleep(wait_time)
                    continue
                else:
                    print(f"      [ERRO] Falhou apos {max_retries} tentativas")
                    raise
            else:
                # Erro nao transiente, nao vale a pena retry
                print(f"      [ERRO] {error_msg}")
                raise

    raise Exception("Numero maximo de tentativas excedido")

# Configuracao dos anuncios restantes
ads_config = [
    {
        'name': 'Anuncio 2: Casa Familiar',
        'campaign_name': 'Campanha Casas Familiares - Automacao',
        'ad_name': 'Casa Ideal para Familia',
        'image_path': './generated_images/casa_familia.png',
        'prompt': '''Beautiful suburban family house with garden, modern architecture,
        warm lighting at sunset, green lawn, real estate photography, inviting atmosphere''',
        'title': 'Casa dos Sonhos para sua Familia',
        'body': 'Espaco, conforto e qualidade de vida. Sua familia merece!',
        'link_url': 'https://www.chatbotimoveis.com.br/casas/familiares',
        'daily_budget': 5000,  # R$ 50,00
        'targeting': {
            'geo_locations': {'countries': ['BR']},
            'age_min': 30,
            'age_max': 50,
        },
        'special_ad_categories': ['HOUSING']
    },
    {
        'name': 'Anuncio 3: Studio Moderno',
        'campaign_name': 'Campanha Studios Urbanos - Automacao',
        'ad_name': 'Studio Moderno Centro',
        'image_path': './generated_images/studio_urbano.png',
        'prompt': '''Modern studio apartment in urban setting, compact but functional,
        stylish minimalist interior, city view, professional real estate photo''',
        'title': 'Studio Perfeito no Centro',
        'body': 'Praticidade e estilo no coracao da cidade. Viva onde tudo acontece!',
        'link_url': 'https://www.chatbotimoveis.com.br/studios/urbanos',
        'daily_budget': 4000,  # R$ 40,00
        'targeting': {
            'geo_locations': {'countries': ['BR']},
            'age_min': 22,
            'age_max': 35,
        },
        'special_ad_categories': ['HOUSING']
    }
]

# Criar os anuncios
results = []
failed = []

for i, config in enumerate(ads_config, start=2):
    print(f"\n[{i}/3] Criando {config['name']}")
    print("-" * 60)

    try:
        result = create_ad_with_retry(config)
        results.append(result)
    except Exception as e:
        print(f"\n[ERRO] Falha ao criar {config['name']}: {e}")
        failed.append(config['name'])

# Resumo final
print("\n" + "="*60)
print("RESUMO FINAL")
print("="*60)

print(f"\n✅ Anuncios criados com sucesso: {len(results) + 1}")  # +1 pelo primeiro que ja foi criado
print(f"❌ Anuncios que falharam: {len(failed)}")

if results:
    print("\nAnuncios criados nesta execucao:")
    for i, result in enumerate(results, start=2):
        print(f"\n  Anuncio {i}:")
        print(f"    Campaign ID: {result['campaign_id']}")
        print(f"    Ad ID: {result['ad_id']}")

if failed:
    print("\nAnuncios que falharam:")
    for name in failed:
        print(f"  - {name}")

print("\n" + "="*60)
print("\nAcesse seus anuncios em:")
print("https://adsmanager.facebook.com/adsmanager/manage/campaigns?act=834934475636055")
print("="*60)
