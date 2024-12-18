import socket
import os

def resolve_subdomain_to_ip(subdomain):
    """
    Resolve a subdomain to its IP address.
    """
    try:
        ip = socket.gethostbyname(subdomain)
        return ip
    except socket.gaierror:
        return None

def extract_unique_ips(subdomains):
    """
    Extract unique IPs for a list of subdomains.
    """
    unique_ips = set()
    for subdomain in subdomains:
        ip = resolve_subdomain_to_ip(subdomain)
        if ip:
            unique_ips.add(ip)
    return unique_ips

def save_ips_to_file(unique_ips, domain):
    """
    Save unique IPs to a file.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))


    file_name = os.path.join(script_dir, f"{domain}_ips.txt")
    with open(file_name, 'w') as f:
        for ip in unique_ips:
            f.write(f"{ip}\n")
    print(f"[+] Unique IPs saved to {file_name}")

def main():
    domain = input("[*] Enter the domain (e.g., example.com): ").strip()
    subdom_file = rf'D:\Old D Parti\Mine-Repos\gradProj\Recon\subdomains\{domain}_all_subdomains.txt'


    try:
        with open(subdom_file, 'r') as f:
            subdomains = [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        print(f"[-] The file {subdom_file} does not exist.")
        return

    unique_ips = extract_unique_ips(subdomains)

    save_ips_to_file(unique_ips, domain)

if __name__ == "__main__":
    main()