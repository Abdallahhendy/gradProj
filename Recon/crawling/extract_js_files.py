import os
import requests
from bs4 import BeautifulSoup

def add_protocol(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        return "https://" + url
    return url

def extract_js_files(subdomains_file, output_file):
    subdomains = []
    
    try:
        # فتح الملف وقراءة النطاقات
        with open(subdomains_file, 'r') as csvfile:
            for line in csvfile:
                if line.strip():  # تأكد من أن السطر ليس فارغًا
                    subdomains.append(line.strip())
    except Exception as e:
        print(f"[ERROR] Failed to read subdomains file: {e}")
        return

    js_files = []

    for subdomain in subdomains:
        subdomain = add_protocol(subdomain)
        try:
            print(f"[*] Running extract_js_files for {subdomain}...")
            response = requests.get(subdomain, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                scripts = soup.find_all('script', src=True)

                for script in scripts:
                    js_file = script['src']
                    js_file = add_protocol(js_file)  # التأكد من إضافة البروتوكول
                    js_files.append(js_file)

        except Exception as e:
            print(f"Error processing {subdomain}: {e}")

    # حفظ ملفات الجافا سكربت
    if js_files:
        with open(output_file, 'w') as output:
            output.write('\n'.join(js_files))

        print(f"[*] JS files saved to {output_file}")
    else:
        print("[*] No JS files found.")

if __name__ == "__main__":
    subdomains_file = '/home/kali/Desktop/connect/results_by_status/udemy_200.csv'  # تعديل المسار هنا
    output_file = '/home/kali/Desktop/connect/crawling1/all_js_files.txt'  # تعديل المسار هنا
    extract_js_files(subdomains_file, output_file)
