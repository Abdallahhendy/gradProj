import requests
import os
def check_security_headers(url):
    headers_to_check = {
        "security_headers": [
            "Content-Security-Policy",
            "Strict-Transport-Security",
            "X-Content-Type-Options",
            "X-Frame-Options",
            "X-XSS-Protection",
            "Permissions-Policy",
            "Referrer-Policy",
            "Feature-Policy",
            "Cache-Control",
            "Set-Cookie"
        ],
        "info_headers": [
            "Server",
            "X-Powered-By",
            'X-AspNet-Version',
            'X-AspNetMvc-Version',

        ]
    }
    
    results = {}
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        response = requests.get(url, timeout=10)
        headers = response.headers

        results["security_headers"] = {header: headers.get(header, "Not present") for header in headers_to_check["security_headers"]}

        results["info_headers"] = {header: headers.get(header, "Not present") for header in headers_to_check["info_headers"]}

    except requests.exceptions.RequestException as e:
        results["security_headers"] = {header: "Error" for header in headers_to_check["security_headers"]}
        results["info_headers"] = {header: "Error" for header in headers_to_check["info_headers"]}

    return results

def read_urls_from_file(file_path):
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the script's directory
    file_path = os.path.join(script_dir, file_path)  # Build the full file path

    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

if __name__ == "__main__":
    urls = read_urls_from_file("urls.txt")
    description = {
        "Content-Security-Policy": "Helps prevent cross-site scripting (XSS) attacks and data injection.",
        "Strict-Transport-Security": "Forces secure (HTTPS) connections to the server, mitigating man-in-the-middle attacks.",
        "X-Content-Type-Options": "Prevents browsers from interpreting files as a different MIME type, reducing risks of XSS.",
        "X-Frame-Options": "Protects against clickjacking attacks by controlling if a page can be framed.",
        "X-XSS-Protection": "Activates browser XSS filtering, mitigating some reflected XSS attacks.",
        "Permissions-Policy": "Restricts browser features like camera, microphone, and geolocation.",
        "Referrer-Policy": "Controls how much referrer information is sent with requests, reducing data leakage.",
        "Feature-Policy": "Deprecated; use Permissions-Policy to limit browser features.",
        "Cache-Control": "Prevents sensitive data from being stored in cache, reducing risks of data theft.",
        "Set-Cookie": "Ensures secure and HttpOnly attributes on cookies, protecting against cookie theft and XSS."
    }
    for url in urls:
        print(f"\nChecking headers for: {url}")
        results = check_security_headers(url)

        print("\nSecurity Headers:")
        for header, value in results["security_headers"].items():
            if value == "Not present":
                print(f"  {header}: Missing")
                print(f"{description[f"{header}"]}")
            else:
                pass

        print("\nInfo Headers:")
        for header, value in results["info_headers"].items():
            if value == "Not present":
                pass
            else:
                print(f"  {header}: {value}")



# dictt = {"abdo":"111", "moha":"222", "ahmed":"333"}
# print(dictt["abdo"])