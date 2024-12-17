import socket
import os

def resolve_subdomain(word, domain):
    """
    Try resolving a subdomain by appending it to the domain name.
    """
    if not word or word.startswith('.'):
        return None

    full_domain = f"{word}.{domain}"
    
    try:
        socket.gethostbyname(full_domain)
        return full_domain
    except socket.gaierror:
        return None

def brute_force_subdomains(domain, wordlist_path):
    """
    Brute-force subdomain enumeration using a wordlist.
    """
    subdomains = []
    with open(wordlist_path, 'r') as wordlist:
        for word in wordlist:
            word = word.strip()  # Remove leading/trailing spaces or newlines
            subdomain = resolve_subdomain(word, domain)
            if subdomain:
                subdomains.append(subdomain)
    return subdomains

def main():
    domain = input("[*] Enter the target domain (e.g., example.com): ").strip()
    wordlist_path = os.path.join(os.path.dirname(__file__), "wordlist.txt")

    subdomains = brute_force_subdomains(domain, wordlist_path)
    print("[+] Found subdomains:")
    for subdomain in subdomains:
        print(subdomain)

if __name__ == "__main__":
    main()