import json
import requests

url = "https://remoteok.com/api"

def call_api(url):
    """
    simple api to call remoteok api and return json data
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list):
            return data
        else:
            print("Unexpected data format received from API.")
            return None
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None

    
if __name__ == "__main__":
    data = call_api(url)
    if data:
        for job in data[1:]:  # Skip the first element which is metadata
            print(f"Company: {job.get('company')}")
            print(f"Position: {job.get('position')}")
            print(f"Location: {job.get('location')}")
            print(f"URL: {job.get('url')}")
            print("-" * 40)
    else:
        print("No data retrieved from the API.")