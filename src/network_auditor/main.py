import sys
from core.host_discovery import HostDiscovery
from core.port_scanner import PortScanner
from core.nmap_auditor import NmapAuditor
from utils.reporting import AuditReporter

def main():
    target_subnet = "192.168.1.0/24"
    common_ports = [21, 22, 80, 443, 445, 8080]
    audit_results = []

    print(f"[*] Iniciando Descoberta na sub-rede: {target_subnet}")
    discovery = HostDiscovery(target_subnet)
    hosts = discovery.scan_arp()
    
    print(f"[+] Hosts encontrados: {len(hosts)}")
    
    auditor = NmapAuditor()

    for host in hosts:
        ip = host["ip"]
        mac = host["mac"]
        print(f"\n--- Analisando Host: {ip} ({mac}) ---")
        
        # 1. Varredura de Portas via Socket
        scanner = PortScanner(ip)
        open_ports = scanner.scan_ports(common_ports)
        print(f"[+] Portas TCP Abertas: {open_ports}")

        # 2. Impressão Digital via Nmap
        details = {}
        if open_ports:
            print("[*] Identificando serviços e SO com Nmap...")
            details = auditor.audit_target(ip, open_ports)

        # 3. Consolida dados do Host
        audit_results.append({
            "ip": ip,
            "mac": mac,
            "details": details
        })

    # 4. Geração dos Relatórios
    print("\n[*] Gerando relatórios finais...")
    reporter = AuditReporter(output_dir="reports")
    
    json_path = reporter.export_json(audit_results)
    txt_path = reporter.export_txt(audit_results)

    print(f"[+] Relatório JSON salvo em: {json_path}")
    print(f"[+] Relatório TXT salvo em: {txt_path}")

if __name__ == "__main__":
    try:
        main()
    except PermissionError:
        print("[-] Erro: Execute o script com privilégios de Administrador/Root.")
        sys.exit(1)
