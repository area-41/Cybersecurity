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
