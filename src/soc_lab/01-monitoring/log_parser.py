import json
import re
from datetime import datetime
from pathlib import Path

class LogCollectorAndParser:
    def __init__(self):
        # Padrão regex simples para logs no formato Apache/Nginx Common Log Format
        self.log_pattern = re.compile(
            r'(?P<client_ip>\d+\.\d+\.\d+\.\d+)\s+-\s+-\s+\[(?P<timestamp>[^\]]+)\]\s+"(?P<method>\A\S+|\S+)\s+(?P<path>\S+)\s+(?P<protocol>[^"]+)"\s+(?P<status_code>\d+)\s+(?P<bytes_sent>\d+|-)'
        )

    def parse_line(self, line: str) -> dict | None:
        """Converte uma linha de log bruto para uma estrutura normalizada."""
        match = self.log_pattern.match(line)
        if not match:
            return None

        data = match.groupdict()
        
        # Normalização de dados (Esquema simplificado)
        normalized_event = {
            "@timestamp": datetime.now().isoformat(),
            "source": {
                "ip": data["client_ip"]
            },
            "http": {
                "request": {
                    "method": data["method"],
                    "referrer": data["path"]
                },
                "response": {
                    "status_code": int(data["status_code"]),
                    "bytes": int(data["bytes_sent"]) if data["bytes_sent"] != '-' else 0
                }
            },
            "event": {
                "kind": "event",
                "category": ["web"],
                "type": ["access"]
            }
        }
        return normalized_event

    def process_log_file(self, file_path: str) -> list[dict]:
        """Lê um arquivo de log e retorna os eventos normalizados."""
        path = Path(file_path)
        if not path.exists():
            print(f"[-] Arquivo não encontrado: {file_path}")
            return []

        parsed_events = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                event = self.parse_line(line.strip())
                if event:
                    parsed_events.append(event)
        
        return parsed_events

if __name__ == "__main__":
    # Exemplo de uso com dados simulados
    sample_logs = [
        '192.168.1.50 - - [18/Sep/2026:14:32:10 +0000] "GET /admin/login HTTP/1.1" 200 5120',
        '10.0.0.15 - - [18/Sep/2026:14:32:11 +0000] "POST /api/v1/data HTTP/1.1" 403 128',
        '172.16.0.4 - - [18/Sep/2026:14:32:12 +0000] "GET /index.html HTTP/1.1" 200 2048'
    ]

    parser = LogCollectorAndParser()
    events = []

    print("[*] Normalizando entradas de log de exemplo...")
    for raw_line in sample_logs:
        parsed = parser.parse_line(raw_line)
        if parsed:
            events.append(parsed)

    # Exibe o resultado da normalização em JSON
    print(json.dumps(events, indent=2, ensure_ascii=False))
