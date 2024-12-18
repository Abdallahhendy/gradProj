import os
import subprocess

def run_subdomain_tools(domain, output_directory):
    """
    Orchestrates The subdomain enum
    """
    subdomains_file = rf'D:\Old D Parti\Mine-Repos\gradProj\Recon\subdomains\{domain}_all_subdomains.txt'
    
    script_path = r'D:\Old D Parti\Mine-Repos\gradProj\Recon\subdomains\run_all_enum.py'
    
    subprocess.run(['python', script_path, domain], check=True)
    
    
    if os.path.exists(subdomains_file):
        with open(subdomains_file, 'r') as f:
            subdomains = [line.strip() for line in f.readlines()]
    else:
        print(f"[!] File {subdomains_file} not found.")
        return []

    return sorted(set(subdomains))


def collect_ips_from_subdomains(subdomains_file, output_directory):
    """
    Collects unique IPs for each subdomain.
    """
    ip_collector_script = r'D:\Old D Parti\Mine-Repos\gradProj\Recon\ips_collector\ips.py'
    
    subprocess.run(['python', ip_collector_script, str(subdomains_file), str(output_directory)], check=True)
    

def run_port_scanner(domain, output_directory):
    """
    Runs the port scanner script.
    """
    port_scanner_script = r'D:\Old D Parti\Mine-Repos\gradProj\Recon\portScanner\python_scanner.py'
    ips_file = os.path.join(r'D:\Old D Parti\Mine-Repos\gradProj\Recon\ips_collector', f'{domain}_ips.txt')

        
    with open(ips_file, 'r') as file:
        ips = [line.strip() for line in file.readlines() if line.strip()]
    
    subprocess.run(['python', port_scanner_script, *ips_file, output_directory], check=True)


def main():
    domain = input("[*] Enter the target domain: ").strip()

    output_directory = os.path.join('D:/Old D Parti/Mine-Repos/gradProj/Recon/', domain)
    os.makedirs(output_directory, exist_ok=True)

    subdomains = run_subdomain_tools(domain, output_directory)
    print(f"[+] Subdomain Enumeration Complete. Found {len(subdomains)} subdomains.")
    
    print("[*] Collecting IPs for the subdomains...")
    ips = collect_ips_from_subdomains(subdomains, output_directory)
    
    print("[*] Starting Port Scanning...")
    run_port_scanner(domain, output_directory)
    
    print(f"[+] Port Scanning completed for {domain}.")


    # Step 4: Security Headers Check (Optional step, can be added later)
    # check_security_headers(subdomains)  # Add functionality as needed


if __name__ == "__main__":
    main()
