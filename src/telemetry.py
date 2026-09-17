import json
from datetime import datetime
from typing import Dict, Any, List
from src.config import TELEMETRY_LOG_PATH, settings


class TelemetryTracker:
    """
    Rastreador de telemetria e histórico local de prompts gerados.
    Registra parâmetros sorteados, carimbo de data/hora e mantém os últimos registros
    para consulta e análise no Streamlit conforme a Seção 5 e Seção 9 da Constituição V2.1.
    """

    def __init__(self, log_path=TELEMETRY_LOG_PATH, max_entries: int = settings.max_history_entries):
        self.log_path = log_path
        self.max_entries = max_entries

    def _read_logs(self) -> List[Dict[str, Any]]:
        if not self.log_path.exists():
            return []
        try:
            with open(self.log_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except Exception:
            return []

    def _write_logs(self, logs: List[Dict[str, Any]]) -> None:
        try:
            with open(self.log_path, "w", encoding="utf-8") as f:
                json.dump(logs, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def record_generation(self, combination: Dict[str, Any], prompt: str) -> None:
        """Grava uma nova geração de prompt no topo do histórico respeitando o limite máximo."""
        logs = self._read_logs()

        entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "tema": combination.get("macro_tema", {}).get("titulo", "N/A"),
            "persona": combination.get("persona", {}).get("nome", "N/A"),
            "bairro": combination.get("bairro", {}).get("nome", "N/A"),
            "formato": combination.get("formato", {}).get("nome", "N/A"),
            "tom": combination.get("tom", {}).get("nome", "N/A"),
            "ancora": combination.get("ancora", {}).get("conceito", "N/A"),
            "prompt": prompt,
        }

        # Insere no topo do histórico
        logs.insert(0, entry)

        # Trunca nos últimos registros configurados
        if len(logs) > self.max_entries:
            logs = logs[: self.max_entries]

        self._write_logs(logs)

    def get_recent_history(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Retorna os registros mais recentes de prompts gerados."""
        logs = self._read_logs()
        return logs[:limit]
