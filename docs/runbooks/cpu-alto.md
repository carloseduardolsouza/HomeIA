# Runbook - CPU Alto

1. Confirmar pico no dashboard `servidor-saude` (painel CPU).
2. Identificar processo/container causador:
   - `docker stats`
   - `Get-Process | Sort-Object CPU -Descending | Select-Object -First 10`
3. Verificar deploy recente/loop de erro.
4. Mitigar:
   - reduzir carga
   - escalar recursos
   - reiniciar servico afetado
5. Validar retorno abaixo de 80% por pelo menos 10 min.
