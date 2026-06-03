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

MESSAGING_PROVIDER=zapi

ZAPI_INSTANCE_ID=
ZAPI_TOKEN=
ZAPI_CLIENT_TOKEN=

EVOLUTION_BASE_URL=
EVOLUTION_INSTANCE_NAME=
EVOLUTION_API_KEY=

BOTEXPRESS_BASE_URL=
BOTEXPRESS_API_KEY=
BOTEXPRESS_BOT_ID=

REQUEST_TIMEOUT=10
```

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

A aplicação foi construída com foco em desacoplamento.

A camada `providers` permite trocar o provedor externo de mensageria sem alterar a regra principal da aplicação.

A camada `services` concentra integrações e regras auxiliares, como comunicação com BotExpress, normalização de payloads e idempotência.

A camada `schemas` define modelos normalizados para entrada, saída e resposta do bot.

A camada `exceptions` padroniza os erros retornados pela API.

## Observações

A integração com o BotExpress está isolada no arquivo `botexpress_service.py`. Caso o endpoint, autenticação ou formato de payload do BotExpress seja diferente no ambiente real, o ajuste fica concentrado nessa camada.

## Melhorias futuras

* Persistência de conversas em PostgreSQL
* Redis para idempotência e controle de sessão
* Rate limiting
* Autenticação no webhook
* Testes com mock de APIs externas
* Deploy em cloud
* Observabilidade com Grafana
* Pipeline CI/CD com GitHub Actions
