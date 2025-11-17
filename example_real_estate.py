"""
Exemplo Prático: Automação para Anúncios de Imóveis
"""
from automation_main import AdAutomation
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Inicializar automação
automation = AdAutomation()

print("\n" + "="*60)
print("🏠 EXEMPLO: AUTOMAÇÃO DE ANÚNCIOS DE IMÓVEIS")
print("="*60)

# Exemplo 1: Apartamento de Luxo
print("\n📍 Criando anúncio: Apartamento de Luxo")
print("-"*60)

apartamento_luxo = automation.create_ad_with_ai_image(
    # Configuração da imagem
    image_prompt="""
    Luxurious modern apartment interior with floor-to-ceiling windows,
    panoramic ocean view, minimalist Scandinavian design,
    elegant white and beige furniture, natural sunlight,
    professional real estate photography, wide angle
    """,
    image_size="1024x1024",
    image_quality="hd",
    image_style="vivid",

    # Configuração do anúncio
    campaign_name="Campanha Apartamentos Luxo - Costa",
    ad_title="Apartamento de Luxo Frente Mar",
    ad_body="""
🏖️ Viva com Vista para o Mar!

✨ Design moderno e sofisticado
🌊 Vista panorâmica do oceano
🏠 Acabamento de alto padrão
📍 Localização privilegiada
🔒 Segurança 24h

Agende sua visita e se apaixone!
    """,
    link_url="https://www.seusite.com/apartamentos/luxo",
    daily_budget=10000,  # R$ 100/dia

    # Segmentação
    targeting={
        'geo_locations': {
            'countries': ['BR'],
            'regions': [{'key': '3450'}]  # São Paulo
        },
        'age_min': 35,
        'age_max': 60,
        'interests': [
            {'id': 6003139266461, 'name': 'Real estate'},
            {'id': 6003107902433, 'name': 'Luxury goods'}
        ]
    },

    objective="OUTCOME_TRAFFIC",
    call_to_action="LEARN_MORE"
)

if apartamento_luxo['success']:
    print(f"✅ Sucesso! Ad ID: {apartamento_luxo['meta_ad']['ad_id']}")
else:
    print(f"❌ Erro: {apartamento_luxo.get('error')}")


# Exemplo 2: Casa Familiar
print("\n📍 Criando anúncio: Casa Familiar")
print("-"*60)

casa_familiar = automation.create_ad_with_ai_image(
    image_prompt="""
    Beautiful suburban family house with garden,
    modern architecture, warm lighting at sunset,
    green lawn, family-friendly atmosphere,
    professional real estate photo
    """,
    image_quality="standard",

    campaign_name="Campanha Casas Familiares",
    ad_title="Casa Perfeita para Sua Família",
    ad_body="""
🏡 O Lar dos Seus Sonhos!

👨‍👩‍👧‍👦 Espaço ideal para família
🌳 Jardim amplo e arborizado
🚗 Garagem para 3 carros
🎯 Próximo a escolas e parques
💚 Área de lazer completa

Venha conhecer!
    """,
    link_url="https://www.seusite.com/casas/familiar",
    daily_budget=7000,

    targeting={
        'geo_locations': {'countries': ['BR']},
        'age_min': 30,
        'age_max': 50,
        'interests': [
            {'id': 6003139266461, 'name': 'Real estate'}
        ],
        'life_events': [
            {'id': 6002714398172, 'name': 'Recently moved'}
        ]
    }
)

if casa_familiar['success']:
    print(f"✅ Sucesso! Ad ID: {casa_familiar['meta_ad']['ad_id']}")
else:
    print(f"❌ Erro: {casa_familiar.get('error')}")


# Exemplo 3: Studio para Jovens Profissionais
print("\n📍 Criando anúncio: Studio Moderno")
print("-"*60)

studio = automation.create_ad_with_ai_image(
    image_prompt="""
    Modern compact studio apartment,
    efficient space design, industrial chic style,
    natural light, young professional lifestyle,
    minimalist furniture, city view
    """,
    image_quality="standard",

    campaign_name="Campanha Studios Centro",
    ad_title="Studio Moderno no Coração da Cidade",
    ad_body="""
🌆 Vida Urbana com Estilo!

⚡ Localização central
🚇 Ao lado do metrô
💼 Ideal para home office
🎯 Design inteligente
💰 Preço acessível

Seu primeiro imóvel te espera!
    """,
    link_url="https://www.seusite.com/studios",
    daily_budget=5000,

    targeting={
        'geo_locations': {'countries': ['BR']},
        'age_min': 22,
        'age_max': 35,
        'interests': [
            {'id': 6003139266461, 'name': 'Real estate'}
        ]
    }
)

if studio['success']:
    print(f"✅ Sucesso! Ad ID: {studio['meta_ad']['ad_id']}")
else:
    print(f"❌ Erro: {studio.get('error')}")


# Resumo final
print("\n" + "="*60)
print("📊 RESUMO DA AUTOMAÇÃO")
print("="*60)

total_ads = 3
successful_ads = sum([
    1 if apartamento_luxo.get('success') else 0,
    1 if casa_familiar.get('success') else 0,
    1 if studio.get('success') else 0
])

print(f"✅ Anúncios criados com sucesso: {successful_ads}/{total_ads}")
print(f"📁 Logs salvos em: ./logs/")
print(f"🖼️ Imagens salvas em: ./generated_images/")

if successful_ads == total_ads:
    print("\n🎉 Parabéns! Todos os anúncios foram criados com sucesso!")
    print("💡 Acesse o Meta Ads Manager para ativar suas campanhas.")
    print("🔗 https://business.facebook.com/adsmanager")
else:
    print(f"\n⚠️ {total_ads - successful_ads} anúncio(s) falharam.")
    print("💡 Verifique os logs para mais detalhes.")

print("="*60 + "\n")
