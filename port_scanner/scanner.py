#!/usr/bin/env python3

import argparse
import json
import socket
import csv
import concurrent.futures
from typing import List, Dict, Tuple, Union
import ipaddress
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ScanResult:
    host: str
    port: int
    is_open: bool
    service: str = ""
    banner: str = ""
    scan_time: str = ""

class PortScanner:
    COMMON_PORTS = {
        20: "FTP",
        21: "FTP",
        22: "SSH",
        23: "Telnet",
        25: "SMTP",
        53: "DNS",
        80: "HTTP",
        110: "POP3",
        143: "IMAP",
        443: "HTTPS",
        445: "SMB",
        3306: "MySQL",
        3389: "RDP",
        5432: "PostgreSQL",
        8080: "HTTP-Proxy"
    }

    def __init__(self, timeout: float = 1.0, threads: int = 100):
        self.timeout = timeout
        self.threads = threads
        self.results: List[ScanResult] = []

    @staticmethod
    def parse_ports(port_input: str) -> List[int]:
        """Parse port ranges and individual ports from a string."""
        ports = set()
        for part in port_input.split(','):
            part = part.strip()
            if '-' in part:
                start, end = map(int, part.split('-'))
                ports.update(range(start, end + 1))
            else:
                if part:  # Skip empty strings
                    ports.add(int(part))
        return sorted(ports)

    @staticmethod
    def is_valid_host(host: str) -> bool:
        """Check if the host is a valid IP or hostname."""
        try:
            # Try to parse as IP address
            ipaddress.ip_address(host)
            return True
        except ValueError:
            # If not an IP, check if it's a valid hostname
            try:
                socket.gethostbyname(host)
                return True
            except socket.gaierror:
                return False

    def scan_port(self, host: str, port: int) -> ScanResult:
        """Scan a single port on a host."""
        result = ScanResult(host=host, port=port, is_open=False)
        result.scan_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(self.timeout)
                result.is_open = sock.connect_ex((host, port)) == 0
                
                if result.is_open and port in self.COMMON_PORTS:
                    result.service = self.COMMON_PORTS[port]
                    try:
                        sock.send(b"GET / HTTP/1.1\r\n\r\n")
                        banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                        if banner:
                            result.banner = banner.split('\n')[0]  # Get first line of banner
                    except (socket.timeout, socket.error):
                        pass
                        
        except (socket.timeout, socket.error, socket.gaierror):
            pass
            
        return result

    def scan_host(self, host: str, ports: List[int]) -> None:
        """Scan multiple ports on a single host using thread pool."""
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.threads) as executor:
            future_to_port = {
                executor.submit(self.scan_port, host, port): port 
                for port in ports
            }
            
            for future in concurrent.futures.as_completed(future_to_port):
                result = future.result()
                if result.is_open:
                    self.results.append(result)
                    print(f"[+] {result.host}:{result.port} ({result.service or 'unknown'}) is open")
                    if result.banner:
                        print(f"    Banner: {result.banner}")

    def scan_hosts(self, hosts: List[str], ports: List[int]) -> None:
        """Scan multiple hosts."""
        for host in hosts:
            print(f"\nScanning {host}...")
            self.scan_host(host, ports)

    def to_json(self, filename: str) -> None:
        """Save scan results to a JSON file."""
        with open(filename, 'w') as f:
            json.dump([{
                'host': r.host,
                'port': r.port,
                'service': r.service,
                'banner': r.banner,
                'scan_time': r.scan_time
            } for r in self.results], f, indent=2)

    def to_csv(self, filename: str) -> None:
        """Save scan results to a CSV file."""
        if not self.results:
            return
            
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['host', 'port', 'service', 'banner', 'scan_time'])
            writer.writeheader()
            for result in self.results:
                writer.writerow({
                    'host': result.host,
                    'port': result.port,
                    'service': result.service,
                    'banner': result.banner,
                    'scan_time': result.scan_time
                })

def parse_arguments():
    parser = argparse.ArgumentParser(description='Port Scanner')
    parser.add_argument('-t', '--target', required=True, 
                      help='Target IP(s) or hostname(s), comma-separated')
    parser.add_argument('-p', '--ports', required=True,
                      help='Port range (e.g., 20-80) or specific ports (e.g., 22,80,443)')
    parser.add_argument('-o', '--output', help='Output base name for results (without extension)')
    parser.add_argument('--timeout', type=float, default=1.0,
                      help='Connection timeout in seconds (default: 1.0)')
    parser.add_argument('--threads', type=int, default=100,
                      help='Number of threads (default: 100)')
    return parser.parse_args()

def main():
    args = parse_arguments()
    
    # Parse targets
    targets = [t.strip() for t in args.target.split(',') if t.strip()]
    
    # Validate targets
    invalid_targets = [t for t in targets if not PortScanner.is_valid_host(t)]
    if invalid_targets:
        print(f"Error: Invalid target(s): {', '.join(invalid_targets)}")
        return
    
    # Parse ports
    try:
        ports = PortScanner.parse_ports(args.ports)
    except ValueError as e:
        print(f"Error: {e}")
        return
    
    if not ports:
        print("Error: No valid ports specified")
        return
    
    print(f"Starting scan on {len(targets)} target(s) with {len(ports)} port(s)")
    print("Press Ctrl+C to stop the scan\n")
    
    scanner = PortScanner(timeout=args.timeout, threads=args.threads)
    
    try:
        scanner.scan_hosts(targets, ports)
        
        # Output results
        if args.output:
            json_file = f"{args.output}.json"
            csv_file = f"{args.output}.csv"
            
            scanner.to_json(json_file)
            scanner.to_csv(csv_file)
            
            print(f"\nScan results saved to {json_file} and {csv_file}")
        
        print("\nScan completed!")
        
    except KeyboardInterrupt:
        print("\nScan interrupted by user")
    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    main()
