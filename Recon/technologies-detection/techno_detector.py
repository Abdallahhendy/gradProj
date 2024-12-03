from webappalyzer.Wappalyzer import Wappalyzer
from webappalyzer.webpage._bs4 import WebPage
import requests
import os, sys, warnings

warnings.filterwarnings("ignore", message=".*bad character range.*")
warnings.filterwarnings("ignore", message=".*unbalanced parenthesis.*")

def suppress_output(func, *args, **kwargs):
    """Suppress stdout and stderr temporarily."""
    with open(os.devnull, 'w') as fnull:
        original_stdout = sys.stdout
        original_stderr = sys.stderr
        try:
            sys.stdout = fnull
            sys.stderr = fnull
            return func(*args, **kwargs)
        finally:
            sys.stdout = original_stdout
            sys.stderr = original_stderr

def get_website_technologies(url):
    try:
        wappalyzer = Wappalyzer.latest()

        response = requests.get(url)
        response.raise_for_status()
        webpage = WebPage(url, response.text, response.headers)

        technologies = wappalyzer.analyze_with_versions_and_categories(webpage)

        print(f"Technologies used by {url}:")
        for tech, details in technologies.items():  # Correct iteration over dictionary
            version = details.get('version', 'Unknown')  # Fetch version if available
            categories = ", ".join(details.get('categories', []))  # Fetch categories
            print(f"  - {tech}: Version {version} | Categories: {categories}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    target_url = input("Enter the website URL (e.g., https://example.com): ")
    if not target_url.startswith('http'):
        target_url = 'http://' + target_url
    get_website_technologies(target_url)