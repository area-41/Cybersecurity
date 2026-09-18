 Projeto profissional de auditoria de redes em Python, com uma arquitetura modular orientada a objetos. Essa estrutura separa a lógica de execução da interface, facilitando a manutenção e a reutilização do código em ambientes de *Red Teaming* ou defesa cibernética.

### Arquitetura do Projeto

```text
network_auditor/
│
├── core/
│   ├── __init__.py
│   ├── host_discovery.py   # Mapeamento ARP/ICMP via Scapy
│   ├── port_scanner.py     # Varredura multithreaded via Socket
│   └── nmap_auditor.py     # Detecção de serviços e OS via python-nmap
│
├── utils/
│   ├── __init__.py
│   └── reporting.py        # Exportação de resultados em JSON/Texto
│
├── requirements.txt
└── main.py                 # Ponto de entrada (CLI)

```

### Dependências (requirements.txt)

```text
scapy>=2.5.0
python-nmap>=0.7.1

```

> **Nota:** O python-nmap exige que o executável do **Nmap** esteja instalado no sistema operacional host. Além disso, a biblioteca scapy requer privilégios de administrador/root para criar e manipular pacotes na camada de enlace/rede.
> 
### Módulos do Sistema
#### 1. Descoberta de Hosts (core/host_discovery.py)
Utiliza o **Scapy** para enviar requisições ARP na rede local, identificando endereços IP e MAC ativos.

```python
from scapy.all import ARP, Ether, srp

class HostDiscovery:
    def __init__(self, target_range: str):
        self.target_range = target_range

    def scan_arp(self) -> list[dict]:
        """Realiza descoberta de hosts via ARP Request."""
        # Cria um pacote Ether + ARP
        arp_request = ARP(pdst=self.target_range)
        broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = broadcast / arp_request

        # Envia e recebe pacotes na Camada 2
        answered_list = srp(packet, timeout=2, verbose=False)[0]

        discovered_hosts = []
        for element in answered_list:
            discovered_hosts.append({
                "ip": element[1].psrc,
                "mac": element[1].hwsrc
            })
        return discovered_hosts

```

#### 2. Varredura de Portas Multithreaded (core/port_scanner.py)

Utiliza a biblioteca nativa socket com suporte a threads para verificar conexões TCP de forma rápida.

```python
import socket
from concurrent.futures import ThreadPoolExecutor

class PortScanner:
    def __init__(self, target_ip: str, timeout: float = 1.0):
        self.target_ip = target_ip
        self.timeout = timeout

    def _check_port(self, port: int) -> int | None:
        """Tenta abrir uma conexão TCP Socket com a porta estipulada."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(self.timeout)
            result = s.connect_ex((self.target_ip, port))
            if result == 0:
                return port
        return None

    def scan_ports(self, ports: list[int], max_workers: int = 100) -> list[int]:
        """Executa a verificação de portas em paralelo."""
        open_ports = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = executor.map(self._check_port, ports)
            for port in results:
                if port:
                    open_ports.append(port)
        return sorted(open_ports)

```

#### 3. Impressão Digital e Serviços (core/nmap_auditor.py)

Aplica o python-nmap sobre portas identificadas para obter a versão exata do serviço e o sistema operacional subjacente.

```python
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

```

#### 4. Arquivo Principal (main.py)

Combina os módulos em um fluxo sequencial configurável.

```python
import sys
import json
from core.host_discovery import HostDiscovery
from core.port_scanner import PortScanner
from core.nmap_auditor import NmapAuditor

def main():
    target_subnet = "192.168.1.0/24"
    common_ports = [21, 22, 80, 443, 445, 8080]

    print(f"[*] Iniciando Descoberta na sub-rede: {target_subnet}")
    discovery = HostDiscovery(target_subnet)
    hosts = discovery.scan_arp()
    
    print(f"[+] Hosts encontrados: {len(hosts)}")
    for host in hosts:
        ip = host["ip"]
        print(f"\n--- Analisando Host: {ip} ({host['mac']}) ---")
        
        # 1. Varredura Rápida de Portas via Sockets
        scanner = PortScanner(ip)
        open_ports = scanner.scan_ports(common_ports)
        print(f"[+] Portas TCP Abertas: {open_ports}")

        # 2. Impressão Digital detalhada com Nmap
        if open_ports:
            print("[*] Identificando serviços e SO com Nmap...")
            auditor = NmapAuditor()
            details = auditor.audit_target(ip, open_ports)
            print(json.dumps(details, indent=2))

if __name__ == "__main__":
    # Exemplo exige execução como administrador/root devido ao Scapy e Nmap -O
    try:
        main()
    except PermissionError:
        print("[-] Erro: Execute o script com privilégios de Administrador/Root.")
        sys.exit(1)

```

### Execução

Para rodar a ferramenta em ambientes Linux/macOS:

```bash
sudo python3 main.py

```

No Windows, abra o *Prompt de Comando* ou *PowerShell* como **Administrador** antes de rodar o comando.
