"""
Script simplificado - Criar anuncio SEM requerer pagina do Facebook
Usa formato de anuncio direto com imagem
"""
import sys
import os
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from dotenv import load_dotenv
from image_generator import ImageGenerator
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adimage import AdImage

load_dotenv()

print("\nCRIANDO ANUNCIO SIMPLIFICADO (sem pagina)")
print("="*60)

# Inicializar APIs
print("\n[1/4] Inicializando...")
image_gen = ImageGenerator()

FacebookAdsApi.init(
    app_id=os.getenv('META_APP_ID'),
    app_secret=os.getenv('META_APP_SECRET'),
    access_token=os.getenv('META_ACCESS_TOKEN')
)
ad_account = AdAccount(os.getenv('META_AD_ACCOUNT_ID'))
print("      [OK] APIs prontas!")

# Gerar imagem
print("\n[2/4] Gerando imagem com IA...")
os.makedirs("./generated_images", exist_ok=True)
image = image_gen.generate_image(
    prompt="Modern luxury apartment with ocean view, professional real estate photo",
    save_path="./generated_images/test_ad.png"
)
print(f"      [OK] Imagem: {image['local_path']}")

# Upload imagem
print("\n[3/4] Upload para Meta...")
ad_image = AdImage(parent_id=ad_account.get_id())
ad_image[AdImage.Field.filename] = "./generated_images/test_ad.png"
ad_image.remote_create()
image_hash = ad_image[AdImage.Field.hash]
print(f"      [OK] Hash: {image_hash}")

# Criar campanha
print("\n[4/4] Criando estrutura de anuncio...")
campaign = ad_account.create_campaign(params={
    Campaign.Field.name: "TESTE Automacao - Sem Pagina",
    Campaign.Field.objective: "OUTCOME_TRAFFIC",
    Campaign.Field.status: "PAUSED",
    Campaign.Field.special_ad_categories: ['HOUSING'],
    'is_adset_budget_sharing_enabled': False
})
print(f"      [OK] Campaign: {campaign.get_id()}")

# Criar ad set
ad_set = ad_account.create_ad_set(params={
    AdSet.Field.name: "AdSet Teste",
    AdSet.Field.campaign_id: campaign.get_id(),
    AdSet.Field.daily_budget: 5000,
    AdSet.Field.billing_event: "IMPRESSIONS",
    AdSet.Field.optimization_goal: "LINK_CLICKS",
    AdSet.Field.targeting: {
        'geo_locations': {'countries': ['BR']},
        'age_min': 25,
        'age_max': 55
    },
    AdSet.Field.status: 'PAUSED',
    AdSet.Field.bid_amount: 500
})
print(f"      [OK] AdSet: {ad_set.get_id()}")

# Criar ad criativo SIMPLES (sem pagina)
creative_params = {
    'name': 'Creative Teste',
    'degrees_of_freedom_spec': {
        'creative_features_spec': {
            'standard_enhancements': {
                'enroll_status': 'OPT_OUT'
            }
        }
    },
    'object_story_spec': {
        'instagram_actor_id': os.getenv('META_PAGE_ID'),
        'link_data': {
            'image_hash': image_hash,
            'link': 'https://www.chatbotimoveis.com.br',
            'message': 'Apartamento de luxo com vista para o mar! Confira.',
            'call_to_action': {
                'type': 'LEARN_MORE',
                'value': {
                    'link': 'https://www.chatbotimoveis.com.br'
                }
            }
        }
    }
}

try:
    creative = ad_account.create_ad_creative(params=creative_params)
    print(f"      [OK] Creative: {creative.get_id()}")

    # Criar ad
    ad = ad_account.create_ad(params={
        Ad.Field.name: "Ad Teste",
        Ad.Field.adset_id: ad_set.get_id(),
        Ad.Field.creative: {'creative_id': creative.get_id()},
        Ad.Field.status: 'PAUSED'
    })

    print(f"      [OK] Ad: {ad.get_id()}")
    print("\n" + "="*60)
    print("SUCESSO! Anuncio criado!")
    print(f"Campaign ID: {campaign.get_id()}")
    print(f"Ad ID: {ad.get_id()}")
    print("\nAcesse: https://adsmanager.facebook.com/adsmanager/manage/campaigns?act=834934475636055")
    print("="*60)

except Exception as e:
    print(f"\n[ERRO] {e}")
    # Tentar sem instagram_actor_id
    print("\nTentando formato alternativo...")
    creative_params2 = {
        'name': 'Creative Teste 2',
        'object_story_spec': {
            'link_data': {
                'image_hash': image_hash,
                'link': 'https://www.chatbotimoveis.com.br',
                'message': 'Apartamento de luxo! Confira agora.'
            }
        }
    }

    try:
        creative2 = ad_account.create_ad_creative(params=creative_params2)
        print(f"      [OK] Creative alternativo: {creative2.get_id()}")

        ad2 = ad_account.create_ad(params={
            Ad.Field.name: "Ad Teste 2",
            Ad.Field.adset_id: ad_set.get_id(),
            Ad.Field.creative: {'creative_id': creative2.get_id()},
            Ad.Field.status: 'PAUSED'
        })

        print(f"      [OK] Ad: {ad2.get_id()}")
        print("\nSUCESSO com formato alternativo!")
        print(f"Ad ID: {ad2.get_id()}")
    except Exception as e2:
        print(f"[ERRO] Tambem falhou: {e2}")
