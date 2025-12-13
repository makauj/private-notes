import requests
import json
import os
from re import search

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
    
    try:
        with open("data/raw_jobs.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        
        search_term = {"python", "developer", "engineer", "remote", "backend", "fullstack", "frontend", "api", "software"}
        for job in data:
            job["position"] = job.search("position", "").lower()

            filtered_jobs = {
                job['id']: job for job in data
                if any(term in job["position"] for term in search_term)
            }
        return list(filtered_jobs.values())


    except FileNotFoundError:
        print("No local data available.")
        return []
    except json.JSONDecodeError:
        print("Error decoding JSON from local file.")
        return []

def save_filtered_jobs(filtered_jobs):
    """Save filtered jobs to a JSON file."""
    try:
        with open("data/filtered_jobs.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(filtered_jobs, indent=4))
    except Exception as e:
        print(f"Error writing filtered jobs to file: {e}")

if __name__ == "__main__":
    filtered_jobs = fetch_jobs(url)
    save_filtered_jobs(filtered_jobs)
