import requests
import json
import os

url = "https://remoteok.com/api"
def fetch_jobs(url):
    try:
        response = requests.get(
            url,
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        # create file and directory if not exists and write data to it
        
        os.makedirs("data", exist_ok=True)
        json_str = json.dumps(data, indent=4)
        # Make sure the folder exists or you’ll get an error
        with open("data/raw_jobs.json", "w", encoding="utf-8") as f:
            f.write(json_str)
        return data
    except requests.exceptions.Timeout:
        print("Error: Timeout...")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Other errors caught: {e}")

if __name__ == "__main__":
    fetch_jobs(url)
