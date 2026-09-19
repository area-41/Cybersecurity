import sys
from datetime import datetime
from scapy.all import sniff, IP, TCP, UDP, Raw

class NetworkTrafficMonitor:
    def __init__(self, interface: str = None):
        self.interface = interface

    def _process_packet(self, packet):
        """Processa e analisa cada pacote capturado na interface."""
        if not packet.haslayer(IP):
            return

        timestamp = datetime.now().isoformat()
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        proto = packet[IP].proto

        # Análise de Camada de Transporte (TCP/UDP)
        src_port = None
        dst_port = None

        if packet.haslayer(TCP):
            src_port = packet[TCP].sport
            dst_port = packet[TCP].dport
            proto_name = "TCP"
        elif packet.haslayer(UDP):
            src_port = packet[UDP].sport
            dst_port = packet[UDP].dport
            proto_name = "UDP"
        else:
            proto_name = f"IP_{proto}"

        # Exemplo de Detecção: Identificação de payload em texto claro em portas web
        payload_preview = ""
        if packet.haslayer(Raw):
            payload = packet[Raw].load
            # Tenta decodificar amostra do payload se for texto plano
            if dst_port in [80, 8080] or src_port in [80, 8080]:
                try:
                    payload_preview = payload[:50].decode('utf-8', errors='ignore').replace('\r\n', ' ')
                except Exception:
                    payload_preview = "<binary_data>"

        log_entry = (
            f"[{timestamp}] [{proto_name}] {src_ip}:{src_port} -> {dst_ip}:{dst_port} "
            f"| Payload Sample: {payload_preview}"
        )
        print(log_entry)

    def start_capture(self, packet_count: int = 0, bpf_filter: str = ""):
        """Inicia a escuta de pacotes com suporte a filtros BPF."""
        print(f"[*] Iniciando monitoramento de rede na interface: {self.interface or 'Padrão'}")
        print(f"[*] Filtro BPF aplicado: '{bpf_filter}'")
        
        sniff(
            iface=self.interface,
            prn=self._process_packet,
            filter=bpf_filter,
            store=False,
            count=packet_count
        )

if __name__ == "__main__":
    # Requer privilégios de Administrador/Root
    try:
        monitor = NetworkTrafficMonitor()
        # Captura apenas tráfego IP (pode ser ajustado conforme o filtro BPF)
        monitor.start_capture(bpf_filter="ip")
    except KeyboardInterrupt:
        print("\n[*] Monitoramento encerrado pelo usuário.")
    except PermissionError:
        print("[-] Erro: Execução requer privilégios de Administrador/Root.")
        sys.exit(1)
