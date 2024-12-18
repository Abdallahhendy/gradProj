import os
import requests
import socket
import re
import csv

def add_protocol(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        return "https://" + url
    return url

def is_resolvable(domain):
    try:
        hostname = domain.replace("http://", "").replace("https://", "").split('/')[0]
        socket.gethostbyname(hostname)
        return True
    except socket.gaierror:
        return False

def extract_endpoints_and_queries(subdomains_file, domain):
    endpoint_regex = r"(https?://[^\s\"'<>]+)"
    query_endpoints = []
    normal_endpoints = []

    subdomains = []
    try:
        with open(subdomains_file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row:
                    subdomains.append(row[0].strip())
    except Exception as e:
        print(f"[ERROR] Failed to read subdomains file: {e}")
        return

    for subdomain in subdomains:
        subdomain = add_protocol(subdomain)
        if not is_resolvable(subdomain):
            # print(f"[SKIPPED] {subdomain} is not resolvable.")
            continue

        try:
            response = requests.get(subdomain, timeout=10)
            if response.status_code == 200:
                print(f"Processing {subdomain}...")

                links = re.findall(endpoint_regex, response.text)

                for link in links:
                    if "?" in link:
                        query_endpoints.append(link)
                    else:
                        normal_endpoints.append(link)

        except Exception as e:
            # print(f"Error processing {subdomain}: {e}")
            continue

    query_endpoints = list(set(query_endpoints))
    normal_endpoints = list(set(normal_endpoints))

    project_dir = os.path.dirname(os.path.abspath(__file__))
    query_filename = os.path.join(project_dir, f"{domain}_params.txt")
    normal_filename = os.path.join(project_dir, f"{domain}_endpoints.txt")

    with open(query_filename, 'w', encoding='utf-8') as output:
        output.write('\n'.join(query_endpoints))

    with open(normal_filename, 'w', encoding='utf-8') as output:
        output.write('\n'.join(normal_endpoints))

    print(f"Saved query endpoints to {query_filename}")
    print(f"Saved normal endpoints to {normal_filename}")

def search_for_file(target):
    """
    Search for a file in the entire project folder that matches the pattern {target}_all_subdomains.txt
    """
    target_file_name = f"{target}_all_subdomains.txt"
    
    for root, dirs, files in os.walk(os.getcwd()):  # Walk through all files and folders in the current directory
        if target_file_name in files:
            file_path = os.path.join(root, target_file_name)
            print(f"[+] Found file: {file_path}")
            return file_path
    
    print(f"[-] File {target_file_name} not found in the project.")
    return None

def main():
    domain = input("[*] Enter the domain (e.g., example.com): ").strip()
    result_file = search_for_file(domain)
    if not result_file:
        return 

    extract_endpoints_and_queries(result_file, domain)
     
if __name__ == "__main__":
    main()