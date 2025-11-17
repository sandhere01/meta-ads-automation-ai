"""
Módulo de gerenciamento de anúncios na Meta (Facebook, Instagram, WhatsApp)
"""
import os
from typing import Optional, Literal
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adcreative import AdCreative
from facebook_business.adobjects.adimage import AdImage


class MetaAdsManager:
    """Classe para gerenciar anúncios na plataforma Meta"""

    def __init__(
        self,
        app_id: Optional[str] = None,
        app_secret: Optional[str] = None,
        access_token: Optional[str] = None,
        ad_account_id: Optional[str] = None
    ):
        """
        Inicializa o gerenciador de anúncios Meta

        Args:
            app_id: ID do aplicativo Meta
            app_secret: Secret do aplicativo
            access_token: Token de acesso do usuário
            ad_account_id: ID da conta de anúncios (formato: act_xxxxx)
        """
        self.app_id = app_id or os.getenv('META_APP_ID')
        self.app_secret = app_secret or os.getenv('META_APP_SECRET')
        self.access_token = access_token or os.getenv('META_ACCESS_TOKEN')
        self.ad_account_id = ad_account_id or os.getenv('META_AD_ACCOUNT_ID')

        # Validar credenciais
        if not all([self.app_id, self.app_secret, self.access_token, self.ad_account_id]):
            raise ValueError(
                "Credenciais Meta incompletas. Configure META_APP_ID, META_APP_SECRET, "
                "META_ACCESS_TOKEN e META_AD_ACCOUNT_ID no .env"
            )

        # Inicializar API
        FacebookAdsApi.init(
            app_id=self.app_id,
            app_secret=self.app_secret,
            access_token=self.access_token
        )

        self.ad_account = AdAccount(self.ad_account_id)
        print(f"✅ Meta Ads API inicializada para conta: {self.ad_account_id}")

    def upload_image(self, image_path: str, image_name: Optional[str] = None) -> str:
        """
        Faz upload de uma imagem para a biblioteca de anúncios

        Args:
            image_path: Caminho local da imagem
            image_name: Nome da imagem (opcional)

        Returns:
            Hash da imagem para usar em criativos
        """
        print(f"📤 Fazendo upload da imagem: {image_path}")

        try:
            image = AdImage(parent_id=self.ad_account_id)
            image[AdImage.Field.filename] = image_path

            if image_name:
                image[AdImage.Field.name] = image_name

            image.remote_create()
            image_hash = image[AdImage.Field.hash]

            print(f"✅ Upload concluído! Hash: {image_hash}")
            return image_hash

        except Exception as e:
            print(f"❌ Erro no upload da imagem: {str(e)}")
            raise

    def create_campaign(
        self,
        name: str,
        objective: str = "OUTCOME_TRAFFIC",
        status: str = "PAUSED",
        special_ad_categories: Optional[list] = None
    ) -> Campaign:
        """
        Cria uma nova campanha

        Args:
            name: Nome da campanha
            objective: Objetivo da campanha (OUTCOME_TRAFFIC, OUTCOME_ENGAGEMENT,
                      OUTCOME_LEADS, OUTCOME_SALES, etc.)
            status: Status inicial (PAUSED, ACTIVE)
            special_ad_categories: Categorias especiais (ex: ['HOUSING', 'CREDIT'])

        Returns:
            Objeto Campaign criado
        """
        print(f"📢 Criando campanha: {name}")

        try:
            params = {
                Campaign.Field.name: name,
                Campaign.Field.objective: objective,
                Campaign.Field.status: status,
            }

            if special_ad_categories:
                params[Campaign.Field.special_ad_categories] = special_ad_categories

            # Novo requisito da Meta API: budget sharing
            params['is_adset_budget_sharing_enabled'] = False

            campaign = self.ad_account.create_campaign(params=params)

            print(f"✅ Campanha criada! ID: {campaign.get_id()}")
            return campaign

        except Exception as e:
            print(f"❌ Erro ao criar campanha: {str(e)}")
            raise

    def create_ad_set(
        self,
        campaign_id: str,
        name: str,
        daily_budget: int,
        targeting: dict,
        optimization_goal: str = "LINK_CLICKS",
        billing_event: str = "IMPRESSIONS",
        bid_amount: Optional[int] = None
    ) -> AdSet:
        """
        Cria um conjunto de anúncios

        Args:
            campaign_id: ID da campanha
            name: Nome do conjunto
            daily_budget: Orçamento diário em centavos (ex: 5000 = R$50,00)
            targeting: Dicionário de segmentação (países, idades, etc)
            optimization_goal: Meta de otimização
            billing_event: Evento de cobrança
            bid_amount: Lance em centavos (opcional)

        Returns:
            Objeto AdSet criado
        """
        print(f"🎯 Criando conjunto de anúncios: {name}")

        try:
            params = {
                AdSet.Field.name: name,
                AdSet.Field.campaign_id: campaign_id,
                AdSet.Field.daily_budget: daily_budget,
                AdSet.Field.billing_event: billing_event,
                AdSet.Field.optimization_goal: optimization_goal,
                AdSet.Field.targeting: targeting,
                AdSet.Field.status: 'PAUSED',
            }

            # Definir bid_amount automaticamente se não fornecido
            if bid_amount:
                params[AdSet.Field.bid_amount] = bid_amount
            else:
                # Usar 10% do orçamento diário como lance padrão
                params[AdSet.Field.bid_amount] = int(daily_budget * 0.1)

            ad_set = self.ad_account.create_ad_set(params=params)

            print(f"✅ Conjunto criado! ID: {ad_set.get_id()}")
            return ad_set

        except Exception as e:
            print(f"❌ Erro ao criar conjunto: {str(e)}")
            raise

    def create_ad_creative(
        self,
        name: str,
        image_hash: str,
        title: str,
        body: str,
        link_url: str,
        call_to_action_type: str = "LEARN_MORE",
        page_id: Optional[str] = None
    ) -> AdCreative:
        """
        Cria um criativo de anúncio

        Args:
            name: Nome do criativo
            image_hash: Hash da imagem (retornado por upload_image)
            title: Título do anúncio
            body: Texto principal
            link_url: URL de destino
            call_to_action_type: Tipo de call-to-action
            page_id: ID da página do Facebook (opcional)

        Returns:
            Objeto AdCreative criado
        """
        print(f"🎨 Criando criativo: {name}")

        try:
            page_id = page_id or os.getenv('META_PAGE_ID')

            object_story_spec = {
                'page_id': page_id,
                'link_data': {
                    'image_hash': image_hash,
                    'link': link_url,
                    'message': body,
                    'name': title,
                    'call_to_action': {
                        'type': call_to_action_type,
                        'value': {
                            'link': link_url
                        }
                    }
                }
            }

            params = {
                AdCreative.Field.name: name,
                AdCreative.Field.object_story_spec: object_story_spec
            }

            creative = self.ad_account.create_ad_creative(params=params)

            print(f"✅ Criativo criado! ID: {creative.get_id()}")
            return creative

        except Exception as e:
            print(f"❌ Erro ao criar criativo: {str(e)}")
            raise

    def create_ad(
        self,
        ad_set_id: str,
        creative_id: str,
        name: str,
        status: str = "PAUSED"
    ) -> Ad:
        """
        Cria um anúncio

        Args:
            ad_set_id: ID do conjunto de anúncios
            creative_id: ID do criativo
            name: Nome do anúncio
            status: Status inicial (PAUSED, ACTIVE)

        Returns:
            Objeto Ad criado
        """
        print(f"📱 Criando anúncio: {name}")

        try:
            params = {
                Ad.Field.name: name,
                Ad.Field.adset_id: ad_set_id,
                Ad.Field.creative: {'creative_id': creative_id},
                Ad.Field.status: status,
            }

            ad = self.ad_account.create_ad(params=params)

            print(f"✅ Anúncio criado! ID: {ad.get_id()}")
            return ad

        except Exception as e:
            print(f"❌ Erro ao criar anúncio: {str(e)}")
            raise

    def create_complete_ad(
        self,
        campaign_name: str,
        ad_name: str,
        image_path: str,
        title: str,
        body: str,
        link_url: str,
        daily_budget: int,
        targeting: dict,
        objective: str = "OUTCOME_TRAFFIC",
        call_to_action: str = "LEARN_MORE",
        special_ad_categories: Optional[list] = None
    ) -> dict:
        """
        Cria um anúncio completo (campanha + conjunto + criativo + anúncio)

        Args:
            campaign_name: Nome da campanha
            ad_name: Nome do anúncio
            image_path: Caminho da imagem
            title: Título do anúncio
            body: Texto principal
            link_url: URL de destino
            daily_budget: Orçamento diário em centavos
            targeting: Segmentação
            objective: Objetivo da campanha
            call_to_action: Tipo de CTA

        Returns:
            Dicionário com IDs de todos os objetos criados
        """
        print(f"\n🚀 Criando anúncio completo: {campaign_name}")
        print("=" * 60)

        try:
            # 1. Upload da imagem
            image_hash = self.upload_image(image_path)

            # 2. Criar campanha
            campaign = self.create_campaign(
                name=campaign_name,
                objective=objective,
                status="PAUSED",
                special_ad_categories=special_ad_categories
            )

            # 3. Criar conjunto de anúncios
            ad_set = self.create_ad_set(
                campaign_id=campaign.get_id(),
                name=f"{ad_name} - Ad Set",
                daily_budget=daily_budget,
                targeting=targeting
            )

            # 4. Criar criativo
            creative = self.create_ad_creative(
                name=f"{ad_name} - Creative",
                image_hash=image_hash,
                title=title,
                body=body,
                link_url=link_url,
                call_to_action_type=call_to_action
            )

            # 5. Criar anúncio
            ad = self.create_ad(
                ad_set_id=ad_set.get_id(),
                creative_id=creative.get_id(),
                name=ad_name,
                status="PAUSED"
            )

            result = {
                'campaign_id': campaign.get_id(),
                'ad_set_id': ad_set.get_id(),
                'creative_id': creative.get_id(),
                'ad_id': ad.get_id(),
                'image_hash': image_hash
            }

            print("\n" + "=" * 60)
            print("✅ ANÚNCIO COMPLETO CRIADO COM SUCESSO!")
            print(f"📊 Campaign ID: {result['campaign_id']}")
            print(f"📊 Ad Set ID: {result['ad_set_id']}")
            print(f"📊 Creative ID: {result['creative_id']}")
            print(f"📊 Ad ID: {result['ad_id']}")
            print("=" * 60)

            return result

        except Exception as e:
            print(f"\n❌ Erro ao criar anúncio completo: {str(e)}")
            raise


# Exemplo de uso
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    # Inicializar gerenciador
    manager = MetaAdsManager()

    # Exemplo: Criar anúncio completo
    targeting = {
        'geo_locations': {'countries': ['BR']},
        'age_min': 25,
        'age_max': 55,
    }

    result = manager.create_complete_ad(
        campaign_name="Test Campaign - Real Estate",
        ad_name="Luxury Apartment Ad",
        image_path="./generated_images/apartment_1.png",
        title="Apartamento de Luxo com Vista para o Mar",
        body="Descubra o imóvel dos seus sonhos. Design moderno e localização privilegiada.",
        link_url="https://www.exemplo.com/imoveis",
        daily_budget=5000,  # R$ 50,00
        targeting=targeting
    )

    print(f"\n📊 Resultado final: {result}")
