import requests
import argparse
import csv
import os
from concurrent.futures import ThreadPoolExecutor

# Enumerate subdomains using crt.sh
def enumerate_subdomains_crtsh(domain):
    subdomains = set()
    url = f"https://crt.sh/?q=%.{domain}&output=json"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            for entry in data:
                name = entry.get("name_value")
                if name:
                    subdomains.update(name.split("\n"))  # Add subdomains
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from crt.sh: {e}")
    return list(subdomains)

# Check the HTTP response for the given subdomain
def check_response(url, protocol="http"):
    try:
        response = requests.get(f"{protocol}://{url}", timeout=20, allow_redirects=False)
        if response.status_code in [200, 301, 302, 401, 403, 404]:  # Check for valid status codes
            print(f"Found {response.status_code} with {url}")
            return (url, response.status_code)
    except requests.exceptions.RequestException as e:
        print(f"Error with {url}: {e}")
    return None

# Save results to CSV files categorized by HTTP status code
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
    parser = argparse.ArgumentParser(description="Subdomain Enumerator using crt.sh")
    parser.add_argument("domain", help="Target domain (e.g., example.com)")
    parser.add_argument("--https", action="store_true", help="Check HTTPS instead of HTTP")
    parser.add_argument("--threads", type=int, default=50, help="Number of threads to use (default: 50)")
    args = parser.parse_args()

    protocol = "https"
    print("[*] Enumerating subdomains using crt.sh...")
    subdomains = enumerate_subdomains_crtsh(args.domain)

    print(f"[*] Found {len(subdomains)} subdomains. Checking responses using {args.threads} threads...")
    results = process_subdomains(subdomains, protocol, args.threads)

    save_to_csv_by_status(results, args.domain)
    print("[*] Results saved in 'results_by_status' directory.")

if __name__ == "__main__":
    main()
