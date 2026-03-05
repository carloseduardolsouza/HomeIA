# Modulo M-05 - Servidor

## Thresholds configurados

- CPUAlto: > 80% por 5 min.
- MemoriaCritica: > 90% por 2 min.
- DiscoQuaseCheio: > 85%.
- ServicoDown: `up == 0` por 1 min.

## Como adicionar novos alertas

1. Editar `infra/configs/alertmanager/alerts.yml`.
2. Adicionar regra no grupo correspondente.
3. Reiniciar Prometheus: `docker compose ... restart prometheus`.
4. Validar em `/alerts` do Prometheus.

## Runbook de resposta a incidentes

- Confirmar alerta no Grafana/Prometheus.
- Validar impacto (servicos afetados).
- Aplicar runbook especifico (`docs/runbooks/`).
- Registrar causa raiz e acao corretiva.
