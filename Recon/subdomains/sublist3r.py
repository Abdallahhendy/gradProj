import os
import subprocess

sublister_full_path = r"C:\Users\Softlaptop\Sublist3r"

def run_sublist3r(domain):
    """
    Run Sublist3r to enumerate subdomains for a given domain and display the output on the screen.
    """
    try:
        sublist3r_script = os.path.join(sublister_full_path, 'sublist3r.py')

        if not os.path.exists(sublist3r_script):
            raise FileNotFoundError(f"Sublist3r script not found at {sublist3r_script}")

        print(f"[*] Enumerating subdomains for {domain} using Sublist3r...\n")

        result = subprocess.run(
            ['python', sublist3r_script, '-d', domain],
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE
        )

        if result.returncode != 0:
            print("[!] Sublist3r failed with error:")
            print(result.stderr.decode())
        else:
            print("[+] Subdomains Found:\n")
            print(result.stdout.decode())

    except FileNotFoundError as e:
        print("[!] Error:", e)
    except Exception as e:
        print("[!] Unexpected Error:", e)

def main():
    domain = input("Enter the domain to enumerate subdomains: ").strip()

    run_sublist3r(domain)

if __name__ == "__main__":
    main()