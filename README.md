# Automação de Anúncios: OpenAI + Meta Ads

[![GitHub release](https://img.shields.io/github/v/release/dkbot7/meta-ads-automation-ai)](https://github.com/dkbot7/meta-ads-automation-ai/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![OpenAI](https://img.shields.io/badge/OpenAI-DALL--E%203-412991.svg)](https://openai.com/dall-e-3)
[![Meta API](https://img.shields.io/badge/Meta%20API-v24.0-0668E1.svg)](https://developers.facebook.com/docs/marketing-api)

Sistema completo de automação para geração de imagens com IA (DALL-E 3) e publicação de anúncios na plataforma Meta (Facebook, Instagram, WhatsApp).

## 📋 Sumário

- [Características](#características)
- [Confirmação sobre API Meta](#confirmação-sobre-api-meta)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Uso](#uso)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Exemplos Práticos](#exemplos-práticos)
- [Troubleshooting](#troubleshooting)

## ✨ Características

- ✅ Geração de imagens com DALL-E 3 (OpenAI)
- ✅ Upload automático para biblioteca de anúncios Meta
- ✅ Criação completa de campanhas na Meta
- ✅ Suporte para Facebook, Instagram e WhatsApp
- ✅ Segmentação avançada de público
- ✅ Processamento em lote (múltiplos anúncios)
- ✅ Logs em JSON para auditoria
- ✅ API oficial da Meta (100% legal e suportado)

## 🔍 Confirmação sobre API Meta

**IMPORTANTE:** A afirmação de que "não tem como automatizar via API Meta" está **INCORRETA**.

A Meta possui uma API oficial e completa chamada **Meta Marketing API** (anteriormente Facebook Marketing API) que permite:

- ✅ Criar campanhas programaticamente
- ✅ Gerenciar conjuntos de anúncios
- ✅ Upload de imagens e vídeos
- ✅ Definir segmentação e orçamento
- ✅ Monitorar performance em tempo real
- ✅ Publicar em Facebook, Instagram, Messenger e WhatsApp

**Fontes oficiais:**
- GitHub: github.com/facebook/facebook-python-business-sdk
- Documentação: developers.facebook.com/docs/marketing-apis
- Última atualização da API: v22.0 (2025)

## 📦 Requisitos

### Software
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Conta Meta for Developers
- Conta Meta Ads Manager

### Credenciais Necessárias

#### 1. OpenAI API Key
1. Acesse: https://platform.openai.com/api-keys
2. Crie uma nova API key
3. Copie e guarde com segurança

#### 2. Meta App ID e App Secret
1. Acesse: https://developers.facebook.com/apps
2. Crie um novo aplicativo (tipo "Business")
3. Vá em Configurações > Básico
4. Copie App ID e App Secret

#### 3. Meta Access Token
1. Acesse: https://developers.facebook.com/tools/explorer/
2. Selecione seu aplicativo
3. Adicione permissões: `ads_management`, `business_management`, `pages_read_engagement`
4. Gere o token
5. **IMPORTANTE:** Use a ferramenta de Debug de Token para estender a validade

#### 4. Meta Ad Account ID
1. Acesse: https://business.facebook.com/settings/ad-accounts
2. Copie o ID da conta (formato: `act_123456789`)

#### 5. Meta Page ID (Opcional)
1. Acesse sua página do Facebook
2. Vá em Configurações > Informações da Página
3. Copie o ID da Página

## 🚀 Instalação

### 1. Clone ou baixe o projeto

```bash
cd C:\Users\Vaio\Documents\TRABALHO\CHATBOT_IMOVEIS\PROJETO_CHATBOT_16092025\PROJETO_RESTART\MKT
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Configure as variáveis de ambiente

Copie o arquivo `.env.example` para `.env`:

```bash
copy .env.example .env
```

Edite o arquivo `.env` com suas credenciais:

```env
# OpenAI Configuration
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxx

# Meta/Facebook Configuration
META_APP_ID=1234567890
META_APP_SECRET=abcdef1234567890abcdef1234567890
META_ACCESS_TOKEN=EAAxxxxxxxxxxxxxxxxxxxxxxxxxxxx
META_AD_ACCOUNT_ID=act_1234567890

# Optional: Page ID
META_PAGE_ID=1234567890
```

## 📖 Uso

### Uso Básico

```python
from automation_main import AdAutomation

# Inicializar automação
automation = AdAutomation()

# Criar um anúncio completo
result = automation.create_ad_with_ai_image(
    # Imagem
    image_prompt="Modern luxury apartment with ocean view",
    image_quality="hd",

    # Anúncio
    campaign_name="Campanha Imóveis de Luxo",
    ad_title="Apartamento de Luxo",
    ad_body="Descubra o imóvel dos seus sonhos!",
    link_url="https://www.seusite.com",
    daily_budget=10000,  # R$ 100,00

    # Segmentação
    targeting={
        'geo_locations': {'countries': ['BR']},
        'age_min': 25,
        'age_max': 55
    }
)

print(result)
```

### Executar Exemplos

```bash
python automation_main.py
```

## 📁 Estrutura do Projeto

```
MKT/
│
├── automation_main.py           # Script principal da automação
├── image_generator.py           # Módulo de geração de imagens (OpenAI)
├── meta_ads_manager.py          # Módulo de gerenciamento Meta Ads
│
├── requirements.txt             # Dependências Python
├── .env.example                 # Template de variáveis de ambiente
├── .env                         # Suas credenciais (NÃO COMMITAR)
├── README.md                    # Esta documentação
│
├── generated_images/            # Imagens geradas pela IA
├── logs/                        # Logs JSON das automações
└── .gitignore                   # Arquivos a ignorar no Git
```

## 🎯 Exemplos Práticos

### Exemplo 1: Anúncio Simples

```python
automation = AdAutomation()

result = automation.create_ad_with_ai_image(
    image_prompt="Cozy apartment living room, modern furniture, natural light",
    campaign_name="Apartamentos Aconchegantes",
    ad_title="Seu Novo Lar Espera por Você",
    ad_body="Apartamento moderno e aconchegante. Agende sua visita!",
    link_url="https://exemplo.com/apartamentos",
    daily_budget=5000  # R$ 50,00
)
```

### Exemplo 2: Segmentação Avançada

```python
targeting_avancado = {
    'geo_locations': {
        'countries': ['BR'],
        'regions': [
            {'key': '3450'},  # São Paulo
            {'key': '3462'}   # Rio de Janeiro
        ],
        'cities': [
            {'key': '2490299', 'radius': 25, 'distance_unit': 'kilometer'}
        ]
    },
    'age_min': 30,
    'age_max': 55,
    'genders': [1],  # 1=homens, 2=mulheres
    'interests': [
        {'id': 6003139266461, 'name': 'Real estate'},
        {'id': 6003107902433, 'name': 'Luxury goods'}
    ],
    'life_events': [
        {'id': 6002714398172, 'name': 'Recently moved'}
    ]
}

result = automation.create_ad_with_ai_image(
    image_prompt="Luxury penthouse with city view",
    campaign_name="Coberturas Premium SP/RJ",
    ad_title="Cobertura de Alto Padrão",
    ad_body="Exclusividade e sofisticação. Viva no topo!",
    link_url="https://exemplo.com/coberturas",
    daily_budget=20000,  # R$ 200,00
    targeting=targeting_avancado
)
```

### Exemplo 3: Múltiplos Anúncios em Lote

```python
automation = AdAutomation()

anuncios = [
    {
        'image_prompt': 'Studio apartment, minimalist design',
        'campaign_name': 'Studios Modernos',
        'ad_title': 'Studio no Centro',
        'ad_body': 'Ideal para jovens profissionais',
        'link_url': 'https://exemplo.com/studios',
        'daily_budget': 5000
    },
    {
        'image_prompt': 'Family house with garden',
        'campaign_name': 'Casas Familiares',
        'ad_title': 'Casa para sua Família',
        'ad_body': 'Ampla, segura e confortável',
        'link_url': 'https://exemplo.com/casas',
        'daily_budget': 8000
    }
]

results = automation.create_multiple_ads(anuncios)
```

### Exemplo 4: Usando Apenas Geração de Imagens

```python
from image_generator import ImageGenerator

generator = ImageGenerator()

# Gerar imagem
result = generator.generate_image(
    prompt="Modern kitchen, marble countertop, stainless steel appliances",
    size="1792x1024",
    quality="hd",
    style="natural",
    save_path="./my_images/kitchen.png"
)

print(f"URL: {result['url']}")
print(f"Prompt revisado: {result['revised_prompt']}")
```

### Exemplo 5: Usando Apenas Meta Ads

```python
from meta_ads_manager import MetaAdsManager

manager = MetaAdsManager()

# Criar anúncio com imagem existente
result = manager.create_complete_ad(
    campaign_name="Minha Campanha",
    ad_name="Meu Anúncio",
    image_path="./my_images/existing_image.jpg",
    title="Título do Anúncio",
    body="Texto principal do anúncio",
    link_url="https://exemplo.com",
    daily_budget=5000,
    targeting={'geo_locations': {'countries': ['BR']}}
)
```

## 🔧 Troubleshooting

### Erro: "OPENAI_API_KEY não encontrada"

**Solução:** Verifique se o arquivo `.env` existe e contém a chave correta.

```bash
# Verificar se o arquivo existe
dir .env

# Editar o arquivo
notepad .env
```

### Erro: "Invalid OAuth access token"

**Problema:** Access Token inválido ou expirado.

**Solução:**
1. Gere um novo token em: https://developers.facebook.com/tools/explorer/
2. Use a ferramenta de Debug de Token para estender a validade
3. Atualize o `.env` com o novo token

### Erro: "(#200) Permissions error"

**Problema:** Faltam permissões no token.

**Solução:**
1. No Graph API Explorer, adicione as permissões:
   - `ads_management`
   - `business_management`
   - `pages_read_engagement`
2. Gere um novo token
3. Submeta o app para revisão do Facebook (se necessário)

### Erro: "Ad account not found"

**Problema:** ID da conta de anúncios incorreto.

**Solução:** Verifique se o ID está no formato correto: `act_1234567890`

### Erro: "Image upload failed"

**Problema:** Imagem não encontrada ou formato inválido.

**Solução:**
- Verifique se o caminho da imagem está correto
- Formatos aceitos: JPG, PNG
- Tamanho máximo: 30 MB
- Resolução mínima: 600x600px

### Erro: "Rate limit exceeded"

**Problema:** Muitas requisições em pouco tempo.

**Solução:** Adicione delays entre as chamadas:

```python
import time

for ad in ads_batch:
    result = automation.create_ad_with_ai_image(**ad)
    time.sleep(5)  # Aguardar 5 segundos entre anúncios
```

## 📊 Objetivos de Campanha Disponíveis

- `OUTCOME_TRAFFIC` - Tráfego
- `OUTCOME_ENGAGEMENT` - Engajamento
- `OUTCOME_LEADS` - Leads
- `OUTCOME_SALES` - Vendas
- `OUTCOME_AWARENESS` - Reconhecimento de marca
- `OUTCOME_APP_PROMOTION` - Promoção de app

## 🎨 Tipos de Call-to-Action (CTA)

- `LEARN_MORE` - Saiba mais
- `SHOP_NOW` - Compre agora
- `SIGN_UP` - Cadastre-se
- `DOWNLOAD` - Baixar
- `BOOK_TRAVEL` - Reserve viagem
- `CONTACT_US` - Entre em contato
- `APPLY_NOW` - Candidate-se agora
- `GET_QUOTE` - Solicite orçamento

## 📚 Documentação Oficial

- **Meta Marketing API:** https://developers.facebook.com/docs/marketing-apis
- **Python Business SDK:** https://github.com/facebook/facebook-python-business-sdk
- **OpenAI DALL-E API:** https://platform.openai.com/docs/guides/images
- **Meta Targeting:** https://developers.facebook.com/docs/marketing-api/audiences/reference/targeting

## ⚠️ Avisos Importantes

1. **Custos:** Cada geração de imagem e anúncio gera custos nas respectivas plataformas
2. **Segurança:** NUNCA commite o arquivo `.env` para repositórios públicos
3. **Políticas:** Respeite as políticas de publicidade da Meta e diretrizes da OpenAI
4. **Testes:** Sempre teste com orçamentos baixos antes de escalar
5. **Compliance:** Anúncios de categorias especiais (imóveis, crédito, emprego) têm regras específicas

## 🤝 Suporte

Para dúvidas ou problemas:
1. Consulte esta documentação
2. Verifique os logs em `./logs/`
3. Revise a documentação oficial das APIs
4. Teste com os exemplos fornecidos

## 📝 Licença

Este projeto é fornecido como está para fins educacionais e comerciais.

---

**Desenvolvido com Python | OpenAI DALL-E 3 | Meta Marketing API**

Última atualização: Novembro 2025
