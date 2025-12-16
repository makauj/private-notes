import requests
import json
import os
import re

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
        filtered_jobs = {}
        for job in data:
            job["position"] = job.get("position", "").lower()

            if any(term in job["position"] for term in search_term):
                filtered_jobs[job['id']] = job
        return list(filtered_jobs.values())


    except FileNotFoundError:
        print("No local data available.")
        return []
    except json.JSONDecodeError:
        print("Error decoding JSON from local file.")
        return []

def save_filtered_jobs():
    try:
        with open("data/raw_jobs.json", "r", encoding="utf-8") as file:
            data = json.load(file)


        search_list = {"backend", "api", "server", "data"}


        # Use word boundaries only for pure words (backend/server/data), but "api" works fine too.
        pattern = re.compile(r"\b(" + "|".join(search_list) + r")\b", re.IGNORECASE)


        results = []


        for job in data:
            # Ensure job is a dict and has expected fields
            if not isinstance(job, dict) or "position" not in job:
                continue


            # Extract matches from job title
            matches = pattern.findall(job["position"])


            # Build structured result
            results.append({
                "position": job.get("position"),
                "location": job.get("location"),
                "apply_url": job.get("url"),
                "tags": list({m.lower() for m in matches}),  # remove duplicates, normalize
            })


    except Exception as e:
        raise Exception(f"An error occurred: {e}")


if __name__ == "__main__":
    fetch_jobs(url)
    save_filtered_jobs()
