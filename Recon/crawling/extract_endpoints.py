import os
import requests
import re
import csv

def add_protocol(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        return "https://" + url
    return url

def extract_endpoints_and_queries(subdomains_file):
    endpoint_regex = r"(https?://[^\s\"'<>]+)"
    query_endpoints = []
    normal_endpoints = []

    subdomains = []
    try:
        # فتح الملف وقراءة النطاقات
        with open(subdomains_file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row:  # تأكد من أن الصف غير فارغ
                    subdomains.append(row[0].strip())  # افتراض أن النطاقات في العمود الأول

    except Exception as e:
        print(f"[ERROR] Failed to read subdomains file: {e}")
        return

    for subdomain in subdomains:
        subdomain = add_protocol(subdomain)
        try:
            response = requests.get(subdomain, timeout=10)
            if response.status_code == 200:
                print(f"Processing {subdomain}...")

                links = re.findall(endpoint_regex, response.text)

                for link in links:
                    if "?" in link:
                        query_endpoints.append(link)
                    else:
                        normal_endpoints.append(link)

        except Exception as e:
            print(f"Error processing {subdomain}: {e}")

    query_endpoints = list(set(query_endpoints))
    normal_endpoints = list(set(normal_endpoints))

    project_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(project_dir, "query_endpoints.txt"), 'w') as output:
        output.write('\n'.join(query_endpoints))

    with open(os.path.join(project_dir, "normal_endpoints.txt"), 'w') as output:
        output.write('\n'.join(normal_endpoints))

    print("Saved all query and normal endpoints.")

if __name__ == "__main__":
    project_dir = os.path.dirname(os.path.abspath(__file__))
    subdomains_file = '/home/kali/Desktop/connect/results_by_status/udemy_200.csv'  # تعديل المسار
    extract_endpoints_and_queries(subdomains_file)
