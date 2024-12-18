import nmap
import sys
import os

def scan_target(ip):
    scanner = nmap.PortScanner()
    open_ports = []

    try:
        print(f"Scanning IP: {ip}...")
        scanner.scan(ip, '1-1000', arguments='-O -sV')

        if scanner[ip].state() == 'up':
            print(f"\nHost {ip} is up.")
            
            if 'tcp' in scanner[ip]:
                print("Open Ports:")
                for port in scanner[ip]['tcp']:
                    port_info = scanner[ip]['tcp'][port]
                    service_name = port_info.get('name', 'unknown')
                    if service_name == "http-proxy":
                        service_name = "http" if port == 80 else "https"    
                    print(f"  Port {port}/TCP: {port_info['state']} ({service_name})")
                    open_ports.append(f"{service_name}({port})")
            
            # Display OS information
            if 'osmatch' in scanner[ip]:
                print("\nDetected Operating System(s):")
                for os in scanner[ip]['osmatch']:
                    print(f"  {os['name']}")
            else:
                print("\nNo OS information detected.")

            if open_ports:
                print("\nSummary of open ports:")
                print(f"You have {len(open_ports)} open port(s) and they are {', '.join(open_ports)}.")
        else:
            print(f"Host {ip} is down or unresponsive.")
    
    except Exception as e:
        print(f"An error occurred while scanning {ip}")

def main():
    target = input("Enter a single IP or the path to a file containing a list of IPs: ")

    if os.path.isfile(target):
        with open(target, 'r') as file:
            ips = file.readlines()
        ips = [ip.strip() for ip in ips if ip.strip()]
    else:
        ips = [target.strip()]

    for ip in ips:
        scan_target(ip)
        print("-" * 50)

if __name__ == "__main__":
    main()