"""
Script principal de automação: Geração de imagens + Publicação de anúncios Meta
"""
import os
from dotenv import load_dotenv
from image_generator import ImageGenerator
from meta_ads_manager import MetaAdsManager
from typing import Optional
import json
from datetime import datetime


class AdAutomation:
    """Classe principal para automação completa de anúncios"""

    def __init__(self):
        """Inicializa a automação carregando variáveis de ambiente"""
        load_dotenv()

        print("🚀 Inicializando Automação de Anúncios")
        print("=" * 60)

        self.image_generator = ImageGenerator()
        self.meta_manager = MetaAdsManager()

        print("✅ Automação inicializada com sucesso!")
        print("=" * 60 + "\n")

    def create_ad_with_ai_image(
        self,
        # Parâmetros da imagem
        image_prompt: str,
        image_size: str = "1024x1024",
        image_quality: str = "hd",
        image_style: str = "vivid",

        # Parâmetros do anúncio
        campaign_name: str = None,
        ad_title: str = None,
        ad_body: str = None,
        link_url: str = None,
        daily_budget: int = 5000,

        # Segmentação
        targeting: Optional[dict] = None,

        # Configurações adicionais
        objective: str = "OUTCOME_TRAFFIC",
        call_to_action: str = "LEARN_MORE",
        save_locally: bool = True
    ) -> dict:
        """
        Cria um anúncio completo: gera imagem com IA e publica na Meta

        Args:
            image_prompt: Descrição da imagem para DALL-E
            image_size: Tamanho da imagem
            image_quality: Qualidade (standard/hd)
            image_style: Estilo (vivid/natural)
            campaign_name: Nome da campanha
            ad_title: Título do anúncio
            ad_body: Texto principal
            link_url: URL de destino
            daily_budget: Orçamento diário em centavos
            targeting: Segmentação do público
            objective: Objetivo da campanha
            call_to_action: Tipo de CTA
            save_locally: Salvar imagem localmente

        Returns:
            Dicionário com informações da imagem e do anúncio criado
        """
        print("\n" + "=" * 60)
        print("🎯 INICIANDO AUTOMAÇÃO COMPLETA")
        print("=" * 60)

        try:
            # Gerar timestamp para nomes únicos
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            # 1. GERAR IMAGEM COM IA
            print("\n📍 ETAPA 1/2: Gerando imagem com IA")
            print("-" * 60)

            image_path = None
            if save_locally:
                os.makedirs("./generated_images", exist_ok=True)
                image_path = f"./generated_images/ad_image_{timestamp}.png"

            image_result = self.image_generator.generate_image(
                prompt=image_prompt,
                size=image_size,
                quality=image_quality,
                style=image_style,
                save_path=image_path
            )

            print(f"✅ Imagem gerada com sucesso!")
            print(f"🔗 URL: {image_result['url']}")

            if not image_path:
                print("\n⚠️  Aviso: Imagem não foi salva localmente.")
                print("💡 Dica: Para publicar na Meta, a imagem precisa ser salva localmente.")
                print("    Defina save_locally=True ou forneça um save_path.")
                return {
                    'success': False,
                    'image': image_result,
                    'error': 'Imagem não salva localmente'
                }

            # 2. PUBLICAR ANÚNCIO NA META
            print("\n📍 ETAPA 2/2: Publicando anúncio na Meta")
            print("-" * 60)

            # Configurar targeting padrão se não fornecido
            if targeting is None:
                targeting = {
                    'geo_locations': {'countries': ['BR']},
                    'age_min': 25,
                    'age_max': 55,
                }

            # Usar nomes padrão se não fornecidos
            campaign_name = campaign_name or f"Campaign_{timestamp}"
            ad_title = ad_title or "Descubra algo incrível"
            ad_body = ad_body or image_result.get('revised_prompt', image_prompt)[:500]
            link_url = link_url or "https://www.exemplo.com"

            meta_result = self.meta_manager.create_complete_ad(
                campaign_name=campaign_name,
                ad_name=f"Ad_{timestamp}",
                image_path=image_path,
                title=ad_title,
                body=ad_body,
                link_url=link_url,
                daily_budget=daily_budget,
                targeting=targeting,
                objective=objective,
                call_to_action=call_to_action
            )

            # 3. COMPILAR RESULTADOS
            final_result = {
                'success': True,
                'timestamp': timestamp,
                'image': {
                    'url': image_result['url'],
                    'local_path': image_path,
                    'revised_prompt': image_result['revised_prompt'],
                    'size': image_result['size'],
                    'quality': image_result['quality']
                },
                'meta_ad': {
                    'campaign_id': meta_result['campaign_id'],
                    'ad_set_id': meta_result['ad_set_id'],
                    'creative_id': meta_result['creative_id'],
                    'ad_id': meta_result['ad_id'],
                    'campaign_name': campaign_name,
                    'title': ad_title,
                    'body': ad_body,
                    'link': link_url,
                    'daily_budget': daily_budget
                }
            }

            # Salvar log em JSON
            log_path = f"./logs/automation_log_{timestamp}.json"
            os.makedirs("./logs", exist_ok=True)
            with open(log_path, 'w', encoding='utf-8') as f:
                json.dump(final_result, f, indent=2, ensure_ascii=False)

            print("\n" + "=" * 60)
            print("🎉 AUTOMAÇÃO CONCLUÍDA COM SUCESSO!")
            print("=" * 60)
            print(f"📊 Log salvo em: {log_path}")
            print(f"🖼️  Imagem: {image_path}")
            print(f"📱 Campaign ID: {meta_result['campaign_id']}")
            print(f"📱 Ad ID: {meta_result['ad_id']}")
            print("=" * 60 + "\n")

            return final_result

        except Exception as e:
            error_msg = f"Erro na automação: {str(e)}"
            print(f"\n❌ {error_msg}")

            return {
                'success': False,
                'error': error_msg,
                'timestamp': timestamp
            }

    def create_multiple_ads(self, ads_config: list[dict]) -> list[dict]:
        """
        Cria múltiplos anúncios em lote

        Args:
            ads_config: Lista de configurações de anúncios

        Returns:
            Lista de resultados
        """
        print(f"\n🚀 Criando {len(ads_config)} anúncios em lote...")

        results = []
        for i, config in enumerate(ads_config, 1):
            print(f"\n{'='*60}")
            print(f"📍 Anúncio {i}/{len(ads_config)}")
            print(f"{'='*60}")

            result = self.create_ad_with_ai_image(**config)
            results.append(result)

        successful = sum(1 for r in results if r.get('success'))
        print(f"\n✅ Concluído! {successful}/{len(ads_config)} anúncios criados com sucesso.")

        return results


