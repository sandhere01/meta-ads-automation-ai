# SOLUÇÃO PARA PROBLEMA DE PÁGINA AUSENTE

## Problemas Identificados

### 1. Permissão Faltando
O token de acesso está **sem a permissão `pages_manage_ads`** que é obrigatória para criar anúncios usando páginas do Facebook.

**Permissões atuais:**
- ✅ ads_management
- ✅ ads_read
- ✅ business_management
- ✅ pages_read_engagement
- ✅ pages_show_list
- ❌ **pages_manage_ads** (FALTANDO!)

### 2. Página ID Incorreta
A página ID `61557902163872` configurada no `.env` **não está acessível** com o token atual.

**Páginas que você TEM acesso:**
1. **Treinamento de I.A. Para Corretores de Imóveis** - ID: `268630006333803`
   - Mais adequada para anúncios de imóveis
   - Tem todas as permissões necessárias (ADVERTISE, MANAGE, etc)

2. **Dani DKbots** - ID: `263636190177579`
   - Alternativa se a primeira não funcionar

3. **Dani Kaloi** - ID: `397671420088892`
   - Outra alternativa

## SOLUÇÃO EM 3 PASSOS

### Passo 1: Atualizar Page ID no .env
Use uma das páginas que você realmente tem acesso. Recomendo:
```
META_PAGE_ID=268630006333803
```
(Página: Treinamento de I.A. Para Corretores de Imóveis)

### Passo 2: Regenerar Token com Permissão pages_manage_ads

#### Opção A: Graph API Explorer (Recomendado)
1. Acesse: https://developers.facebook.com/tools/explorer/
2. Selecione seu App: **3175000345993024**
3. Clique em "Generate Access Token"
4. **IMPORTANTE**: Marque as seguintes permissões:
   - ✅ ads_management
   - ✅ ads_read
   - ✅ business_management
   - ✅ pages_read_engagement
   - ✅ pages_show_list
   - ✅ **pages_manage_ads** ← ESTA É A NOVA!
   - ✅ whatsapp_business_management (se necessário)

5. Clique em "Generate Access Token" e copie o token
6. **IMPORTANTE**: Estenda o token para 60 dias usando o Access Token Debugger:
   - Acesse: https://developers.facebook.com/tools/debug/accesstoken/
   - Cole o token gerado
   - Clique em "Extend Access Token"
   - Copie o token estendido

7. Atualize o `.env` com o novo token:
```
META_ACCESS_TOKEN=<novo_token_estendido_aqui>
```

#### Opção B: Business Manager
1. Acesse: https://business.facebook.com/settings/pages
2. Adicione a página "Treinamento de I.A. Para Corretores de Imóveis" à conta de anúncios
3. Gere um novo token de sistema com as permissões corretas

### Passo 3: Testar Novamente
Depois de atualizar o `.env` com o novo Page ID e o novo token, execute:
```bash
python test_credentials_simple.py
```

Se o teste passar, execute a automação completa:
```bash
python run_automation.py
```

## Verificação Rápida

Você pode verificar se o token tem a permissão correta executando:
```bash
python diagnose_page_permissions.py
```

Na seção "[2] Verificando permissoes do token de acesso...", deve aparecer:
- ✅ pages_manage_ads (na lista de "Permissoes CONCEDIDAS")

## Por que isso aconteceu?

A página ID `61557902163872` provavelmente é:
- De um perfil pessoal (não uma página de negócios)
- De uma conta diferente
- Uma página que foi deletada ou cujas permissões foram revogadas

## Próximos Passos Recomendados

1. ✅ Atualizar `META_PAGE_ID` para `268630006333803` no `.env`
2. ⚠️ Gerar novo token COM a permissão `pages_manage_ads`
3. ✅ Executar diagnóstico novamente para confirmar
4. ✅ Executar automação completa

---

**NOTA IMPORTANTE:**
- Toda vez que você gera um novo token, os tokens anteriores podem ser invalidados
- Certifique-se de estender o token para 60 dias para não precisar regenerar frequentemente
- A permissão `pages_manage_ads` é OBRIGATÓRIA para criar anúncios com páginas do Facebook
