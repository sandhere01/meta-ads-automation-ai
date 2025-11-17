"""
Módulo de geração de imagens usando OpenAI DALL-E 3
"""
import os
import requests
from openai import OpenAI
from typing import Optional, Literal
import base64


class ImageGenerator:
    """Classe para gerar imagens usando a API OpenAI DALL-E 3"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializa o gerador de imagens

        Args:
            api_key: Chave da API OpenAI (se None, usa variável de ambiente)
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY não encontrada. Configure no .env ou passe como parâmetro")

        self.client = OpenAI(api_key=self.api_key)

    def generate_image(
        self,
        prompt: str,
        size: Literal["1024x1024", "1792x1024", "1024x1792"] = "1024x1024",
        quality: Literal["standard", "hd"] = "standard",
        style: Literal["vivid", "natural"] = "vivid",
        save_path: Optional[str] = None
    ) -> dict:
        """
        Gera uma imagem usando DALL-E 3

        Args:
            prompt: Descrição da imagem desejada (máx 4000 caracteres)
            size: Tamanho da imagem
            quality: Qualidade da imagem ('standard' ou 'hd')
            style: Estilo ('vivid' para dramático ou 'natural' para realista)
            save_path: Caminho para salvar a imagem localmente

        Returns:
            dict com 'url', 'revised_prompt' e opcionalmente 'local_path'
        """
        if len(prompt) > 4000:
            raise ValueError("Prompt muito longo. Máximo 4000 caracteres para DALL-E 3")

        print(f"🎨 Gerando imagem com DALL-E 3...")
        print(f"📝 Prompt: {prompt[:100]}...")

        try:
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size=size,
                quality=quality,
                style=style,
                n=1  # DALL-E 3 só suporta n=1
            )

            image_url = response.data[0].url
            revised_prompt = response.data[0].revised_prompt

            result = {
                'url': image_url,
                'revised_prompt': revised_prompt,
                'size': size,
                'quality': quality,
                'style': style
            }

            # Salvar imagem localmente se solicitado
            if save_path:
                local_path = self._download_image(image_url, save_path)
                result['local_path'] = local_path
                print(f"✅ Imagem salva em: {local_path}")

            print(f"✅ Imagem gerada com sucesso!")
            print(f"🔗 URL: {image_url}")
            print(f"📝 Prompt revisado pela IA: {revised_prompt}")

            return result

        except Exception as e:
            print(f"❌ Erro ao gerar imagem: {str(e)}")
            raise

    def _download_image(self, url: str, save_path: str) -> str:
        """
        Baixa a imagem da URL e salva localmente

        Args:
            url: URL da imagem
            save_path: Caminho onde salvar

        Returns:
            Caminho completo do arquivo salvo
        """
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            # Criar diretório se não existir
            os.makedirs(os.path.dirname(save_path), exist_ok=True)

            with open(save_path, 'wb') as f:
                f.write(response.content)

            return save_path

        except Exception as e:
            print(f"❌ Erro ao baixar imagem: {str(e)}")
            raise

    def generate_multiple_variations(
        self,
        base_prompt: str,
        variations: list[str],
        **kwargs
    ) -> list[dict]:
        """
        Gera múltiplas variações de uma imagem

        Args:
            base_prompt: Prompt base
            variations: Lista de modificações para criar variações
            **kwargs: Parâmetros adicionais para generate_image

        Returns:
            Lista de resultados de cada variação
        """
        results = []

        for i, variation in enumerate(variations, 1):
            full_prompt = f"{base_prompt}. {variation}"
            print(f"\n🎨 Gerando variação {i}/{len(variations)}")

            result = self.generate_image(prompt=full_prompt, **kwargs)
            results.append({
                'variation': variation,
                **result
            })

        return results


# Exemplo de uso
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    # Inicializar gerador
    generator = ImageGenerator()

    # Exemplo 1: Imagem simples
    result = generator.generate_image(
        prompt="Modern luxury apartment interior with ocean view, minimalist design, natural lighting",
        size="1024x1024",
        quality="hd",
        style="vivid",
        save_path="./generated_images/apartment_1.png"
    )

    print(f"\n📊 Resultado: {result}")
