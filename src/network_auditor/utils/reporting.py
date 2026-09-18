import json
import os
from datetime import datetime

class AuditReporter:
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = output_dir
        self._ensure_output_dir()

    def _ensure_output_dir(self):
        """Garante que o diretório de relatórios exista."""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def export_json(self, data: list[dict], filename_prefix: str = "audit_report") -> str:
        """Exporta os resultados brutos em formato JSON estruturado."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = os.path.join(self.output_dir, f"{filename_prefix}_{timestamp}.json")

        report_payload = {
            "metadata": {
                "scan_date": datetime.now().isoformat(),
                "total_hosts_scanned": len(data)
            },
            "results": data
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(report_payload, f, indent=4, ensure_ascii=False)

        return filepath

    def export_txt(self, data: list[dict], filename_prefix: str = "audit_report") -> str:
        """Exporta um relatório textual formatado para leitura rápida."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = os.path.join(self.output_dir, f"{filename_prefix}_{timestamp}.txt")

        lines = [
            "=" * 60,
            "         RELATÓRIO DE VARREDURA E RECONHECIMENTO DE REDE",
            f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
            "=" * 60,
            ""
        ]

        for host_entry in data:
            ip = host_entry.get("ip", "Desconhecido")
            mac = host_entry.get("mac", "Desconhecido")
            details = host_entry.get("details", {})

            lines.append(f"[+] HOST: {ip}")
            lines.append(f"    MAC Address: {mac}")
            lines.append(f"    Sistema Operacional: {details.get('os', 'Não identificado')}")
            lines.append("    Serviços Detectados:")

            services = details.get("services", [])
            if services:
                for srv in services:
                    port = srv.get("port")
                    name = srv.get("name", "unkown")
                    product = srv.get("product", "")
                    version = srv.get("version", "")
                    lines.append(f"      - Porta {port}/TCP: {name} ({product} {version})".strip())
            else:
                lines.append("      - Nenhum serviço/porta aberta identificado.")

            lines.append("-" * 60)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        return filepath
