"""
Script de automacao completa - Versao Windows sem emojis
Gera imagens com IA e cria anuncios na Meta automaticamente
"""
import sys
import os

# Configurar encoding UTF-8 para Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from dotenv import load_dotenv
from image_generator import ImageGenerator
from meta_ads_manager import MetaAdsManager

# Carregar variaveis de ambiente
load_dotenv()

print("\n" + "="*60)
print("AUTOMACAO DE ANUNCIOS - Chatbot Imoveis")
print("="*60)

try:
    # Inicializar geradores
    print("\n[1/5] Inicializando APIs...")
    image_gen = ImageGenerator()
    meta_manager = MetaAdsManager()
    print("      [OK] APIs inicializadas com sucesso!")

    # Exemplo 1: Apartamento de Luxo
    print("\n[2/5] Criando Anuncio 1: Apartamento de Luxo")
    print("-"*60)

    # Gerar imagem
    print("      Gerando imagem com IA...")
    os.makedirs("./generated_images", exist_ok=True)

    image1 = image_gen.generate_image(
        prompt="""Modern luxury apartment interior with panoramic ocean view,
        floor-to-ceiling windows, minimalist design, natural sunlight,
        elegant furniture, professional real estate photography""",
        size="1024x1024",
        quality="standard",
        style="vivid",
        save_path="./generated_images/apt_luxo.png"
    )
    print(f"      [OK] Imagem gerada: {image1['local_path']}")

    # Criar anuncio completo
    print("      Criando anuncio na Meta...")

    targeting1 = {
        'geo_locations': {'countries': ['BR']},
        'age_min': 35,
        'age_max': 60,
    }

    ad1 = meta_manager.create_complete_ad(
        campaign_name="Campanha Apartamentos Luxo - Automacao",
        ad_name="Apartamento Luxo Vista Mar",
        image_path="./generated_images/apt_luxo.png",
        title="Apartamento de Luxo Frente Mar",
        body="Viva com Vista para o Mar! Design moderno, vista panoramica, acabamento premium.",
        link_url="https://www.chatbotimoveis.com.br/apartamentos/luxo",
        daily_budget=5000,  # R$ 50/dia
        targeting=targeting1,
        objective="OUTCOME_TRAFFIC",
        special_ad_categories=['HOUSING']  # OBRIGATORIO para anuncios de imoveis
    )

    print(f"      [OK] Anuncio 1 criado!")
    print(f"      Campaign ID: {ad1['campaign_id']}")
    print(f"      Ad ID: {ad1['ad_id']}")

    # Exemplo 2: Casa Familiar
    print("\n[3/5] Criando Anuncio 2: Casa Familiar")
    print("-"*60)

    print("      Gerando imagem com IA...")
    image2 = image_gen.generate_image(
        prompt="""Beautiful suburban family house with garden, modern architecture,
        warm lighting at sunset, green lawn, family-friendly atmosphere""",
        size="1024x1024",
        quality="standard",
        style="vivid",
        save_path="./generated_images/casa_familia.png"
    )
    print(f"      [OK] Imagem gerada: {image2['local_path']}")

    print("      Criando anuncio na Meta...")

    targeting2 = {
        'geo_locations': {'countries': ['BR']},
        'age_min': 30,
        'age_max': 50,
    }

    ad2 = meta_manager.create_complete_ad(
        campaign_name="Campanha Casas Familiares - Automacao",
        ad_name="Casa Ideal para Familia",
        image_path="./generated_images/casa_familia.png",
        title="Casa Perfeita para Sua Familia",
        body="O Lar dos Seus Sonhos! Espaco ideal, jardim amplo, area de lazer completa.",
        link_url="https://www.chatbotimoveis.com.br/casas",
        daily_budget=5000,  # R$ 50/dia
        targeting=targeting2,
        special_ad_categories=['HOUSING']
    )

    print(f"      [OK] Anuncio 2 criado!")
    print(f"      Campaign ID: {ad2['campaign_id']}")
    print(f"      Ad ID: {ad2['ad_id']}")

    # Exemplo 3: Studio Moderno
    print("\n[4/5] Criando Anuncio 3: Studio Moderno")
    print("-"*60)

    print("      Gerando imagem com IA...")
    image3 = image_gen.generate_image(
        prompt="""Modern compact studio apartment, efficient space design,
        natural light, minimalist furniture, city view, young professional lifestyle""",
        size="1024x1024",
        quality="standard",
        style="vivid",
        save_path="./generated_images/studio.png"
    )
    print(f"      [OK] Imagem gerada: {image3['local_path']}")

    print("      Criando anuncio na Meta...")

    targeting3 = {
        'geo_locations': {'countries': ['BR']},
        'age_min': 22,
        'age_max': 35,
    }

    ad3 = meta_manager.create_complete_ad(
        campaign_name="Campanha Studios Centro - Automacao",
        ad_name="Studio Moderno Centro",
        image_path="./generated_images/studio.png",
        title="Studio Moderno no Coracao da Cidade",
        body="Vida Urbana com Estilo! Localizacao central, design inteligente, preco acessivel.",
        link_url="https://www.chatbotimoveis.com.br/studios",
        daily_budget=3000,  # R$ 30/dia
        targeting=targeting3,
        special_ad_categories=['HOUSING']
    )

    print(f"      [OK] Anuncio 3 criado!")
    print(f"      Campaign ID: {ad3['campaign_id']}")
    print(f"      Ad ID: {ad3['ad_id']}")

    # Resumo
    print("\n[5/5] Resumo Final")
    print("="*60)
    print("SUCESSO! Todos os anuncios foram criados!")
    print("="*60)
    print(f"\nAnuncios criados: 3")
    print(f"Imagens geradas: 3")
    print(f"Campanhas criadas: 3")
    print(f"\nLocal das imagens: ./generated_images/")
    print(f"\nStatus: PAUSADO (ative manualmente no Ads Manager)")
    print(f"\nAcesse seus anuncios em:")
    print(f"https://adsmanager.facebook.com/adsmanager/manage/campaigns?act=834934475636055")
    print("\n" + "="*60)
    print("AUTOMACAO CONCLUIDA COM SUCESSO!")
    print("="*60 + "\n")

except Exception as e:
    print(f"\n[ERRO] Falha na automacao: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
