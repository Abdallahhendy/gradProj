import requests
import argparse
import csv
import os
from concurrent.futures import ThreadPoolExecutor

# Enumerate subdomains using SecurityTrails API
def enumerate_subdomains_securitytrails(api_key, domain):
    subdomains = []
    url = f"https://api.securitytrails.com/v1/domain/{domain}/subdomains"
    headers = {
        "Content-Type": "application/json",
        "APIKEY": api_key
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            subdomains = [f"{sub}.{domain}" for sub in data.get("subdomains", [])]
        else:
            print(f"Error fetching data from SecurityTrails: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error with SecurityTrails API: {e}")
    return subdomains

# Check HTTP responses for the given subdomains
def check_response(url, protocol="http"):
    try:
        response = requests.get(f"{protocol}://{url}", timeout=5, allow_redirects=False)
        if response.status_code in [200, 301, 302, 401, 403, 404]:
            print(f"Found {response.status_code} with {url}")
            return (url, response.status_code)
    except requests.exceptions.RequestException as e:
        print(f"Error with {url}: {e}")
    return None

# Save results into CSV files grouped by HTTP status codes
def save_to_csv_by_status(results, domain):
    output_dir = "results_by_status"
    os.makedirs(output_dir, exist_ok=True)

    results_by_status = {}
    for result in results:
        status_code = result[1]
        if status_code not in results_by_status:
            results_by_status[status_code] = []
        results_by_status[status_code].append(result)

    for status_code, entries in results_by_status.items():
        file_name = f"{domain.split('.')[0]}_{status_code}.csv"
        file_path = os.path.join(output_dir, file_name)
        with open(file_path, mode="a", newline="") as file:
            writer = csv.writer(file)
            for entry in entries:
                writer.writerow([entry[0]])

# Process subdomains using multithreading
def process_subdomains(subdomains, protocol, max_threads):
    results = []
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [executor.submit(check_response, subdomain, protocol) for subdomain in subdomains]
        for future in futures:
            result = future.result()
            if result:
                results.append(result)
    return results

def main():
    parser = argparse.ArgumentParser(description="Subdomain Enumerator using SecurityTrails API")
    parser.add_argument("domain", help="Target domain (e.g., example.com)")
    parser.add_argument("--api-key", help="SecurityTrails API key", required=True)
    parser.add_argument("--https", action="store_true", help="Check HTTPS instead of HTTP")
    parser.add_argument("--threads", type=int, default=50, help="Number of threads to use (default: 50)")
    args = parser.parse_args()

    protocol = "https"
    print("[*] Enumerating subdomains using SecurityTrails API...")
    subdomains = enumerate_subdomains_securitytrails(args.api_key, args.domain)

    if subdomains:
        print(f"[*] Found {len(subdomains)} subdomains. Checking responses using {args.threads} threads...")
        results = process_subdomains(subdomains, protocol, args.threads)

        save_to_csv_by_status(results, args.domain)
        print("[*] Results saved in 'results_by_status' directory.")
    else:
        print("[!] No subdomains found.")

if __name__ == "__main__":
    main()
