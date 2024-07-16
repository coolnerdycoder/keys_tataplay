import requests
import json
import logging
import subprocess
import os
import filecmp

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
API_URL = "https://tplayapi.code-crafters.app/321codecrafters/fetcher.json"
RETRIES = 3

def fetch_api(url, retries):
    for attempt in range(retries):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise HTTPError for bad status codes
            return response.json()
        except requests.RequestException as e:
            logging.error(f"Error fetching API data (attempt {attempt + 1}/{retries}): {e}")
            if attempt < retries - 1:
                continue
            else:
                return None

def transform_data(api_data):
    transformed_data = []
    if api_data and 'data' in api_data and 'channels' in api_data['data']:
        for channel in api_data['data']['channels']:
            if 'clearkeys' in channel and channel['clearkeys']:
                for clearkey in channel['clearkeys']:
                    if 'base64' in clearkey:
                        transformed_channel = clearkey['base64']
                        transformed_channel["channel_id"] = channel['id']
                        transformed_data.append(transformed_channel)
    return transformed_data

def read_keys_json():
    try:
        with open('keys.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def write_keys_json(data):
    with open('keys.json', 'w') as f:
        json.dump(data, f, indent=2)

def has_content_changed(new_data):
    try:
        with open('keys.json.tmp', 'w') as f:
            json.dump(new_data, f, indent=2)
        return not filecmp.cmp('keys.json', 'keys.json.tmp')
    except FileNotFoundError:
        return True
    finally:
        if os.path.exists('keys.json.tmp'):
            os.remove('keys.json.tmp')

def main():
    api_data = fetch_api(API_URL, RETRIES)
    if api_data:
        transformed_data = transform_data(api_data)
        if transformed_data:
            current_data = read_keys_json()
            if current_data != transformed_data:
                write_keys_json(transformed_data)
                logging.info("Data saved to keys.json")
                
                if has_content_changed(transformed_data):
                    # Commit and push changes
                    commit_message = "Updated keys.json"
                    subprocess.run(['git', 'commit', '-am', commit_message])
                    subprocess.run(['git', 'push'])
                    logging.info("Changes committed and pushed successfully.")
                else:
                    logging.info("No changes detected in keys.json. Skipping commit and push.")
            else:
                logging.info("No changes detected in transformed data. Skipping writing to keys.json.")
        else:
            logging.warning("No clear keys found in API response")
    else:
        logging.error("Failed to fetch data from API")

if __name__ == "__main__":
    main()
