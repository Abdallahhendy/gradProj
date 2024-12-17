# import subprocess
# import requests
# import os
# import re

# sublister_full_path = r"C:\Users\Softlaptop\Sublist3r"

# def run_sublist3r(domain):
#     """
#     Run Sublist3r to enumerate subdomains for a given domain.
#     """
#     sublist3r_script = os.path.join(sublister_full_path, 'sublist3r.py')

#     print(f"[*] Running Sublist3r for {domain}...\n")
#     result = subprocess.run(
#         ['python', sublist3r_script, '-d', domain],
#         stderr=subprocess.PIPE,
#         stdout=subprocess.PIPE
#     )
    
#     if result.returncode != 0:
#         print("[!] Sublist3r failed with error:", result.stderr.decode())
#         return []
    
#     output = result.stdout.decode().strip().splitlines()
#     return output

# def check_status_code(subdomain):
#     """
#     Check the HTTP/HTTPS status code of a subdomain using requests.
#     Tries both HTTP and HTTPS protocols.
#     """
#     http_url = f"http://{subdomain}"
#     https_url = f"https://{subdomain}"

#     try:
#         # Try HTTP first
#         response = requests.get(http_url, timeout=5)
#         return response.status_code, 'http'
#     except requests.exceptions.RequestException:
#         pass

#     try:
#         # Try HTTPS if HTTP fails
#         response = requests.get(https_url, timeout=5)
#         return response.status_code, 'https'
#     except requests.exceptions.RequestException:
#         return None, None

# def is_valid_subdomain(subdomain):
#     """
#     Validate if a given subdomain is in the correct format.
#     """
#     subdomain_regex = re.compile(
#         r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)\.(?:[A-Za-z]{2,6}|[A-Za-z0-9-]{2,}\.[A-Za-z]{2,6})$"
#     )
#     return subdomain_regex.match(subdomain)

# def save_status_codes(subdomains, domain):
#     """
#     Save subdomains into separate files based on their HTTP status codes.
#     """
#     print("[*] Checking status codes for subdomains...")
#     status_codes = {'200': [], '403': [], '500': [], 'other': []}
    
#     for subdomain in subdomains:
#         # Sanitize and validate subdomain
#         if not is_valid_subdomain(subdomain):
#             print(f"[!] Skipping invalid subdomain: {subdomain}")
#             continue
        
#         for protocol in ['http', 'https']:
#             try:
#                 url = f"{protocol}://{subdomain}"
#                 response = requests.head(url, timeout=5)
#                 code = str(response.status_code)
#                 if code in status_codes:
#                     status_codes[code].append(f"{subdomain} ({protocol.upper()})")
#                 else:
#                     status_codes['other'].append(f"{subdomain} ({protocol.upper()})")
#             except requests.RequestException:
#                 # Handle subdomain with no response
#                 status_codes['other'].append(f"{subdomain} ({protocol.upper()})")

#     script_dir = os.path.dirname(os.path.abspath(__file__))  # Get script directory
#     for code, subdomains in status_codes.items():
#         output_file = os.path.join(script_dir, f"{domain}_{code}.txt")
#         with open(output_file, 'w') as file:
#             for subdomain in subdomains:
#                 file.write(f"{subdomain}\n")
#         print(f"[*] {len(subdomains)} subdomains saved in {output_file}.")

# def merge_and_deduplicate(sublist3r_subdomains, brute_force_subdomains):
#     """
#     Merge Sublist3r and brute-force subdomains and remove duplicates.
#     """
#     all_subdomains = set(sublist3r_subdomains + brute_force_subdomains)
#     return list(all_subdomains)

# def main():
#     domain = input("Enter the target domain: ").strip()
    
#     # Run Sublist3r and brute-force subdomain enumeration
#     sublist3r_subdomains = run_sublist3r(domain)
#     wordlist_path = os.path.join(os.path.dirname(__file__), "wordlist.txt")
#     brute_force_subdomains = [subdomain.strip() for subdomain in open(wordlist_path).readlines()]
    
#     all_subdomains = merge_and_deduplicate(sublist3r_subdomains, brute_force_subdomains)

#     print(f"[*] Found {len(all_subdomains)} unique subdomains.")
    
#     script_dir = os.path.dirname(os.path.abspath(__file__))
#     final_output_file = os.path.join(script_dir, f"{domain}_final_subdomains.txt")
#     with open(final_output_file, 'w') as file:
#         for subdomain in sorted(all_subdomains):
#             file.write(f"{subdomain}\n")
#     print(f"[*] Final subdomains saved to {final_output_file}.")

#     save_status_codes(all_subdomains, domain)

# if __name__ == "__main__":
#     main()
# ================================================================================================================================

import os
import subprocess
import re

sublister_full_path = r"C:\Users\Softlaptop\Sublist3r"

def run_sublister(domain):
    """
    Run Sublist3r and extract subdomains.
    """
    print("[*] Running Sublist3r...")
    try:
        sublist3r_script = os.path.join(sublister_full_path, 'sublist3r.py')
        result = subprocess.run(
            ["python", sublist3r_script, "-d", domain],
            capture_output=True,
            text=True,
            check=True,
        )
        output = result.stdout
        subdomains = extract_subdomains(output)
        print(f"[+] Sublist3r found {len(subdomains)} subdomains.")
        return subdomains
    except subprocess.CalledProcessError as e:
        print(f"[!] Error running Sublist3r: {e}")
        return []


def run_bruteforce(domain):
    """
    Run the brute force tool and extract subdomains.
    """
    print("[*] Running brute-force subdomain enumeration...")
    try:
        bruteforcer_script = os.path.join(sublister_full_path, 'sublist3r.py')
        result = subprocess.run(
            ["python", bruteforcer_script, domain],
            capture_output=True,
            text=True,
            check=True,
        )
        output = result.stdout
        subdomains = extract_subdomains(output)
        print(f"[+] Bruteforcer found {len(subdomains)} subdomains.")
        return subdomains
    except subprocess.CalledProcessError as e:
        print(f"[!] Error running bruteforce tool: {e}")
        return []


def extract_subdomains(output):
    """
    Extract valid subdomains from a tool's output using regex.
    """
    # Regex to match valid subdomains
    subdomain_regex = re.compile(
        r"\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b"
    )
    return subdomain_regex.findall(output)


def save_final_subdomains(domain, all_subdomains):
    """
    Save the combined, deduplicated list of subdomains to a file.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Get script directory
    final_output_file = os.path.join(script_dir, f"{domain}_all_subdomains.txt")
    
    unique_subdomains = sorted(set(all_subdomains))

    with open(final_output_file, 'w') as file:
        for subdomain in unique_subdomains:
            file.write(f"{subdomain}\n")
    print(f"[+] Final subdomains saved to {final_output_file}.")
    return final_output_file


def main():
    """
    Main function to orchestrate Sublist3r and bruteforcer, 
    combine their results, and save them in a file.
    """
    domain = input("[*] Enter the target domain (e.g., example.com): ").strip()

    bruteforce_subdomains = run_bruteforce(domain)
    sublist3r_subdomains = run_sublister(domain)

    all_subdomains = sublist3r_subdomains + bruteforce_subdomains
    print(f"[+] Total unique subdomains found: {len(set(all_subdomains))}")

    save_final_subdomains(domain, all_subdomains)


if __name__ == "__main__":
    main()
