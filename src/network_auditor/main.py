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
