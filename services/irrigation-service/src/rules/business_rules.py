from datetime import timedelta

from src.models.irrigation_model import IrrigationContext


class IrrigationRules:
    HORARIOS_PERMITIDOS = [(5, 9), (18, 21)]
    DURACAO_MAXIMA_MIN = 60
    INTERVALO_MINIMO_HORAS = 4
    THRESHOLD_CHUVA_MM = 5.0
    UMIDADE_MINIMA_PCT = 40.0

    def _horario_permitido(self, hour: int) -> bool:
        for start, end in self.HORARIOS_PERMITIDOS:
            if start <= hour <= end:
                return True
        return False

    def pode_irrigar(self, contexto: IrrigationContext) -> tuple[bool, str]:
        if contexto.umidade_pct >= self.UMIDADE_MINIMA_PCT:
            return False, "umidade_adequada"

        if contexto.chuva_prevista_mm > self.THRESHOLD_CHUVA_MM:
            return False, "chuva_prevista_acima_limite"

        if not self._horario_permitido(contexto.now.hour):
            return False, "fora_horario_permitido"

        if contexto.ultima_irrigacao is not None:
            delta = contexto.now - contexto.ultima_irrigacao
            if delta < timedelta(hours=self.INTERVALO_MINIMO_HORAS):
                return False, "intervalo_minimo_nao_respeitado"

        if contexto.duracao_sugerida_min > self.DURACAO_MAXIMA_MIN:
            return False, "duracao_acima_limite"

        return True, "ok"
