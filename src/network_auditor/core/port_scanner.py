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
