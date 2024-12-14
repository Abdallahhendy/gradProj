import os
import subprocess

def run_script(script_name, args):
    """تشغيل السكربت مع المعاملات المحددة"""
    command = ['python3', script_name] + args
    print(f"[*] Running {script_name} with arguments: {args}")
    result = subprocess.run(command, capture_output=True, text=True)

    # طباعة المخرجات من السكربت
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)

def load_subdomains_from_file(file_path):
    """تحميل النطاقات من ملف CSV"""
    subdomains = []
    try:
        with open(file_path, 'r') as f:
            subdomains = [line.strip() for line in f if line.strip()]
        if not subdomains:
            raise ValueError("No subdomains found in the file.")
    except Exception as e:
        print(f"[ERROR] Failed to load subdomains: {e}")
    return subdomains

def find_200_ok_file(directory):
    """البحث عن أول ملف 200.csv في المسار المحدد"""
    for filename in os.listdir(directory):
        if filename.endswith("200.csv"):
            return os.path.join(directory, filename)
    return None

def main():
    # تحديد المسارات
    results_by_status_dir = "/home/kali/Desktop/connect/results_by_status"
    
    # البحث عن أول ملف يحتوي على 200.csv
    input_file = find_200_ok_file(results_by_status_dir)
    
    if not input_file:
        print(f"[ERROR] No 200.csv file found in {results_by_status_dir}. Exiting.")
        return
    
    print(f"[*] Found file: {input_file}")
    
    # 1. تحميل النطاقات من ملف CSV
    print(f"[*] Loading subdomains from {input_file}...")
    subdomains = load_subdomains_from_file(input_file)

    if not subdomains:
        print("[ERROR] No subdomains found. Exiting.")
        return

    # 2. تشغيل extract_js_files.py مع تمرير النطاقات
    print(f"[*] Running extract_js_files.py for {len(subdomains)} subdomains...")
    output_file_js = "/home/kali/Desktop/connect/crawling1/all_js_files.txt"  # تحديد الملف لحفظ نتائج JS
    for subdomain in subdomains:
        run_script('extract_js_files.py', [subdomain, output_file_js])

    # 3. تشغيل extract_endpoints.py مع تمرير النطاقات
    print(f"[*] Running extract_endpoints.py for {len(subdomains)} subdomains...")
    output_file_endpoints = "/home/kali/Desktop/connect/crawling1/all_endpoints.txt"  # تحديد الملف لحفظ النتائج
    for subdomain in subdomains:
        run_script('extract_endpoints.py', [subdomain, output_file_endpoints])

    print("[+] Extraction completed successfully!")

if __name__ == "__main__":
    main()
