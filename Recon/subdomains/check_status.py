import os
import requests

def check_status_code(url):
    """
    Check the HTTP status code of a URL.
    """
    try:
        response = requests.get(url, timeout=5)
        return response.status_code
    except requests.exceptions.RequestException:
        return None


def group_subdomains_by_status(input_file, target_name):
    """
    Read subdomains from a file, check their HTTP status codes,
    and save each group of subdomains by status code into separate files.
    """
    if not os.path.isfile(input_file):
        print(f"Input file {input_file} does not exist.")
        return
    
    target_dir = target_name
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    status_groups = {}

    with open(input_file, "r") as file:
        subdomains = [line.strip() for line in file if line.strip()]

    print("[*] Checking status codes for subdomains...")

    for subdomain in subdomains:
        for protocol in ("http", "https"):
            url = f"{protocol}://{subdomain}"
            status_code = check_status_code(url)
            if status_code:
                status_groups.setdefault(status_code, []).append(subdomain)

    print("[+] Status code checks completed.")

    for status_code, domains in status_groups.items():
        output_file = os.path.join(target_dir, f"{target_name}_{status_code}.txt")
        with open(output_file, "w") as file:
            file.write("\n".join(set(domains)))  # Remove duplicates
        print(f"[+] Saved {len(domains)} subdomains to {output_file}.")


if __name__ == "__main__":
    target_name = input("[*] Enter your target name: ")
    input_file = input("[*] The path of the subdomains file: ")

    group_subdomains_by_status(input_file, target_name)
