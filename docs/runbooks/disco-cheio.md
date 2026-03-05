# Runbook - Disco Cheio

1. Confirmar particao com uso > 85% no dashboard.
2. Verificar consumo por diretorio:
   - Linux: `du -h --max-depth=1 /var | sort -h`
   - Windows: usar Explorer/PowerShell para ranking de pastas.
3. Limpar logs/artefatos temporarios antigos.
4. Verificar volumes Docker:
   - `docker system df`
   - `docker volume ls`
5. Se necessario, expandir armazenamento e revisar retention.
