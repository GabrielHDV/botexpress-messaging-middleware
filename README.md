# Botpress Messaging Middleware

Middleware para integração entre agentes conversacionais criados no Botpress e provedores de mensageria como Z-API e Evolution API.

## Objetivo

O objetivo deste projeto é receber mensagens por webhook, encaminhá-las para um agente conversacional no Botpress e retornar a resposta ao usuário final por meio de um provedor externo de mensageria.

A aplicação foi construída com foco em organização, desacoplamento, segurança de credenciais, tratamento de exceções e facilidade de manutenção.

## Arquitetura

```txt
Canal de mensagem
→ Z-API / Evolution API
→ FastAPI Middleware
→ Botpress Chat API
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
* Botpress Chat API
* Z-API
* Evolution API

## Funcionalidades

* Recebimento de mensagens via webhook
* Normalização de payloads de diferentes provedores
* Integração com agente conversacional Botpress via Chat API
* Envio de respostas por provedor configurável
* Suporte inicial para Z-API e Evolution API
* Seleção dinâmica de provedor via variável de ambiente
* Cache do provider com `lru_cache`
* Injeção de dependência com `Depends`
* Autenticação simples dos webhooks com `X-Webhook-Secret`
* Logs estruturados
* Mascaramento de telefone em logs
* Tratamento centralizado de exceções
* Controle simples de idempotência
* Testes básicos
* Suporte a Docker

## Agente conversacional

O agente conversacional foi criado no Botpress com o nome **Retta Tech Assistant**.

Ele simula um pré-atendimento comercial e técnico para uma empresa de tecnologia B2B, utilizando instruções personalizadas, base de conhecimento com páginas do site da empresa, tabela estruturada de serviços e learnings salvos a partir dos testes no emulador.

A documentação completa do agente está disponível em:

```txt
docs/botpress-agent.md
```

## Estrutura do projeto

```txt
app/
├── api/
│   └── routes/
│       └── webhook.py
├── core/
│   ├── auth.py
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
│   ├── botpress_service.py
│   ├── idempotency_service.py
│   └── payload_parser.py
└── main.py
```

## Como executar localmente

Clone o repositório:

```bash
git clone https://github.com/GabrielHDV/botpress-messaging-middleware.git
cd botpress-messaging-middleware
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

Exemplo de payload textual:

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

Exemplo de payload textual:

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
APP_NAME=Botpress Messaging Middleware

WEBHOOK_SECRET=change-me

MESSAGING_PROVIDER=zapi

ZAPI_INSTANCE_ID=
ZAPI_TOKEN=
ZAPI_CLIENT_TOKEN=

EVOLUTION_BASE_URL=
EVOLUTION_INSTANCE_NAME=
EVOLUTION_API_KEY=

BOTPRESS_WEBHOOK_ID=
BOTPRESS_POLLING_ATTEMPTS=8
BOTPRESS_POLLING_INTERVAL=1

REQUEST_TIMEOUT=10
```

## Autenticação dos webhooks

Os endpoints de webhook utilizam autenticação simples baseada no header:

```http
X-Webhook-Secret: change-me
```

Quando a variável `WEBHOOK_SECRET` está configurada, todas as chamadas aos webhooks precisam enviar o mesmo valor no header `X-Webhook-Secret`.

Também é possível enviar o segredo por query param em cenários onde o provedor de webhook não permite configurar headers customizados:

```txt
/webhooks/zapi?secret=change-me
```

Caso o segredo esteja ausente ou incorreto, a API retorna:

```json
{
  "error": "http_error",
  "message": "Webhook secret inválido ou ausente"
}
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

A seleção do provedor utiliza `lru_cache` e injeção de dependência com `Depends`, evitando recriação desnecessária da instância do provider a cada requisição.

## Integração com Botpress

A integração com o agente conversacional foi implementada utilizando a Botpress Chat API.

O middleware recebe a mensagem enviada pelo usuário, normaliza o payload recebido da Z-API ou Evolution API e encaminha essa mensagem para o agente configurado no Botpress.

As configurações da integração são definidas por variáveis de ambiente:

```env
BOTPRESS_WEBHOOK_ID=
BOTPRESS_POLLING_ATTEMPTS=8
BOTPRESS_POLLING_INTERVAL=1
```

O `BOTPRESS_WEBHOOK_ID` representa o identificador da integração Chat do Botpress, utilizado para comunicação com a Chat API.

O fluxo básico da integração é:

```txt
1. Criar usuário no Botpress
2. Criar ou recuperar conversa
3. Enviar mensagem do usuário para o agente
4. Aguardar a resposta do agente
5. Retornar a resposta para o middleware
6. Enviar a resposta ao usuário final pelo provedor configurado
```

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

A camada `core` concentra configurações, autenticação simples de webhook, logger e utilitários de segurança.

A camada `providers` concentra as integrações com provedores externos de mensageria, como Z-API e Evolution API.

A camada `services` concentra integrações e regras auxiliares, como comunicação com Botpress, normalização de payloads e controle de idempotência.

A camada `schemas` define modelos normalizados para entrada, saída e resposta do bot.

A camada `exceptions` padroniza os erros retornados pela API.

## Limitações conhecidas

Esta versão representa um MVP técnico do middleware e possui algumas limitações conhecidas.

### Idempotência

O controle de idempotência utiliza Redis com TTL de 24 horas, garantindo que mensagens duplicadas sejam descartadas mesmo em caso de reinício da aplicação.

Em ambiente com múltiplas instâncias, o Redis centralizado mantém o estado compartilhado entre os processos.


### Integração com Botpress

A integração com o Botpress utiliza a Chat API e depende do Webhook ID da integração Chat configurada na plataforma.

A versão atual se comunica com o agente e recebe respostas reais, mas ainda não persiste dados como `x-user-key`, histórico de conversa ou informações de sessão.

Em produção, recomenda-se persistir esses dados em banco de dados ou Redis para manter continuidade de conversas e evitar recriações desnecessárias de usuários.

### Tipos de mensagem

O middleware atualmente processa apenas mensagens textuais.

Mensagens de áudio, imagem, documento, vídeo ou outros tipos de mídia não fazem parte do escopo inicial desta versão.

Em uma versão de produção, esses tipos devem ser tratados explicitamente, com download de mídia, transcrição de áudio, OCR de imagens ou resposta controlada informando que o tipo de mensagem não é suportado.

### Rate limiting

A aplicação ainda não possui rate limiting.

Em ambiente produtivo, recomenda-se utilizar API Gateway, proxy reverso ou middleware específico para limitar requisições e reduzir risco de flood.

### Escalabilidade

A aplicação foi estruturada em camadas para facilitar evolução, mas recursos como fila, Redis, persistência de conversas e observabilidade ainda estão listados como melhorias futuras.

## Melhorias futuras

* Persistência de conversas em PostgreSQL
* Redis para idempotência e controle de sessão
* Persistência de `x-user-key` do Botpress
* Rate limiting
* Testes com mock de APIs externas
* Deploy em cloud
* Observabilidade com Grafana
* Pipeline CI/CD com GitHub Actions

