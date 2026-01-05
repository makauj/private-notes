import json
import requests
import os


url = "https://remoteok.com/api"
def jobImport(url):
    try:
        response = requests.get(
            url,
            timeout=10
            )
        response.raise_for_status()
        data = response.json()
        os.makedirs("data", exist_ok=True)
        json_str = json.dumps(data, indent=4)
        with open("data/raw_jobs2.json", "w", encoding="utf-8") as f:
            f.write(json_str)
        return data

    except requests.exceptions.Timeout as e:
        print(f"Error: Timeout: {e}")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"Error: HTTP error: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Other errors caught: {e}")
        return None

def filter_jobs_by_keyword(jobs, keyword):
    try:
        with open("data/raw_jobs2.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        search_term = {"python", "developer", "engineer", "remote", "backend", "fullstack", "frontend", "api", "software"}
        filtered_jobs = {}
        for job in data:
            if any(term in job.get("position", "").lower() for term in search_term):
                filtered_jobs[job['id']] = job
        os.makedirs("data", exist_ok=True)
        json_dumps = json.dumps(list(filtered_jobs.values()), indent=4)
        with open("data/filtered_jobs.json", "w", encoding="utf-8") as f:
            f.write(json_dumps)
        return list(filtered_jobs.values())

    except FileNotFoundError:
        print("No local data available.")
        return None
    except json.JSONDecodeError:
        print("Error decoding JSON from local file.")
        return None


if __name__ == "__main__":
    jobs = jobImport(url)
    jobImport(url)
    if jobs:
        filter_jobs_by_keyword(jobs, "remote")
