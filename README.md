# BotExpress Messaging Middleware

Middleware para integração entre agentes conversacionais criados no BotExpress e provedores de mensageria como Z-API e Evolution API.

## Objetivo

O objetivo deste projeto é receber mensagens por webhook, encaminhá-las para um agente conversacional no BotExpress e retornar a resposta ao usuário final por meio de um provedor externo de mensageria.

A aplicação foi construída com foco em organização, desacoplamento, tratamento de exceções, segurança de credenciais e facilidade de manutenção.

## Arquitetura

```txt
Canal de mensagem
→ Z-API / Evolution API
→ FastAPI Middleware
→ BotExpress
→ FastAPI Middleware
→ Z-API / Evolution API
→ Usuário final
```

## Tecnologias utilizadas

* Python
* FastAPI
* Pydantic
* HTTPX
* Uvicorn
* Docker
* Docker Compose
* Pytest
* Z-API
* Evolution API

## Funcionalidades

* Recebimento de mensagens via webhook
* Normalização de payloads de diferentes provedores
* Integração com agente conversacional BotExpress
* Envio de respostas por provedor configurável
* Suporte inicial para Z-API
* Suporte inicial para Evolution API
* Seleção dinâmica de provedor via variável de ambiente
* Logs estruturados
* Mascaramento de telefone em logs
* Tratamento centralizado de exceções
* Controle simples de idempotência
* Testes básicos
* Suporte a Docker

## Estrutura do projeto

```txt
app/
├── api/
│   └── routes/
│       └── webhook.py
├── core/
│   ├── config.py
│   ├── logger.py
│   └── security.py
├── exceptions/
│   └── handlers.py
├── providers/
│   ├── base.py
│   ├── evolution.py
│   ├── factory.py
│   └── zapi.py
├── schemas/
│   └── message.py
├── services/
│   ├── botexpress_service.py
│   ├── idempotency_service.py
│   └── payload_parser.py
└── main.py
```

## Como executar localmente

Clone o repositório:

```bash
git clone https://github.com/GabrielHDV/botexpress-messaging-middleware.git
cd botexpress-messaging-middleware
```

Crie e ative o ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Crie o arquivo de ambiente:

```bash
cp .env.example .env
```

Execute a aplicação:

```bash
uvicorn app.main:app --reload
```

Acesse a documentação da API:

```txt
http://localhost:8000/docs
```

## Como executar com Docker

Crie o arquivo de ambiente:

```bash
cp .env.example .env
```

Suba a aplicação:

```bash
docker compose up --build
```

Acesse:

```txt
http://localhost:8001/health
```

## Endpoints

### Health Check

```http
GET /health
```

Resposta esperada:

```json
{
  "status": "ok",
  "environment": "development"
}
```

### Webhook Z-API

```http
POST /webhooks/zapi
```

Exemplo de payload:

```json
{
  "phone": "5535999999999",
  "text": {
    "message": "Olá"
  },
  "messageId": "abc123",
  "senderName": "Gabriel"
}
```

### Webhook Evolution API

```http
POST /webhooks/evolution
```

Exemplo de payload:

```json
{
  "data": {
    "key": {
      "remoteJid": "5535999999999@s.whatsapp.net",
      "id": "msg123"
    },
    "message": {
      "conversation": "Olá"
    },
    "pushName": "Gabriel"
  }
}
```

## Variáveis de ambiente

```env
ENVIRONMENT=development
APP_NAME=BotExpress Messaging Middleware

WEBHOOK_SECRET=change-me

MESSAGING_PROVIDER=zapi

ZAPI_INSTANCE_ID=
ZAPI_TOKEN=
ZAPI_CLIENT_TOKEN=

EVOLUTION_BASE_URL=
EVOLUTION_INSTANCE_NAME=
EVOLUTION_API_KEY=

BOTEXPRESS_BASE_URL=
BOTEXPRESS_API_KEY=
BOTEXPRESS_ENDPOINT_PATH=
BOTEXPRESS_AUTH_HEADER=Authorization
BOTEXPRESS_AUTH_SCHEME=Bearer

REQUEST_TIMEOUT=10
```

## Autenticação dos webhooks

Os endpoints de webhook utilizam uma autenticação simples baseada no header:

```http
X-Webhook-Secret: change-me
```

Quando a variável `WEBHOOK_SECRET` está configurada, todas as chamadas aos webhooks precisam enviar o mesmo valor no header `X-Webhook-Secret`.

Caso o header esteja ausente ou incorreto, a API retorna:

```json
{
  "error": "http_error",
  "message": "Webhook secret inválido ou ausente"
}
```

Essa abordagem reduz o risco de chamadas não autorizadas aos endpoints públicos do middleware.

## Adapter BotExpress

A integração com o BotExpress foi implementada como um adapter configurável.

As informações de endpoint, autenticação e caminho da API são definidas por variáveis de ambiente:

```env
BOTEXPRESS_BASE_URL=
BOTEXPRESS_API_KEY=
BOTEXPRESS_ENDPOINT_PATH=
BOTEXPRESS_AUTH_HEADER=Authorization
BOTEXPRESS_AUTH_SCHEME=Bearer
```

