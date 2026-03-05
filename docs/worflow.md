# 🚀 Plano de Entregas — IA Preditiva & Generativa

> Baseado na Documentação Técnica v1.0 | Março 2026

---

## Índice

1. [Entrega 01 — Setup do Repositório e Estrutura do Projeto](#entrega-01)
2. [Entrega 02 — Infraestrutura Base com Docker](#entrega-02)
3. [Entrega 03 — Pipeline de Ingestão de Dados IoT](#entrega-03)
4. [Entrega 04 — Módulo de Energia (M-01) — Coleta e Armazenamento](#entrega-04)
5. [Entrega 05 — Módulo de Energia (M-01) — Modelo Preditivo](#entrega-05)
6. [Entrega 06 — Módulo de Irrigação (M-03) — Sensores e Automação](#entrega-06)
7. [Entrega 07 — Módulo de Servidor (M-05) — Monitoramento e Alertas](#entrega-07)
8. [Entrega 08 — Módulo de Equipamentos (M-02) — Detecção de Anomalia](#entrega-08)
9. [Entrega 09 — Módulo de Casa Inteligente (M-04) — Home Assistant + LLM](#entrega-09)
10. [Entrega 10 — Módulo de Câmeras (M-06) — Visão Computacional](#entrega-10)

---

## Convenções deste documento

| Símbolo | Significado                         |
| ------- | ----------------------------------- |
| ✅      | Critério de aceite obrigatório      |
| 📁      | Arquivo ou pasta a ser criado       |
| 📄      | Documento a ser entregue            |
| 🔧      | Configuração técnica obrigatória    |
| ⚠️      | Dependência ou restrição importante |

---

---

## Entrega 01

# 📦 Setup do Repositório e Estrutura do Projeto

**Fase:** 1 | **Sprint:** 1 | **Estimativa:** 3–5 dias  
**Responsável:** Tech Lead / Arquiteto  
**Módulos relacionados:** Todos

### Objetivo

Criar a base de trabalho do projeto: repositório Git, estrutura de pastas, padrões de código, configuração de ambiente de desenvolvimento e documentação inicial. Esta entrega não possui código funcional de IA, mas é o alicerce de tudo que vem depois.

---

### 1.1 Estrutura de Pastas Obrigatória

```
ia-preditiva-generativa/
│
├── 📄 README.md                    # Visão geral, como rodar, links
├── 📄 CONTRIBUTING.md              # Guia de contribuição e padrões
├── 📄 CHANGELOG.md                 # Histórico de versões
├── 📄 .gitignore                   # Node, Python, .env, __pycache__
├── 📄 .env.example                 # Variáveis de ambiente documentadas
│
├── 📁 docs/                        # Toda documentação do projeto
│   ├── 📄 arquitetura.md           # Diagrama de fluxo e decisões técnicas
│   ├── 📄 stack.md                 # Justificativas de cada tecnologia
│   ├── 📄 adr/                     # Architecture Decision Records
│   │   └── ADR-001-escolha-influxdb.md
│   └── 📄 glossario.md             # Termos técnicos do projeto
│
├── 📁 infra/                       # Infraestrutura e DevOps
│   ├── 📁 docker/                  # Dockerfiles por serviço
│   ├── 📁 compose/                 # docker-compose por ambiente
│   │   ├── docker-compose.dev.yml
│   │   ├── docker-compose.prod.yml
│   │   └── docker-compose.test.yml
│   └── 📁 scripts/                 # Scripts de setup e utilitários
│       ├── setup.sh
│       └── teardown.sh
│
├── 📁 services/                    # Microsserviços do sistema
│   ├── 📁 gateway-iot/             # Ingestão de dados dos sensores
│   ├── 📁 inference-engine/        # Motor de ML / inferência
│   ├── 📁 alert-service/           # Serviço de alertas e notificações
│   ├── 📁 llm-service/             # LLM local com Ollama + LangChain
│   └── 📁 vision-service/          # Visão computacional com YOLO
│
├── 📁 firmware/                    # Código para ESP32 / Arduino
│   ├── 📁 esp32-energia/
│   ├── 📁 esp32-irrigacao/
│   └── 📁 esp32-sensores/
│
├── 📁 models/                      # Modelos de ML versionados
│   ├── 📁 energia/
│   ├── 📁 equipamentos/
│   ├── 📁 irrigacao/
│   └── 📁 servidor/
│
├── 📁 notebooks/                   # Jupyter Notebooks de exploração
│   ├── 📁 eda/                     # Análise exploratória de dados
│   ├── 📁 treinamento/             # Notebooks de treino dos modelos
│   └── 📁 experimentos/            # Experimentos e prototipagem
│
├── 📁 dashboard/                   # Frontend React
│
└── 📁 tests/                       # Testes automatizados
    ├── 📁 unit/
    ├── 📁 integration/
    └── 📁 e2e/
```

---

### 1.2 Documentos Obrigatórios

#### `README.md` deve conter:

- Descrição do projeto em 3–5 linhas
- Badges: build status, versão, licença
- Pré-requisitos (Docker, Python 3.11+, Node 20+)
- Guia de instalação local em menos de 5 passos
- Tabela de módulos com status atual (✅ pronto | 🔄 em progresso | ⏳ planejado)
- Link para documentação completa em `/docs`
- Link para o board de tarefas (Jira / Linear / GitHub Projects)

#### `.env.example` deve conter:

```env
# === MQTT ===
MQTT_HOST=localhost
MQTT_PORT=1883
MQTT_USER=
MQTT_PASSWORD=

# === InfluxDB ===
INFLUXDB_URL=http://localhost:8086
INFLUXDB_TOKEN=
INFLUXDB_ORG=ia-preditiva
INFLUXDB_BUCKET=sensores

# === PostgreSQL ===
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=ia_preditiva
POSTGRES_USER=
POSTGRES_PASSWORD=

# === Redis ===
REDIS_HOST=localhost
REDIS_PORT=6379

# === Telegram ===
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=

# === MLflow ===
MLFLOW_TRACKING_URI=http://localhost:5000

# === Ollama ===
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3
```

#### `CONTRIBUTING.md` deve conter:

- Padrão de branches: `feature/`, `fix/`, `chore/`, `docs/`
- Padrão de commits (Conventional Commits): `feat:`, `fix:`, `docs:`, `test:`
- Como abrir Pull Request
- Checklist de PR (testes passando, lint, documentação atualizada)
- Padrão de nomenclatura de variáveis e funções (snake_case Python, camelCase JS)

---

### 1.3 Configurações de Código

#### `.gitignore` deve incluir:

```
# Python
__pycache__/
*.pyc
.venv/
*.egg-info/

# Ambiente
.env
*.env.local

# Dados e modelos
*.pkl
*.h5
*.pt
*.onnx
data/raw/
data/processed/

# Notebooks
.ipynb_checkpoints/

# IDEs
.vscode/
.idea/

# Docker
*.log
```

#### Configurar `pre-commit` com:

- `black` — formatação Python
- `flake8` — linting Python
- `eslint` — linting JavaScript
- `prettier` — formatação JavaScript/CSS
- Checagem de secrets (prevent commit de `.env` real)

---

### 1.4 Critérios de Aceite

| #    | Critério                                                    | Validação                              |
| ---- | ----------------------------------------------------------- | -------------------------------------- |
| ✅ 1 | Repositório criado com todas as pastas listadas             | `ls` na raiz mostra estrutura completa |
| ✅ 2 | `README.md` com todos os itens da seção 1.2                 | Revisão manual                         |
| ✅ 3 | `.env.example` com todas as variáveis documentadas          | Revisão manual                         |
| ✅ 4 | `.gitignore` configurado (sem `.env` real commitado)        | `git status` limpo                     |
| ✅ 5 | `pre-commit` instalado e funcionando                        | `pre-commit run --all-files` sem erros |
| ✅ 6 | `CONTRIBUTING.md` com guia de branches e commits            | Revisão manual                         |
| ✅ 7 | Pelo menos 1 ADR criado (escolha do banco de dados)         | Arquivo em `docs/adr/`                 |
| ✅ 8 | Pipeline CI básico configurado (GitHub Actions / GitLab CI) | Push dispara lint e testes             |

---

---

## Entrega 02

# 🐳 Infraestrutura Base com Docker

**Fase:** 1 | **Sprint:** 1–2 | **Estimativa:** 5–7 dias  
**Responsável:** DevOps / Backend  
**Módulos relacionados:** Todos  
**Dependência:** Entrega 01 concluída

### Objetivo

Levantar toda a infraestrutura de suporte do sistema usando Docker Compose: broker MQTT, bancos de dados, cache, ferramentas de observabilidade e monitoramento. Ao final desta entrega, todos os serviços de infraestrutura devem estar rodando localmente e prontos para receber dados.

---

### 2.1 Serviços a Serem Containerizados

| Serviço          | Imagem Docker           | Porta      | Propósito                  |
| ---------------- | ----------------------- | ---------- | -------------------------- |
| Mosquitto (MQTT) | `eclipse-mosquitto:2`   | 1883, 9001 | Broker de mensagens IoT    |
| InfluxDB         | `influxdb:2.7`          | 8086       | Time-series de sensores    |
| PostgreSQL       | `postgres:16`           | 5432       | Dados relacionais          |
| Redis            | `redis:7-alpine`        | 6379       | Cache e filas              |
| Grafana          | `grafana/grafana:10`    | 3000       | Dashboards                 |
| Prometheus       | `prom/prometheus:v2`    | 9090       | Métricas dos serviços      |
| MLflow           | `ghcr.io/mlflow/mlflow` | 5000       | Tracking de modelos        |
| MinIO            | `minio/minio:latest`    | 9000, 9001 | Armazenamento de objetos   |
| Node-RED         | `nodered/node-red:3`    | 1880       | Orquestração de fluxos IoT |

---

### 2.2 Arquivos de Configuração Obrigatórios

#### `infra/compose/docker-compose.dev.yml` — estrutura mínima:

```yaml
version: "3.9"

networks:
  ia-network:
    driver: bridge

volumes:
  influxdb-data:
  postgres-data:
  redis-data:
  grafana-data:
  minio-data:
  mlflow-data:

services:
  mosquitto:
    image: eclipse-mosquitto:2
    container_name: ia-mqtt
    ports:
      - "1883:1883"
      - "9001:9001"
    volumes:
      - ./configs/mosquitto/mosquitto.conf:/mosquitto/config/mosquitto.conf
      - ./configs/mosquitto/passwd:/mosquitto/config/passwd
    networks: [ia-network]
    restart: unless-stopped
    healthcheck:
      test:
        ["CMD", "mosquitto_pub", "-h", "localhost", "-t", "health", "-m", "ok"]
      interval: 30s
      timeout: 10s
      retries: 3

  influxdb:
    image: influxdb:2.7
    container_name: ia-influxdb
    ports:
      - "8086:8086"
    environment:
      DOCKER_INFLUXDB_INIT_MODE: setup
      DOCKER_INFLUXDB_INIT_USERNAME: ${INFLUXDB_USER}
      DOCKER_INFLUXDB_INIT_PASSWORD: ${INFLUXDB_PASSWORD}
      DOCKER_INFLUXDB_INIT_ORG: ${INFLUXDB_ORG}
      DOCKER_INFLUXDB_INIT_BUCKET: ${INFLUXDB_BUCKET}
      DOCKER_INFLUXDB_INIT_ADMIN_TOKEN: ${INFLUXDB_TOKEN}
    volumes:
      - influxdb-data:/var/lib/influxdb2
    networks: [ia-network]
    restart: unless-stopped

  # ... demais serviços
```

#### `infra/configs/mosquitto/mosquitto.conf`:

```
listener 1883
listener 9001
protocol websockets
allow_anonymous false
password_file /mosquitto/config/passwd
persistence true
persistence_location /mosquitto/data/
log_dest stdout
```

---

### 2.3 Scripts de Setup Obrigatórios

#### `infra/scripts/setup.sh`:

```bash
#!/bin/bash
# Inicializa toda a infra local
# Uso: ./infra/scripts/setup.sh

set -e

echo "🔧 Copiando .env.example para .env..."
cp -n .env.example .env

echo "🐳 Subindo infraestrutura..."
docker compose -f infra/compose/docker-compose.dev.yml up -d

echo "⏳ Aguardando serviços ficarem saudáveis..."
sleep 15

echo "🗄️  Criando buckets no InfluxDB..."
# Script de inicialização do InfluxDB

echo "📊 Importando dashboards no Grafana..."
# Script de importação de dashboards base

echo "✅ Infraestrutura pronta!"
echo "   Grafana:    http://localhost:3000"
echo "   InfluxDB:   http://localhost:8086"
echo "   Node-RED:   http://localhost:1880"
echo "   MLflow:     http://localhost:5000"
echo "   MinIO:      http://localhost:9001"
```

---

### 2.4 Grafana — Dashboards Iniciais

Criar e exportar como JSON em `infra/configs/grafana/dashboards/`:

- `infra-overview.json` — CPU, memória e disco do host
- `mqtt-metrics.json` — mensagens por segundo, clientes conectados
- `influxdb-metrics.json` — escritas por segundo, uso de disco

---

### 2.5 Documentação Obrigatória

Criar `docs/infra/setup-local.md` com:

- Pré-requisitos: versão do Docker, Docker Compose, recursos mínimos (RAM, disco)
- Passo a passo de instalação do zero
- Como verificar que cada serviço está saudável (`docker compose ps`)
- Tabela de portas e credenciais padrão de desenvolvimento
- Seção de troubleshooting com erros comuns
- Como resetar o ambiente completamente

---

### 2.6 Critérios de Aceite

| #    | Critério                                               | Validação                                            |
| ---- | ------------------------------------------------------ | ---------------------------------------------------- |
| ✅ 1 | Todos os 9 serviços sobem com `docker compose up -d`   | `docker compose ps` mostra todos `healthy`           |
| ✅ 2 | Mosquitto aceita conexão MQTT com autenticação         | `mosquitto_pub -u user -P pass -t test -m ok`        |
| ✅ 3 | InfluxDB acessível com token configurado               | UI em `localhost:8086` acessível                     |
| ✅ 4 | Grafana com 3 dashboards de infra pré-configurados     | Dashboards visíveis na UI                            |
| ✅ 5 | `setup.sh` sobe tudo em menos de 5 minutos             | Execução cronometrada                                |
| ✅ 6 | Todos os dados persistem após `docker compose restart` | Reiniciar e verificar dados                          |
| ✅ 7 | `docs/infra/setup-local.md` completo                   | Alguém do time consegue rodar do zero seguindo o doc |
| ✅ 8 | Health checks configurados em todos os serviços        | `docker inspect` mostra health status                |

---

---

## Entrega 03

# 📡 Pipeline de Ingestão de Dados IoT

**Fase:** 1–2 | **Sprint:** 2–3 | **Estimativa:** 7–10 dias  
**Responsável:** Backend + Firmware  
**Módulos relacionados:** M-01, M-02, M-03  
**Dependência:** Entrega 02 concluída

### Objetivo

Criar o pipeline completo de coleta e ingestão de dados: firmware do ESP32 publicando dados reais via MQTT, Node-RED consumindo e roteando para InfluxDB, e uma API FastAPI de ingestão para fontes HTTP. Ao final, dados de sensores devem estar chegando e sendo armazenados de forma contínua.

---

### 3.1 Firmware ESP32 (`firmware/esp32-sensores/`)

#### Estrutura do projeto PlatformIO:

```
firmware/esp32-sensores/
├── platformio.ini
├── src/
│   └── main.cpp
├── include/
│   ├── config.h          # Credenciais WiFi e MQTT (via #define ou SPIFFS)
│   ├── sensors.h         # Funções de leitura de sensores
│   └── mqtt_client.h     # Wrapper de conexão MQTT
└── README.md             # Como flashar, wiring, dependências
```

#### Tópicos MQTT a serem publicados:

```
casa/energia/consumo      → {"watts": 1240.5, "volts": 220.1, "amperes": 5.64, "ts": 1709123456}
casa/energia/disjuntor    → {"id": "disjuntor_01", "status": "closed", "ts": 1709123456}
jardim/solo/umidade       → {"sensor_id": "solo_01", "umidade_pct": 34.2, "ts": 1709123456}
jardim/solo/temperatura   → {"sensor_id": "solo_01", "temp_c": 22.4, "ts": 1709123456}
casa/ambiente/temperatura → {"sensor_id": "amb_01", "temp_c": 24.1, "umidade_pct": 65.0, "ts": 1709123456}
```

---

### 3.2 Serviço Gateway IoT (`services/gateway-iot/`)

#### Estrutura de pastas:

```
services/gateway-iot/
├── Dockerfile
├── requirements.txt
├── README.md
├── src/
│   ├── main.py           # Entry point
│   ├── mqtt/
│   │   ├── client.py     # Conexão e subscrição MQTT
│   │   └── handlers.py   # Handlers por tópico
│   ├── storage/
│   │   ├── influxdb.py   # Escritor de séries temporais
│   │   └── postgres.py   # Escritor de eventos relacionais
│   ├── models/
│   │   └── sensor_reading.py  # Pydantic models para validação
│   └── config.py         # Configurações via env vars
└── tests/
    ├── test_mqtt_handlers.py
    └── test_storage.py
```

#### Regras de validação obrigatórias:

- Rejeitar mensagens com `ts` mais de 60 segundos no passado ou futuro
- Rejeitar leituras fora de faixa física (ex: `umidade > 100%`, `volts < 0`)
- Logar erros de parsing sem derrubar o serviço
- Métrica Prometheus: `mqtt_messages_received_total`, `mqtt_parse_errors_total`

---

### 3.3 Node-RED — Flows Obrigatórios

Exportar flows como JSON em `infra/configs/nodered/flows/`:

- `flow-energia.json` — subscreve `casa/energia/#`, persiste no InfluxDB
- `flow-irrigacao.json` — subscreve `jardim/#`, persiste no InfluxDB
- `flow-router.json` — rota mensagens para diferentes buckets conforme tópico

---

### 3.4 API de Ingestão (`services/gateway-iot/src/api.py`)

```
POST /api/v1/ingest/sensor
POST /api/v1/ingest/batch          # Até 100 leituras por chamada
GET  /api/v1/health
GET  /metrics                      # Prometheus
```

Documentação OpenAPI disponível em `/docs` (Swagger UI automático do FastAPI).

---

### 3.5 Documentação Obrigatória

- `services/gateway-iot/README.md` — como rodar, variáveis de ambiente, endpoints
- `firmware/esp32-sensores/README.md` — esquema de ligação (wiring diagram em ASCII ou imagem), como flashar
- `docs/data/topicos-mqtt.md` — tabela completa de tópicos, payloads e frequências

---

### 3.6 Critérios de Aceite

| #    | Critério                                                | Validação                                   |
| ---- | ------------------------------------------------------- | ------------------------------------------- |
| ✅ 1 | ESP32 publica dados reais a cada 5s no broker MQTT      | `mosquitto_sub -t "casa/#" -v` mostra dados |
| ✅ 2 | Gateway consome todos os tópicos e persiste no InfluxDB | Query no InfluxDB retorna dados             |
| ✅ 3 | Dados inválidos são rejeitados e logados sem crash      | Enviar payload inválido, checar logs        |
| ✅ 4 | Node-RED flow processando e roteando mensagens          | Painel Node-RED mostra fluxo ativo          |
| ✅ 5 | API de ingestão HTTP funcionando com validação Pydantic | `POST /ingest/sensor` retorna 200           |
| ✅ 6 | Métricas Prometheus expostas pelo gateway               | `GET /metrics` retorna dados legíveis       |
| ✅ 7 | Testes unitários com cobertura ≥ 70% dos handlers       | `pytest --cov` mostra cobertura             |
| ✅ 8 | Documentação de tópicos MQTT criada                     | `docs/data/topicos-mqtt.md` completo        |

---

---

## Entrega 04

# ⚡ Módulo de Energia (M-01) — Coleta e Armazenamento

**Fase:** 2 | **Sprint:** 3–4 | **Estimativa:** 5–7 dias  
**Responsável:** Backend + Hardware  
**Módulos relacionados:** M-01  
**Requisitos cobertos:** RF-EN-01, RF-EN-05  
**Dependência:** Entrega 03 concluída

### Objetivo

Implementar a coleta completa e confiável de dados do sensor de energia PZEM-004T via ESP32, com armazenamento em InfluxDB e dashboard Grafana funcional mostrando consumo em tempo real e histórico.

---

### 4.1 Firmware (`firmware/esp32-energia/`)

#### Grandezas coletadas a cada 5 segundos:

- Tensão (V), Corrente (A), Potência ativa (W), Potência aparente (VA)
- Fator de potência, Frequência (Hz), Energia acumulada (kWh)

#### Tópico MQTT:

```
casa/energia/medidor/{id_medidor}
Payload: {
  "id": "medidor_01",
  "tensao_v": 220.3,
  "corrente_a": 5.61,
  "potencia_w": 1234.5,
  "potencia_va": 1240.0,
  "fator_potencia": 0.995,
  "frequencia_hz": 60.0,
  "energia_kwh": 542.3,
  "ts": 1709123456
}
```

#### Funcionalidades obrigatórias do firmware:

- Reconexão automática ao WiFi e MQTT com backoff exponencial
- Buffer local de 50 leituras caso a conexão caia (salvas na RAM/SPIFFS)
- LED de status: verde = OK, amarelo = sem WiFi, vermelho = sem MQTT

---

### 4.2 Schema InfluxDB

```
Measurement: energia_consumo
Tags:
  - medidor_id (string)
  - local (string: "sala", "cozinha", etc.)
Fields:
  - tensao_v (float)
  - corrente_a (float)
  - potencia_w (float)
  - potencia_va (float)
  - fator_potencia (float)
  - frequencia_hz (float)
  - energia_kwh (float)
Timestamp: unix nanoseconds
```

---

### 4.3 Dashboard Grafana (`infra/configs/grafana/dashboards/energia-tempo-real.json`)

Painéis obrigatórios:

- Gauge: Potência atual (W) com zonas verde/amarelo/vermelho
- Gráfico de linha: Potência nas últimas 24h
- Stat: Consumo total do dia (kWh)
- Stat: Custo estimado do dia (R$) com tarifa configurável
- Gráfico de barras: Consumo por hora (últimas 24h)
- Tabela: Últimas 20 leituras brutas

---

### 4.4 Documentação Obrigatória

- `firmware/esp32-energia/README.md` — diagrama de ligação PZEM-004T, pinagem ESP32
- `docs/modulos/m01-energia.md` — descrição do módulo, schema de dados, frequência de coleta, limites físicos esperados

---

### 4.5 Critérios de Aceite

| #    | Critério                                                                    | Validação                             |
| ---- | --------------------------------------------------------------------------- | ------------------------------------- |
| ✅ 1 | PZEM-004T enviando 12 leituras por minuto ao InfluxDB                       | Query Flux conta registros por minuto |
| ✅ 2 | Dashboard Grafana mostra consumo em tempo real (delay < 10s)                | Observação visual                     |
| ✅ 3 | Buffer local funciona: desconectar WiFi por 2min, reconectar e dados chegam | Teste manual                          |
| ✅ 4 | Histórico de 30 dias armazenado sem gaps (retention policy configurada)     | Checar configuração InfluxDB          |
| ✅ 5 | Dashboard com cálculo de custo usando tarifa configurável                   | Alterar tarifa e ver atualização      |
| ✅ 6 | `docs/modulos/m01-energia.md` completo                                      | Revisão manual                        |

---

---

## Entrega 05

# 🧠 Módulo de Energia (M-01) — Modelo Preditivo e Alertas

**Fase:** 3 | **Sprint:** 4–6 | **Estimativa:** 10–14 dias  
**Responsável:** Data Scientist + Backend  
**Módulos relacionados:** M-01  
**Requisitos cobertos:** RF-EN-02, RF-EN-03, RF-EN-04, RN-01, RN-05, RN-06, RN-07, RN-09  
**Dependência:** Entrega 04 com 7+ dias de dados coletados

### Objetivo

Desenvolver e colocar em produção os modelos de ML para: detecção de anomalias de consumo (Isolation Forest), previsão de consumo futuro (Prophet) e projeção de fatura mensal. Incluir sistema de alertas via Telegram.

---

### 5.1 Estrutura do Serviço de Inferência (`services/inference-engine/`)

```
services/inference-engine/
├── Dockerfile
├── requirements.txt
├── README.md
├── src/
│   ├── main.py
│   ├── jobs/
│   │   ├── anomaly_detector.py    # Job Celery: Isolation Forest
│   │   ├── forecaster.py          # Job Celery: Prophet
│   │   └── billing_estimator.py   # Projeção de fatura
│   ├── models/
│   │   ├── base_model.py          # Classe base abstrata
│   │   ├── isolation_forest.py    # Wrapper Isolation Forest
│   │   └── prophet_model.py       # Wrapper Prophet
│   ├── data/
│   │   ├── fetcher.py             # Busca dados do InfluxDB
│   │   └── preprocessor.py        # Normalização e feature engineering
│   ├── alerts/
│   │   └── telegram.py            # Envio de alertas via Telegram Bot
│   └── config.py
└── tests/
    ├── test_anomaly_detector.py
    ├── test_forecaster.py
    └── test_alerts.py
```

---

### 5.2 Notebooks de Treinamento (`notebooks/treinamento/`)

Obrigatório criar e versionar:

- `energia-eda.ipynb` — análise exploratória: distribuição, sazonalidade, outliers
- `energia-isolation-forest.ipynb` — treino, tuning de hiperparâmetros, avaliação
- `energia-prophet.ipynb` — treino, validação cruzada temporal, métricas MAE/MAPE
- `energia-baseline.ipynb` — cálculo do baseline histórico por hora/dia da semana

---

### 5.3 Integração com MLflow

Cada experimento de treino deve registrar:

```python
mlflow.log_param("contamination", 0.05)         # hiperparâmetros
mlflow.log_metric("anomaly_precision", 0.92)     # métricas
mlflow.log_metric("anomaly_recall", 0.87)
mlflow.sklearn.log_model(model, "isolation_forest")  # artefato do modelo
mlflow.set_tag("modulo", "energia")
mlflow.set_tag("versao_dados", "2024-03")
```

---

### 5.4 Regras de Alerta (baseadas em RN-01 a RN-04)

```python
# config/alert_rules.yml
energia:
  anomalia:
    threshold_score: -0.3          # Score abaixo disso = anomalia
    cooldown_minutos: 15           # RN-01
    severidade: CRITICO
  pico:
    threshold_percentual: 150      # RF-EN-03: 150% da média
    janela_minutos: 60
    cooldown_minutos: 15
    severidade: AVISO
```

#### Formato do alerta Telegram:

```
⚡ ALERTA DE ENERGIA — CRÍTICO

📍 Medidor: medidor_01
🕐 Horário: 14:32 | 05/03/2026
📊 Consumo atual: 3.840 W
📈 Média esperada: 1.240 W (+209%)
🔍 Score anomalia: -0.47

→ Verifique equipamentos na sala/cozinha
→ Dashboard: http://grafana:3000/d/energia
```

---

### 5.5 Documentação Obrigatória

- `docs/modulos/m01-modelos.md` com:
  - Descrição de cada modelo, quando é executado, o que detecta
  - Métricas de avaliação obtidas no treino
  - Como retreinar os modelos manualmente
  - Como interpretar os alertas recebidos
  - Diagrama do pipeline: dados → preprocessamento → modelo → decisão → alerta

---

### 5.6 Critérios de Aceite

| #    | Critério                                                            | Validação                                     |
| ---- | ------------------------------------------------------------------- | --------------------------------------------- |
| ✅ 1 | Isolation Forest detecta consumo anômalo injetado manualmente       | Injetar dado anômalo, alerta chega em < 2min  |
| ✅ 2 | Alerta Telegram enviado com formato correto                         | Verificar mensagem no grupo                   |
| ✅ 3 | Cooldown de 15min funcionando (RN-01)                               | Injetar 2 anomalias consecutivas, só 1 alerta |
| ✅ 4 | Prophet prevê consumo das próximas 24h com MAPE < 20%               | Checar notebook de validação                  |
| ✅ 5 | Projeção de fatura mensal visível no dashboard Grafana              | Painel "Estimativa Mensal" no dashboard       |
| ✅ 6 | Todos os experimentos versionados no MLflow                         | Interface MLflow mostra runs                  |
| ✅ 7 | Toda decisão de alerta logada com timestamp, modelo e score (RN-07) | Checar logs estruturados                      |
| ✅ 8 | Notebooks de treino executáveis do zero com dados reais             | Executar notebook limpo                       |
| ✅ 9 | Cobertura de testes ≥ 75% no inference-engine                       | `pytest --cov`                                |

---

---

## Entrega 06

# 💧 Módulo de Irrigação (M-03) — Sensores e Automação

**Fase:** 2–3 | **Sprint:** 5–7 | **Estimativa:** 8–10 dias  
**Responsável:** Backend + Hardware  
**Módulos relacionados:** M-03  
**Requisitos cobertos:** RF-IR-01 a RF-IR-05, RN-10 a RN-13  
**Dependência:** Entrega 03 concluída

### Objetivo

Implementar leitura de umidade do solo, integração com API climática, modelo de decisão de irrigação e acionamento automático da válvula solenoide via relé no ESP32.

---

### 6.1 Firmware (`firmware/esp32-irrigacao/`)

#### Sensores:

- Capacitive Soil Moisture Sensor v1.2 (pino analógico)
- DHT22 (temperatura e umidade do ar)

#### Tópicos MQTT publicados:

```
jardim/solo/{zona_id}/umidade       → {"zona": "A", "umidade_pct": 34.2, "ts": ...}
jardim/solo/{zona_id}/temperatura   → {"zona": "A", "temp_c": 22.4, "ts": ...}
jardim/irrigacao/{zona_id}/status   → {"zona": "A", "ativo": false, "ts": ...}
```

#### Tópico MQTT subscrito (para receber comandos):

```
jardim/irrigacao/{zona_id}/comando
Payload: {"acao": "ligar", "duracao_minutos": 12, "origem": "ia"}
         {"acao": "desligar", "origem": "manual"}
```

---

### 6.2 Serviço de Irrigação (`services/irrigation-service/`)

```
services/irrigation-service/
├── src/
│   ├── decision_engine.py     # Lógica de decisão de irrigação
│   ├── weather_client.py      # Integração OpenWeatherMap API
│   ├── models/
│   │   └── irrigation_model.py  # Random Forest: decidir irrigar e duração
│   ├── rules/
│   │   └── business_rules.py    # RN-10 a RN-13 implementadas como código
│   └── scheduler.py           # Execução periódica (a cada 10 min)
```

#### Regras de negócio como código (obrigatório, baseado em RN-10 a RN-13):

```python
class IrrigationRules:
    HORARIOS_PERMITIDOS = [(5, 9), (18, 21)]      # RN-11
    DURACAO_MAXIMA_MIN = 60                         # RN-12
    INTERVALO_MINIMO_HORAS = 4                      # RN-13
    THRESHOLD_CHUVA_MM = 5.0                        # RN-10

    def pode_irrigar(self, contexto: IrrigationContext) -> tuple[bool, str]:
        """Retorna (pode_irrigar, motivo_negacao)"""
        ...
```

---

### 6.3 Integração Climática

- API: OpenWeatherMap (plano gratuito)
- Variável de ambiente: `OPENWEATHER_API_KEY`
- Cache Redis: previsão cacheada por 30 minutos para evitar rate limit
- Fallback: se API indisponível, usar última previsão cacheada (máx 2h)

---

### 6.4 Dashboard Grafana (`infra/configs/grafana/dashboards/irrigacao.json`)

- Gauge: Umidade atual por zona (com threshold visual)
- Gráfico: Histórico de umidade 7 dias
- Stat: Última irrigação (horário e duração)
- Stat: Status da válvula (ativa/inativa)
- Tabela: Log das últimas 20 irrigações (início, fim, duração, origem: manual/IA)

---

### 6.5 Documentação Obrigatória

- `docs/modulos/m03-irrigacao.md` — fluxo de decisão, regras de negócio, como calibrar sensor
- `firmware/esp32-irrigacao/README.md` — diagrama de ligação sensor + relé + válvula

---

### 6.6 Critérios de Aceite

| #    | Critério                                                  | Validação                                |
| ---- | --------------------------------------------------------- | ---------------------------------------- |
| ✅ 1 | Sensor de umidade lendo e publicando no MQTT a cada 10min | `mosquitto_sub -t "jardim/#"`            |
| ✅ 2 | Irrigação acionada automaticamente quando umidade < 40%   | Forçar leitura baixa, relé aciona        |
| ✅ 3 | Irrigação bloqueada com chuva prevista > 5mm (RN-10)      | Mockar API com chuva, verificar bloqueio |
| ✅ 4 | Irrigação bloqueada fora do horário permitido (RN-11)     | Testar fora de 05h-09h e 18h-21h         |
| ✅ 5 | Duração máxima de 60min respeitada (RN-12)                | Checar código e log                      |
| ✅ 6 | Intervalo mínimo de 4h entre sessões (RN-13)              | Log mostra intervalo respeitado          |
| ✅ 7 | Cancelamento manual via MQTT funciona                     | Publicar `{"acao": "desligar"}`          |
| ✅ 8 | Log completo de todas as irrigações no PostgreSQL         | Query na tabela `irrigacao_log`          |

---

---

## Entrega 07

# 🖥️ Módulo de Servidor (M-05) — Monitoramento e Alertas

**Fase:** 2–3 | **Sprint:** 5–6 | **Estimativa:** 6–8 dias  
**Responsável:** DevOps + Backend  
**Módulos relacionados:** M-05  
**Requisitos cobertos:** RF-SV-01 a RF-SV-04, RNF-05, RNF-06  
**Dependência:** Entrega 02 concluída

### Objetivo

Implementar coleta completa de métricas do servidor com Telegraf + Prometheus, dashboard Grafana de saúde da infraestrutura, alertas preditivos com AlertManager e análise de logs com NLP.

---

### 7.1 Configuração Telegraf (`infra/configs/telegraf/telegraf.conf`)

Plugins de entrada obrigatórios:

```toml
[[inputs.cpu]]
  percpu = true
  totalcpu = true

[[inputs.mem]]

[[inputs.disk]]
  ignore_fs = ["tmpfs", "devtmpfs"]

[[inputs.diskio]]

[[inputs.net]]

[[inputs.system]]

[[inputs.processes]]

[[inputs.docker]]
  endpoint = "unix:///var/run/docker.sock"
  container_names = []

[[inputs.tail]]  # Leitura de logs
  files = ["/var/log/syslog", "/var/log/auth.log"]
  data_format = "grok"
```

---

### 7.2 Alertas AlertManager (`infra/configs/alertmanager/alerts.yml`)

Alertas a configurar:

```yaml
groups:
  - name: servidor
    rules:
      - alert: CPUAlto
        expr: cpu_usage_percent > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "CPU acima de 80% por 5 minutos"

      - alert: MemoriaCritica
        expr: mem_used_percent > 90
        for: 2m
        labels:
          severity: critical

      - alert: DiscoQuaseCheio
        expr: disk_used_percent > 85
        labels:
          severity: warning

      - alert: ServicoDown
        expr: up == 0
        for: 1m
        labels:
          severity: critical
```

---

### 7.3 Análise de Logs com NLP (`services/inference-engine/src/jobs/log_analyzer.py`)

- Rodar a cada 5 minutos
- Classificar linhas de log: `NORMAL`, `AVISO`, `CRITICO`
- Modelo: TF-IDF + Logistic Regression (treinado em dataset público de logs)
- Alertar imediatamente para linhas `CRITICO`
- Relatório diário às 08h com resumo dos erros das últimas 24h

---

### 7.4 Dashboard Grafana (`infra/configs/grafana/dashboards/servidor-saude.json`)

Painéis obrigatórios:

- CPU: uso por core (gráfico de área)
- Memória: uso, disponível, cache (gráfico empilhado)
- Disco: uso por partição (gauge)
- Rede: bytes enviados/recebidos por interface
- Docker: containers up/down, uso de CPU e RAM por container
- Logs: frequência de erros por nível (INFO/WARN/ERROR) nas últimas 24h

---

### 7.5 Documentação Obrigatória

- `docs/modulos/m05-servidor.md` — thresholds configurados, como adicionar novos alertas, runbook de resposta a incidentes
- `docs/runbooks/cpu-alto.md` — passos para investigar CPU alta
- `docs/runbooks/disco-cheio.md` — passos para liberar espaço

---

### 7.6 Critérios de Aceite

| #    | Critério                                           | Validação                              |
| ---- | -------------------------------------------------- | -------------------------------------- |
| ✅ 1 | Telegraf coletando todas as métricas a cada 15s    | Query no InfluxDB mostra dados         |
| ✅ 2 | Dashboard Grafana com todos os painéis funcionando | Revisão visual                         |
| ✅ 3 | Alerta de CPU dispara quando uso > 80% por 5min    | `stress --cpu 8 --timeout 360`         |
| ✅ 4 | Alerta de serviço down chega em < 2min             | Derrubar um container, checar Telegram |
| ✅ 5 | Análise de log classifica erros com acurácia ≥ 85% | Avaliar no conjunto de teste           |
| ✅ 6 | Relatório diário de logs enviado às 08h            | Checar Telegram no dia seguinte        |
| ✅ 7 | Runbooks criados para os 2 alertas mais comuns     | Arquivos em `docs/runbooks/`           |

---

---

## Entrega 08

# 🔧 Módulo de Equipamentos (M-02) — Detecção de Anomalia por Equipamento

**Fase:** 3 | **Sprint:** 6–8 | **Estimativa:** 8–10 dias  
**Responsável:** Data Scientist + Backend  
**Módulos relacionados:** M-02  
**Requisitos cobertos:** RF-EQ-01 a RF-EQ-04, RN-05 a RN-07  
**Dependência:** Entrega 05 (reaproveitamento do inference-engine)

### Objetivo

Estender o sistema para monitorar consumo individual de cada equipamento via smart plugs, criar perfis de consumo (baseline) por equipamento, e detectar desvios que indicam desgaste ou uso excessivo.

---

### 8.1 Schema de Cadastro de Equipamentos (PostgreSQL)

```sql
CREATE TABLE equipamentos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome VARCHAR(100) NOT NULL,           -- "Ar-condicionado sala"
    tipo VARCHAR(50) NOT NULL,            -- "ar_condicionado", "geladeira"
    smart_plug_id VARCHAR(50) UNIQUE,     -- ID do smart plug
    potencia_nominal_w FLOAT,             -- Potência nominal da placa
    local VARCHAR(100),
    ativo BOOLEAN DEFAULT TRUE,
    criado_em TIMESTAMP DEFAULT NOW()
);

CREATE TABLE equipamento_baseline (
    equipamento_id UUID REFERENCES equipamentos(id),
    hora_dia INT,                         -- 0-23
    dia_semana INT,                       -- 0=seg, 6=dom
    media_w FLOAT,
    std_w FLOAT,
    atualizado_em TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (equipamento_id, hora_dia, dia_semana)
);
```

---

### 8.2 Pipeline de Baseline (`services/inference-engine/src/jobs/equipment_baseline.py`)

- Executar 1x por dia às 03h (quando há 7+ dias de dados — RN-05)
- Calcular média e desvio padrão de consumo por `(hora_do_dia, dia_da_semana)`
- Atualizar tabela `equipamento_baseline` no PostgreSQL
- Logar execução no MLflow como "run" do tipo "baseline_update"

---

### 8.3 Detector de Anomalia por Equipamento

Algoritmo Z-Score:

```python
def detectar_anomalia_equipamento(
    leitura_atual_w: float,
    baseline: EquipamentoBaseline,
    threshold_desvios: float = 2.5  # RN-06: equivalente a ~98.8% confiança
) -> AnomaliaResult:
    z_score = (leitura_atual_w - baseline.media_w) / baseline.std_w
    is_anomalia = abs(z_score) > threshold_desvios
    confianca = min(abs(z_score) / threshold_desvios, 1.0)
    return AnomaliaResult(is_anomalia=is_anomalia, z_score=z_score, confianca=confianca)
```

---

### 8.4 Endpoint de Gestão de Equipamentos (FastAPI)

```
GET    /api/v1/equipamentos
POST   /api/v1/equipamentos
GET    /api/v1/equipamentos/{id}/baseline
GET    /api/v1/equipamentos/{id}/historico
GET    /api/v1/equipamentos/{id}/alertas
```

---

### 8.5 Documentação Obrigatória

- `docs/modulos/m02-equipamentos.md` — como cadastrar equipamento, como interpretar alertas, como ajustar threshold
- `docs/data/schema-postgres.md` — diagrama ER e descrição das tabelas

---

### 8.6 Critérios de Aceite

| #    | Critério                                                   | Validação                               |
| ---- | ---------------------------------------------------------- | --------------------------------------- |
| ✅ 1 | Cadastro de equipamento via API retorna 201 com UUID       | `POST /equipamentos`                    |
| ✅ 2 | Baseline calculado após 7 dias de dados (RN-05)            | Verificar tabela `equipamento_baseline` |
| ✅ 3 | Anomalia detectada quando consumo > 30% acima do baseline  | Simular consumo alto                    |
| ✅ 4 | Alerta não disparado com confiança < 70% (RN-06)           | Injetar dado limítrofe                  |
| ✅ 5 | Toda anomalia logada com modelo, score e timestamp (RN-07) | Checar tabela de auditoria              |
| ✅ 6 | Relatorio semanal de saúde dos equipamentos gerado         | Verificar relatório no Telegram         |
| ✅ 7 | API com documentação OpenAPI completa                      | Acessar `/docs`                         |

---

---

## Entrega 09

# 🏠 Módulo de Casa Inteligente (M-04) — Home Assistant + LLM

**Fase:** 4 | **Sprint:** 8–10 | **Estimativa:** 12–15 dias  
**Responsável:** Backend + AI Engineer  
**Módulos relacionados:** M-04  
**Requisitos cobertos:** RF-CI-01 a RF-CI-04, RN-18, RN-19, RN-20  
**Dependência:** Home Assistant configurado, Ollama rodando com LLaMA 3

### Objetivo

Integrar o sistema ao Home Assistant para controle de dispositivos smart home, e implementar o LLM local (Ollama + LLaMA 3) com LangChain para interpretar comandos em linguagem natural e executar ações nos dispositivos.

---

### 9.1 Configuração Home Assistant

#### Arquivo `infra/configs/homeassistant/configuration.yaml`:

```yaml
homeassistant:
  name: "IA Preditiva Casa"
  latitude: !secret latitude
  longitude: !secret longitude

# Habilitar API REST
api:

# Token de acesso longa duração configurado via env
# HA_TOKEN no .env
```

#### Variáveis de ambiente necessárias:

```env
HA_URL=http://homeassistant:8123
HA_TOKEN=seu_token_longa_duracao
```

---

### 9.2 Serviço LLM (`services/llm-service/`)

```
services/llm-service/
├── Dockerfile
├── requirements.txt
├── README.md
├── src/
│   ├── main.py                  # FastAPI app
│   ├── agent/
│   │   ├── home_agent.py        # LangChain agent principal
│   │   ├── tools/
│   │   │   ├── ha_tools.py      # Tools: ligar/desligar/consultar dispositivo
│   │   │   ├── sensor_tools.py  # Tools: consultar sensores InfluxDB
│   │   │   └── alert_tools.py   # Tools: listar alertas ativos
│   │   └── prompts/
│   │       └── system_prompt.py # System prompt do agente
│   ├── memory/
│   │   └── conversation.py      # Histórico: últimas 10 interações (RN-20)
│   └── safety/
│       └── confirmation.py      # RN-18: confirmação para acoes críticas
└── tests/
    └── test_agent.py
```

---

### 9.3 System Prompt do Agente (obrigatório documentar)

```python
SYSTEM_PROMPT = """
Você é um assistente de casa inteligente. Você pode:
- Controlar dispositivos (ligar/desligar/dimmer/temperatura)
- Consultar o estado atual dos dispositivos
- Verificar dados de sensores (temperatura, umidade, energia)
- Criar automações simples

REGRAS OBRIGATÓRIAS:
1. Sempre confirmar com o usuário antes de ações que afetam 3+ dispositivos simultaneamente
2. Nunca enviar dados para APIs externas
3. Responda SEMPRE em português brasileiro
4. Se não tiver certeza do que o usuário quer, pergunte antes de agir
5. Informe sempre quais dispositivos foram afetados e o resultado da ação

Dispositivos disponíveis: {lista_dispositivos}
Estado atual: {estado_atual}
"""
```

---

### 9.4 API do LLM Service

```
POST /api/v1/chat
     Body: {"mensagem": "Apaga tudo e deixa só a luz do quarto", "session_id": "user_123"}
     Response: {"resposta": "...", "acoes_executadas": [...], "requer_confirmacao": false}

POST /api/v1/chat/confirmar
     Body: {"session_id": "user_123", "confirmado": true}

GET  /api/v1/dispositivos
GET  /api/v1/chat/historico/{session_id}
```

---

### 9.5 Automação de Modo Ausente (RF-CI-04)

Criar automação no Home Assistant que:

1. Detecta ausência via sensores de presença Zigbee
2. Aguarda 5 minutos de ausência confirmada
3. Publica evento MQTT: `casa/presenca/modo`
4. Serviço LLM executa rotina "modo_ausente": apaga luzes, AC para 28°C, desativa tomadas não essenciais
5. Notifica Telegram

---

### 9.6 Documentação Obrigatória

- `docs/modulos/m04-casa-inteligente.md` — como configurar dispositivos, exemplos de comandos suportados, limitações do LLM
- `services/llm-service/README.md` — como instalar Ollama, qual modelo baixar, como rodar local

---

### 9.7 Critérios de Aceite

| #    | Critério                                                     | Validação                      |
| ---- | ------------------------------------------------------------ | ------------------------------ |
| ✅ 1 | Comando "apaga a luz da sala" executa ação no Home Assistant | Testar com dispositivo real    |
| ✅ 2 | Confirmação solicitada para ações em 3+ dispositivos (RN-18) | Enviar "apaga tudo em casa"    |
| ✅ 3 | LLM roda 100% local, sem chamadas externas (RN-19)           | Monitorar rede durante uso     |
| ✅ 4 | Histórico limitado a últimas 10 interações (RN-20)           | Checar código de memory        |
| ✅ 5 | Modo ausente ativa automaticamente após 5min sem presença    | Sair de casa e aguardar        |
| ✅ 6 | Resposta em < 5 segundos para comandos simples               | Medir tempo de resposta        |
| ✅ 7 | API documentada com exemplos de uso                          | Acessar `/docs`                |
| ✅ 8 | Todos os comandos executados são logados (RN-07)             | Checar tabela `llm_action_log` |

---

---

## Entrega 10

# 📷 Módulo de Câmeras (M-06) — Visão Computacional

**Fase:** 4 | **Sprint:** 9–11 | **Estimativa:** 10–14 dias  
**Responsável:** AI Engineer + Backend  
**Módulos relacionados:** M-06  
**Requisitos cobertos:** RF-CA-01 a RF-CA-05, RN-14 a RN-17  
**Dependência:** Entregas 02 e 03 concluídas, MinIO configurado

### Objetivo

Implementar captura de stream de câmeras IP via RTSP, detecção de objetos em tempo real com YOLOv8, sistema de alertas com snapshot, e configuração de zonas de detecção por câmera.

---

### 10.1 Serviço de Visão (`services/vision-service/`)

```
services/vision-service/
├── Dockerfile
├── requirements.txt
├── README.md
├── src/
│   ├── main.py
│   ├── capture/
│   │   └── rtsp_capture.py       # Captura de stream via OpenCV
│   ├── detection/
│   │   ├── yolo_detector.py      # Wrapper YOLOv8
│   │   ├── zone_filter.py        # Filtragem por zona de detecção (RN-14)
│   │   └── confidence_filter.py  # Filtragem por confiança mínima
│   ├── storage/
│   │   ├── minio_client.py       # Upload de snapshots (RN-15)
│   │   └── event_logger.py       # Log de eventos no PostgreSQL
│   ├── alerts/
│   │   └── camera_alert.py       # Alerta Telegram com foto
│   └── config/
│       └── cameras.py            # Configuração de câmeras e zonas
└── tests/
    ├── test_yolo_detector.py
    └── test_zone_filter.py
```

---

### 10.2 Schema de Configuração de Câmeras (PostgreSQL)

```sql
CREATE TABLE cameras (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome VARCHAR(100) NOT NULL,
    rtsp_url TEXT NOT NULL,
    local VARCHAR(100),
    ativa BOOLEAN DEFAULT TRUE,
    apenas_modo_ausente BOOLEAN DEFAULT TRUE,  -- RN-16
    confianca_minima FLOAT DEFAULT 0.65        -- RN-17
);

CREATE TABLE camera_zonas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    camera_id UUID REFERENCES cameras(id),
    nome VARCHAR(50),
    -- Polígono como lista de pontos [x%, y%] normalizados (0-1)
    pontos JSONB NOT NULL,
    ativa BOOLEAN DEFAULT TRUE
);

CREATE TABLE camera_eventos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    camera_id UUID REFERENCES cameras(id),
    timestamp TIMESTAMP NOT NULL,
    tipo_objeto VARCHAR(50),          -- "person", "car", etc.
    confianca FLOAT,
    snapshot_url TEXT,
    zona_id UUID REFERENCES camera_zonas(id),
    alerta_enviado BOOLEAN DEFAULT FALSE,
    falso_positivo BOOLEAN DEFAULT FALSE  -- Para retreino (RN-17)
);
```

---

### 10.3 Pipeline de Detecção

```python
# Fluxo por frame:
# 1. Capturar frame via RTSP (OpenCV)
# 2. Redimensionar para 640x640 (YOLOv8 input)
# 3. Executar inferência YOLOv8
# 4. Filtrar por classes de interesse ["person", "car", "motorcycle"]
# 5. Filtrar por confiança mínima (RN-17)
# 6. Filtrar por zonas de detecção configuradas (RN-14)
# 7. Se evento válido:
#    a. Verificar modo ausente (RN-16 para câmeras internas)
#    b. Salvar snapshot no MinIO
#    c. Logar evento no PostgreSQL
#    d. Enviar alerta Telegram com snapshot < 10s após detecção (RF-CA-03)
```

---

### 10.4 Formato do Alerta de Câmera (Telegram)

```
🚨 ALERTA DE SEGURANÇA

📷 Câmera: Entrada Principal
🕐 Horário: 02:34 | 05/03/2026
👤 Detectado: Pessoa (confiança: 94%)
📍 Zona: Porta de entrada

[snapshot anexado como foto]

🔘 Falso positivo? Responda /fp_{evento_id}
→ Salvo em: MinIO/snapshots/2026/03/05/
```

---

### 10.5 API de Configuração de Zonas

```
GET    /api/v1/cameras
POST   /api/v1/cameras
GET    /api/v1/cameras/{id}/zonas
POST   /api/v1/cameras/{id}/zonas      # Cadastrar zona com polígono
DELETE /api/v1/cameras/{id}/zonas/{zona_id}
GET    /api/v1/cameras/{id}/eventos
POST   /api/v1/eventos/{id}/falso-positivo  # RN-17: marcar para retreino
```

---

### 10.6 Política de Retenção de Snapshots (RN-15)

Configurar job Celery diário:

```python
# Executa às 03h
# Remove snapshots com mais de 90 dias do MinIO
# Mantém metadados no PostgreSQL por 1 ano
# Alerta se armazenamento > 80% da capacidade configurada
```

---

### 10.7 Documentação Obrigatória

- `docs/modulos/m06-cameras.md` — como adicionar câmera, como configurar zonas, como interpretar alertas, política de privacidade
- `services/vision-service/README.md` — requisitos de hardware para YOLO (GPU recomendada), como configurar CPU fallback

---

### 10.8 Critérios de Aceite

| #    | Critério                                                            | Validação                                |
| ---- | ------------------------------------------------------------------- | ---------------------------------------- |
| ✅ 1 | Stream RTSP capturado e processado em ≥ 10 FPS (RNF-04)             | Medir FPS no log                         |
| ✅ 2 | Pessoa detectada e alerta com foto chegando em < 10s                | Entrar no campo da câmera, cronometrar   |
| ✅ 3 | Detecção fora da zona configurada é ignorada (RN-14)                | Desenhar zona pequena, mover fora dela   |
| ✅ 4 | Câmera interna só detecta em modo ausente (RN-16)                   | Ativar câmera interna com alguém em casa |
| ✅ 5 | Snapshots salvos no MinIO com URL no evento                         | Verificar MinIO UI                       |
| ✅ 6 | Snapshots removidos após 90 dias (RN-15)                            | Verificar job agendado                   |
| ✅ 7 | Marcação de falso positivo funciona via Telegram `/fp_`             | Responder mensagem de alerta             |
| ✅ 8 | 3 falsos positivos seguidos disparam alerta de recalibração (RN-17) | Marcar 3 FP e verificar alerta           |
| ✅ 9 | Cobertura de testes ≥ 70% no vision-service                         | `pytest --cov`                           |

---

---

## Resumo Geral das Entregas

| #   | Entrega                              | Fase | Sprint | Dias  | Módulos          |
| --- | ------------------------------------ | ---- | ------ | ----- | ---------------- |
| 01  | Setup do Repositório e Estrutura     | 1    | 1      | 3–5   | Todos            |
| 02  | Infraestrutura Base com Docker       | 1    | 1–2    | 5–7   | Todos            |
| 03  | Pipeline de Ingestão IoT             | 1–2  | 2–3    | 7–10  | M-01, M-02, M-03 |
| 04  | Energia — Coleta e Armazenamento     | 2    | 3–4    | 5–7   | M-01             |
| 05  | Energia — Modelo Preditivo e Alertas | 3    | 4–6    | 10–14 | M-01             |
| 06  | Irrigação — Sensores e Automação     | 2–3  | 5–7    | 8–10  | M-03             |
| 07  | Servidor — Monitoramento e Alertas   | 2–3  | 5–6    | 6–8   | M-05             |
| 08  | Equipamentos — Detecção de Anomalia  | 3    | 6–8    | 8–10  | M-02             |
| 09  | Casa Inteligente — HA + LLM          | 4    | 8–10   | 12–15 | M-04             |
| 10  | Câmeras — Visão Computacional        | 4    | 9–11   | 10–14 | M-06             |

**Estimativa total:** 74–100 dias de desenvolvimento  
**Paralelismo possível:** Entregas 06 e 07 podem rodar em paralelo com a 05 (equipes diferentes)

---

## Dependências entre Entregas

```
01 ──► 02 ──► 03 ──► 04 ──► 05
                │
                ├──► 06
                │
                ├──► 07
                │
                └──► 08 (depende também de 05)

05 ──► 08
02 ──► 09 (+ Ollama configurado)
02 ──► 10
03 ──► 10
```

---

> **Nota:** Cada entrega deve ter seu Pull Request revisado por pelo menos 1 outro desenvolvedor antes de ser mergeada. Os critérios de aceite ✅ são obrigatórios — sem todos aprovados a entrega não é considerada concluída.
