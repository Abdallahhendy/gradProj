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