Essa decisão evita acoplamento com um endpoint fixo e permite ajustar a integração conforme a documentação oficial, credenciais ou ambiente real disponibilizado para o desafio.

## Escopo de mensagens

Esta versão do middleware processa apenas mensagens textuais.

Payloads contendo mídia, como imagem, áudio, vídeo, documento, figurinha, localização ou contato, retornam:

```json
{
  "error": "http_error",
  "message": "Tipo de mensagem não suportado nesta versão. O middleware processa apenas mensagens textuais."
}
```

Essa decisão mantém o escopo inicial objetivo e evita processamentos incompletos de mídia sem tratamento adequado.

## Seleção de provedor

O provedor de mensageria é definido pela variável:

```env
MESSAGING_PROVIDER=zapi
```

Valores suportados inicialmente:

```txt
zapi
evolution
```

A seleção do provedor utiliza cache com `lru_cache` e injeção de dependência com `Depends`, evitando recriação desnecessária do provider a cada requisição.


## Seleção de provedor

O provedor de mensageria é definido pela variável:

```env
MESSAGING_PROVIDER=zapi
```

Valores suportados inicialmente:

```txt
zapi
evolution
```

## Segurança

O projeto adota algumas práticas básicas de segurança:

* Credenciais armazenadas em variáveis de ambiente
* Arquivo `.env` ignorado pelo Git
* Mascaramento de telefone em logs
* Timeout em chamadas externas
* Tratamento padronizado de erros
* Separação entre rotas, serviços e provedores

## Tratamento de erros

A aplicação possui handlers globais para:

* Erros HTTP
* Erros de validação
* Falhas em serviços externos
* Erros de configuração
* Erros inesperados

Exemplo de erro para payload inválido:

```json
{
  "error": "http_error",
  "message": "Payload inválido da Z-API: phone e text são obrigatórios"
}
```

## Testes

Execute os testes com:

```bash
pytest -q
```

## Decisões técnicas

A aplicação foi construída com foco em desacoplamento e evolução gradual.

A camada `api` concentra as rotas HTTP e webhooks.

A camada `providers` concentra as integrações com provedores externos de mensageria, como Z-API e Evolution API.

A camada `services` concentra integrações e regras auxiliares, como comunicação com BotExpress, normalização de payloads e controle de idempotência.

A camada `schemas` define modelos normalizados para entrada, saída e resposta do bot.

A camada `exceptions` padroniza os erros retornados pela API.

A camada `core` concentra configurações, autenticação simples de webhook, logger e utilitários de segurança.

O projeto utiliza `Depends` do FastAPI para injetar o provedor de mensageria nas rotas, e `lru_cache` para evitar recriações desnecessárias da instância do provider.

A integração com o BotExpress foi mantida como adapter configurável, permitindo ajuste do endpoint e do formato de autenticação conforme o ambiente real.

## Observações

A integração com o BotExpress está isolada no arquivo `botexpress_service.py`. Caso o endpoint, autenticação ou formato de payload do BotExpress seja diferente no ambiente real, o ajuste fica concentrado nessa camada.

## Limitações conhecidas

Esta versão representa um MVP técnico do middleware e possui algumas limitações conhecidas:

### Idempotência

O controle de idempotência atual utiliza armazenamento em memória por meio de um `set` global.

Essa abordagem funciona para demonstração local, mas não é adequada para produção, pois os dados são perdidos em caso de reinício da aplicação, novo deploy, crash ou execução em múltiplas instâncias.

Em produção, recomenda-se substituir essa implementação por Redis com TTL ou banco de dados.

### Integração com BotExpress

A integração com o BotExpress foi isolada na camada `BotExpressService`.

O endpoint utilizado nessa camada deve ser validado e ajustado conforme a documentação oficial ou as credenciais fornecidas no ambiente real do desafio.

Essa decisão foi tomada para manter a arquitetura desacoplada e permitir que alterações no formato de autenticação, endpoint ou payload fiquem concentradas em um único arquivo.

### Tipos de mensagem

O middleware atualmente processa apenas mensagens textuais.

Mensagens de áudio, imagem, documento, vídeo ou outros tipos de mídia não fazem parte do escopo inicial desta versão.

Em uma versão de produção, esses tipos devem ser tratados explicitamente, com download de mídia, transcrição de áudio, OCR de imagens ou resposta controlada informando que o tipo de mensagem não é suportado.

### Segurança do webhook

A versão inicial ainda não possui validação de segredo no webhook.

Em produção, recomenda-se validar um token enviado no header da requisição, como `X-Webhook-Secret`, para evitar chamadas não autorizadas ao endpoint.

### Rate limiting

A aplicação ainda não possui rate limiting.

Em ambiente produtivo, recomenda-se utilizar API Gateway, proxy reverso ou middleware específico para limitar requisições e reduzir risco de flood.

### Escalabilidade

A aplicação foi estruturada em camadas para facilitar evolução, mas recursos como fila, Redis, persistência de conversas e observabilidade ainda estão listados como melhorias futuras.

## Melhorias futuras

* Persistência de conversas em PostgreSQL
* Redis para idempotência e controle de sessão
* Rate limiting
* Autenticação no webhook
* Testes com mock de APIs externas
* Deploy em cloud
* Observabilidade com Grafana
* Pipeline CI/CD com GitHub Actions
