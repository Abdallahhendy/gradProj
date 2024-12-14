import requests
import argparse
import csv
import os
from concurrent.futures import ThreadPoolExecutor  # For multithreading

# Enumerate subdomains using a wordlist
def enumerate_subdomains_wordlist(domain, wordlist):
    subdomains = []
    with open(wordlist, "r") as file:
        for line in file:
            subdomain = line.strip() + "." + domain
            subdomains.append(subdomain)
    return subdomains


# Check HTTP response for subdomains
def check_response(url, protocol="http"):
    try:
        # Allow redirects but don't follow them
        response = requests.get(f"{protocol}://{url}", timeout=5, allow_redirects=False)

        # Check for specific HTTP response codes
        if response.status_code in [200, 301, 302, 401, 403, 404]:
            print(f"Found {response.status_code} with {url}")
            return (url, response.status_code)
    except requests.exceptions.RequestException as e:
        print(f"Error with {url}: {e}")
    return None


# Save results to CSV files categorized by HTTP status code
def save_to_csv_by_status(results, domain):
    # Ensure the output directory exists
    output_dir = "results_by_status"
    os.makedirs(output_dir, exist_ok=True)

    # Organize results by status code
    results_by_status = {}
    for result in results:
        status_code = result[1]
        if status_code not in results_by_status:
            results_by_status[status_code] = []
        results_by_status[status_code].append(result)

    # Write results to separate CSV files based on status code
    for status_code, entries in results_by_status.items():
        file_name = f"{domain.split('.')[0]}_{status_code}.csv"
        file_path = os.path.join(output_dir, file_name)
        with open(file_path, mode="a", newline="") as file:
            writer = csv.writer(file)
            for entry in entries:
                writer.writerow([entry[0]])


# Handle multithreaded processing of subdomains
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
    parser = argparse.ArgumentParser(description="Subdomain Enumerator using wordlist")
    parser.add_argument("domain", help="Target domain (e.g., example.com)")
    parser.add_argument("--wordlist", help="Path to subdomain wordlist", required=True)
    parser.add_argument("--https", action="store_true", help="Check HTTPS instead of HTTP")
    parser.add_argument("--threads", type=int, default=50, help="Number of threads to use (default: 50)")
    args = parser.parse_args()

    protocol = "https"
    print(f"[*] Enumerating subdomains using wordlist with {args.threads} threads...")
    subdomains = enumerate_subdomains_wordlist(args.domain, args.wordlist)

    print(f"[*] Found {len(subdomains)} subdomains. Checking responses using {args.threads} threads...")
    results = process_subdomains(subdomains, protocol, args.threads)

    # Save results to separate CSV files based on status code
    save_to_csv_by_status(results, args.domain)
    print("[*] Results saved in 'results_by_status' directory.")


if __name__ == "__main__":
    main()
