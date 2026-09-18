import nmap

class NmapAuditor:
    def __init__(self):
        self.nm = nmap.PortScanner()

    def audit_target(self, target_ip: str, ports: list[int]) -> dict:
        """Executa scan avançado (Banner Grabbing/OS) em portas específicas."""
        if not ports:
            return {}

        ports_str = ",".join(map(str, ports))
        # -sV: Versão do Serviço | -O: Detecção de SO
        self.nm.scan(hosts=target_ip, ports=ports_str, arguments="-sV -O")

        audit_data = {}
        if target_ip in self.nm.all_hosts():
            host = self.nm[target_ip]
            audit_data["status"] = host.state()
            
            # Captura SO se disponível
            if "osmatch" in host and host["osmatch"]:
                audit_data["os"] = host["osmatch"][0]["name"]

            audit_data["services"] = []
            for proto in host.all_protocols():
                lports = host[proto].keys()
                for port in lports:
                    service_info = host[proto][port]
                    audit_data["services"].append({
                        "port": port,
                        "name": service_info.get("name"),
                        "product": service_info.get("product"),
                        "version": service_info.get("version")
                    })

        return audit_data