# Exemplos de uso
if __name__ == "__main__":

    # Inicializar automação
    automation = AdAutomation()

    # EXEMPLO 1: Criar um anúncio simples
    print("\n🏠 EXEMPLO 1: Anúncio de Imóvel de Luxo")
    print("=" * 60)

    result = automation.create_ad_with_ai_image(
        # Parâmetros da imagem
        image_prompt="""
        Modern luxury apartment interior with panoramic ocean view,
        floor-to-ceiling windows, minimalist Scandinavian design,
        natural sunlight, elegant furniture, white and beige tones,
        professional real estate photography style
        """,
        image_size="1024x1024",
        image_quality="hd",
        image_style="vivid",

        # Parâmetros do anúncio
        campaign_name="Campanha Imóveis de Luxo - Novembro 2025",
        ad_title="Apartamento de Luxo com Vista para o Mar",
        ad_body="""
        Descubra o imóvel dos seus sonhos! 🏖️
        ✨ Design moderno e elegante
        🌊 Vista panorâmica para o oceano
        📍 Localização privilegiada
        Agende sua visita hoje mesmo!
        """,
        link_url="https://www.exemplo.com/imoveis/luxo",
        daily_budget=10000,  # R$ 100,00 por dia

        # Segmentação
        targeting={
            'geo_locations': {
                'countries': ['BR'],
                'regions': [{'key': '3450'}],  # São Paulo
            },
            'age_min': 30,
            'age_max': 55,
            'interests': [
                {'id': 6003139266461, 'name': 'Real estate'},
                {'id': 6003107902433, 'name': 'Luxury goods'}
            ]
        },

        objective="OUTCOME_TRAFFIC",
        call_to_action="LEARN_MORE"
    )

    print(f"\n📊 Resultado: {json.dumps(result, indent=2, ensure_ascii=False)}")


    # EXEMPLO 2: Criar múltiplos anúncios
    print("\n\n🎯 EXEMPLO 2: Criar 3 Anúncios de Diferentes Imóveis")
    print("=" * 60)

    ads_batch = [
        {
            'image_prompt': 'Modern studio apartment, compact and efficient design, natural light',
            'campaign_name': 'Campanha Studios Modernos',
            'ad_title': 'Studio Moderno no Centro',
            'ad_body': 'Perfeito para jovens profissionais. Localização privilegiada!',
            'link_url': 'https://exemplo.com/studios',
            'daily_budget': 5000
        },
        {
            'image_prompt': 'Luxury penthouse terrace with city skyline view, sunset lighting',
            'campaign_name': 'Campanha Coberturas Premium',
            'ad_title': 'Cobertura Premium com Vista',
            'ad_body': 'Viva no topo! Exclusividade e sofisticação em cada detalhe.',
            'link_url': 'https://exemplo.com/coberturas',
            'daily_budget': 15000,
            'image_quality': 'hd'
        },
        {
            'image_prompt': 'Cozy family house with garden, modern suburban home, warm lighting',
            'campaign_name': 'Campanha Casas Familiares',
            'ad_title': 'Casa Perfeita para Sua Família',
            'ad_body': 'Ampla, confortável e segura. O lar que você sempre sonhou!',
            'link_url': 'https://exemplo.com/casas',
            'daily_budget': 8000
        }
    ]

    # Descomente a linha abaixo para criar os anúncios em lote
    # batch_results = automation.create_multiple_ads(ads_batch)

    print("\n✅ Script finalizado!")
