# ADR-001 - Escolha do InfluxDB para series temporais

## Status

Aceito

## Contexto

O sistema HomeIA precisa armazenar metricas de sensores IoT com alta frequencia e consultas por janela de tempo.

## Decisao

Adotar InfluxDB como banco principal para series temporais.

## Consequencias

- Melhor performance para escrita/consulta temporal.
- Linguagem Flux para agregacoes de series.
- Necessidade de manutencao adicional de um banco especializado.
