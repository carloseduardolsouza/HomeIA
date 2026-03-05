# HomeIA

![Build](https://img.shields.io/github/actions/workflow/status/SEU_USUARIO/HomeIA/ci.yml?branch=main&label=build)
![Version](https://img.shields.io/badge/version-0.1.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

HomeIA e uma plataforma de IA preditiva e generativa para monitoramento residencial com sensores IoT, automacao e analise inteligente.  
O projeto integra ingestao de dados em tempo real, modelos de inferencia e servicos de alerta para decisao operacional.  
A arquitetura combina microsservicos, infraestrutura observavel e componentes de LLM/visao computacional.  
Este repositorio concentra codigo, infraestrutura e documentacao para evolucao incremental por entregas.

## Pre-requisitos

- Docker e Docker Compose
- Python 3.11+
- Node.js 20+
- Git

## Instalacao Local

1. Clone o repositorio.
2. Copie `.env.example` para `.env` e preencha os valores necessarios.
3. Instale hooks de desenvolvimento: `pip install pre-commit && pre-commit install`.
4. Suba a stack local: `bash infra/scripts/setup.sh`.
5. Rode verificacoes locais: `pre-commit run --all-files`.

## Modulos

| Modulo              | Descricao                                 | Status          |
| ------------------- | ----------------------------------------- | --------------- |
| Gateway IoT         | Ingestao e validacao de dados de sensores | ⏳ planejado    |
| Inference Engine    | Predicao, anomalias e jobs de ML          | ⏳ planejado    |
| Alert Service       | Alertas e notificacoes (Telegram)         | ⏳ planejado    |
| LLM Service         | Orquestracao de agente com modelo local   | ⏳ planejado    |
| Vision Service      | Deteccao em cameras e eventos             | ⏳ planejado    |
| Infraestrutura Base | Docker, observabilidade e mensageria      | 🔄 em progresso |

## Documentacao

A documentacao completa esta em [`docs/`](docs/).

## Board de Tarefas

Defina o board oficial do time aqui: `https://github.com/SEU_USUARIO/HomeIA/projects`.
