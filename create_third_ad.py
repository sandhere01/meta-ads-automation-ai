"""
Script para criar o terceiro anuncio (Studio Moderno)
Execute depois de renovar o token no .env
"""
import sys
import os
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from dotenv import load_dotenv
from image_generator import ImageGenerator
from meta_ads_manager import MetaAdsManager

load_dotenv()

print("\n" + "="*60)
print("CRIANDO ANUNCIO 3: STUDIO MODERNO")
print("="*60)

print("\n[1/4] Inicializando APIs...")
image_gen = ImageGenerator()
meta_manager = MetaAdsManager()
print("      [OK] APIs inicializadas!")

print("\n[2/4] Gerando imagem com IA...")
image = image_gen.generate_image(
    prompt="""Modern studio apartment in urban setting, compact but functional,
    stylish minimalist interior, city view, professional real estate photo""",
    save_path="./generated_images/studio_urbano.png"
)
print(f"      [OK] Imagem gerada: {image['local_path']}")

print("\n[3/4] Criando anuncio na Meta...")
result = meta_manager.create_complete_ad(
    campaign_name="Campanha Studios Urbanos - Automacao",
    ad_name="Studio Moderno Centro",
    image_path=image['local_path'],
    title="Studio Perfeito no Centro",
    body="Praticidade e estilo no coracao da cidade. Viva onde tudo acontece!",
    link_url="https://www.chatbotimoveis.com.br/studios/urbanos",
    daily_budget=4000,  # R$ 40,00
    targeting={
        'geo_locations': {'countries': ['BR']},
        'age_min': 22,
        'age_max': 35,
    },
    special_ad_categories=['HOUSING']
)

print("\n[4/4] Anuncio criado com sucesso!")
print("="*60)
print("✅ ANUNCIO 3 CRIADO!")
print(f"Campaign ID: {result['campaign_id']}")
print(f"Ad ID: {result['ad_id']}")
print("\nAcesse em:")
print("https://adsmanager.facebook.com/adsmanager/manage/campaigns?act=834934475636055")
print("="*60)
