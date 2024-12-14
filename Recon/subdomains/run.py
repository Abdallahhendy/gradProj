import subprocess
import os

def run_script(script_name, args):
    # Construct the command to run the script with the provided arguments
    command = ['python', script_name] + args
    print(f"[*] Running {script_name} with arguments: {args}")
    result = subprocess.run(command, capture_output=True, text=True)
    
    # Print the output from the script
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)

def main():
    # Ask user for input interactively
    domain = input("Enter the target domain (e.g., example.com): ")
    api_key = input("Enter your SecurityTrails API key: ")
    threads = input("Enter the number of threads to use (default 50): ")
    
    if not threads:
        threads = 50  # Set default value if no input is given
    else:
        threads = int(threads)  # Convert input to integer
    
    # Ask for the wordlist path
    wordlist_path = input("Enter the path to your wordlist (e.g., /path/to/wordlist.txt): ")
    
    # Run wordlist.py
    print("[*] Running wordlist.py...")
    run_script("wordlist.py", [domain, "--wordlist", wordlist_path, "--threads", str(threads)])

    # Run crtsh.py
    print("[*] Running crtsh.py...")
    run_script("crtsh.py", [domain, "--threads", str(threads)])

    # Run api.py
    print("[*] Running api.py...")
    run_script("api.py", [domain, "--api-key", api_key, "--threads", str(threads)])

    print("[*] All scripts completed.")

if __name__ == "__main__":
    main()
