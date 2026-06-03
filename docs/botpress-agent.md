# Agente Conversacional Botpress

## Nome do agente

Retta Tech Assistant

## Objetivo

O agente foi criado para simular um pré-atendimento comercial e técnico de uma empresa de tecnologia B2B.

Ele atua como primeiro ponto de contato para usuários interessados em soluções digitais, identifica a necessidade principal, faz perguntas de qualificação e direciona a demanda para um possível atendimento comercial ou técnico.

## Plataforma utilizada

O agente foi criado e configurado no Botpress, utilizando:

* instruções personalizadas de comportamento;
* base de conhecimento com páginas do site da empresa;
* tabela estruturada de serviços;
* learnings salvos a partir de melhorias nas respostas;
* testes no emulador do Botpress;
* publicação do agente;
* integração via Botpress Chat API.

## Escopo de atendimento

O agente atua nos seguintes temas:

* Desenvolvimento de software sob medida
* Manutenção e modernização de sistemas legados
* Outsourcing de TI
* Inteligência artificial aplicada a processos
* Automações
* Chatbots, agentes inteligentes e RAG
* Encaminhamento para atendimento comercial

## Fluxo conversacional

O fluxo do agente segue uma abordagem progressiva e consultiva:

1. O usuário inicia a conversa.
2. O agente se apresenta e mostra as opções de atendimento.
3. O usuário informa sua necessidade.
4. O agente identifica a intenção principal.
5. O agente faz perguntas de qualificação.
6. O agente coleta informações gradualmente.
7. O agente direciona a demanda para avaliação comercial ou técnica.
8. Caso não entenda a mensagem, utiliza um fallback curto e objetivo.

## Intenções tratadas

### Saudação

Quando o usuário inicia a conversa com uma saudação, o agente se apresenta como Retta Tech Assistant e exibe as opções principais de atendimento.

Exemplo de entrada:

```txt
Olá
```

Comportamento esperado:

```txt
Olá! Sou o Retta Tech Assistant, assistente comercial técnico para soluções de tecnologia.

Posso te ajudar com:

1. Desenvolvimento de software sob medida
2. Manutenção ou modernização de sistemas legados
3. Outsourcing de TI
4. Inteligência artificial aplicada a processos
5. Chatbots, agentes inteligentes e RAG
6. Falar com o comercial

Me diga qual opção faz mais sentido para sua necessidade.
```

### Chatbots e agentes inteligentes

Quando o usuário demonstra interesse em criar um chatbot ou agente inteligente, o agente faz perguntas progressivas sobre objetivo, canal, público, base de conhecimento, integrações e necessidade de encaminhamento humano.

Exemplo de entrada:

```txt
Quero criar um chatbot para atendimento
```

Comportamento esperado:

```txt
Ótimo! Podemos ajudar sua empresa a estruturar um chatbot para atendimento.

Para começar, esse chatbot seria voltado para atendimento ao cliente, suporte interno, vendas ou outro tipo de uso?
```

### Sistemas legados

Quando o usuário menciona modernização de sistema legado, o agente investiga a dor principal antes de pedir detalhes técnicos.

Exemplo de entrada:

```txt
Tenho um sistema legado e quero modernizar
```

Comportamento esperado:

```txt
Entendi. Modernizar sistemas legados pode envolver manutenção, performance, segurança, integrações ou evolução de funcionalidades.

Para começar, qual é a principal dificuldade que vocês enfrentam hoje com esse sistema?
```

### Inteligência artificial

Quando o usuário pergunta sobre inteligência artificial, o agente explica aplicações possíveis e faz uma pergunta de qualificação.

Exemplo de entrada:

```txt
Vocês trabalham com inteligência artificial?
```

Comportamento esperado:

```txt
Sim, trabalhamos com inteligência artificial aplicada a processos reais da empresa.

Podemos apoiar em automações, agentes inteligentes, chatbots, soluções com RAG para consulta a documentos, integração com sistemas internos e análise de dados.

Para entender melhor: você está pensando em usar IA para atendimento ao cliente, automação interna, análise de documentos, suporte ao time ou outro processo?
```

### Fora do escopo

Quando o usuário pergunta sobre algo fora da atuação da empresa, o agente responde de forma educada e redireciona para os serviços corretos.

Exemplo de entrada:

```txt
Vocês vendem celular?
```

Comportamento esperado:

```txt
Atualmente não trabalhamos com venda de celulares ou dispositivos físicos.

Nosso foco é apoiar empresas com desenvolvimento de software, modernização de sistemas, outsourcing de TI, automação e soluções com inteligência artificial.

Posso te ajudar com alguma dessas opções?

1. Software sob medida
2. Sistemas legados
3. Outsourcing de TI
4. IA e automação
5. Chatbots ou agentes inteligentes
6. Falar com o comercial
```

### Fallback

Quando o usuário envia uma mensagem sem sentido, caracteres aleatórios ou algo impossível de interpretar, o agente não reinicia toda a conversa. Ele utiliza um fallback curto.

Exemplo de entrada:

```txt
asdkjbsa2
```

Comportamento esperado:

```txt
Não consegui entender sua mensagem. Você pode reformular ou escolher uma destas opções?

1. Software sob medida
2. Sistemas legados
3. Outsourcing de TI
4. IA e automação
5. Chatbots ou agentes inteligentes
6. Falar com o comercial
```

## Base de conhecimento

O agente utiliza uma base de conhecimento composta por:

* páginas públicas do site da empresa;
* tabela estruturada de serviços;
* perguntas de qualificação por tipo de demanda.

A tabela de serviços foi criada para ajudar o agente a classificar melhor as demandas e responder de forma mais alinhada ao contexto da empresa.

## Tabela de serviços

A tabela estruturada contém serviços, descrições e perguntas de qualificação.

Exemplos de categorias cadastradas:

* Software sob medida
* Sistemas legados
* Outsourcing de TI
* Inteligência artificial e automação
* Chatbots, agentes inteligentes e RAG
* Integrações e automações

## Dados coletados

Quando adequado, o agente pode solicitar:

* Nome
* Empresa
* E-mail profissional
* WhatsApp
* Tipo de necessidade
* Descrição resumida do problema
* Urgência ou prazo desejado
* Sistemas ou tecnologias envolvidas

A coleta deve ser gradual, evitando solicitar todos os dados logo no início da conversa.

## Integração com o middleware

O middleware recebe mensagens externas via Z-API ou Evolution API, normaliza o payload e encaminha a mensagem para o Botpress por meio da Chat API.

Depois que o Botpress retorna a resposta do agente, o middleware envia essa resposta novamente ao usuário final pelo provedor de mensageria configurado.

## Fluxo técnico

```txt
Z-API / Evolution API
→ Middleware FastAPI
→ Botpress Chat API
→ Middleware FastAPI
→ Z-API / Evolution API
```

## Validação realizada

O agente foi testado no emulador do Botpress com cenários como:

* saudação inicial;
* interesse em chatbot;
* modernização de sistema legado;
* inteligência artificial;
* pergunta fora do escopo;
* fallback para mensagem incompreensível.

Além disso, o middleware foi testado chamando a Botpress Chat API e recebendo uma resposta real do agente.

## Observações

Esta versão representa um MVP funcional do agente conversacional para o desafio técnico.

Melhorias futuras podem incluir:

* coleta estruturada de leads;
* integração com CRM;
* integração com planilha;
* armazenamento de histórico de conversa;
* fallback com classificação mais refinada;
* métricas de intenção e conversão.
