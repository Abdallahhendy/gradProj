import requests
import json

def get_technologies_builtwith(url, api_key):
    endpoint = f"https://api.builtwith.com/free1/api.json?KEY={api_key}&LOOKUP={url}"

    try:
        response = requests.get(endpoint)
        
        if response.status_code == 200:
            data = response.json()
            
            if 'Results' in data and data['Results']:
                print(f"Technologies used by {url}:")
                
                for result in data['Results']:
                    for tech, details in result.items():
                        print(f"  - {tech}: {details}")
            else:
                print(f"No technologies found for {url}.")
        else:
            print(f"Failed to retrieve data for {url}. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    api_key = "4d2b2c40-6921-4eb4-a03b-3ca8bdb57d3a"
    
    # Input URL to check
    target_url = input("Enter the website URL (e.g., https://example.com): ")
    
    get_technologies_builtwith(target_url, api_key)
