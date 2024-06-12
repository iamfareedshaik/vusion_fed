import time
import json
import requests
import uuid

# Function to read all logs from the file
def read_all_logs(file_path):
    with open(file_path, 'r') as f:
        logs = f.readlines()
    return logs

# Function to read new logs from the file
def read_new_logs(file_path, old_logs):
    with open(file_path, 'r') as f:
        new_logs = f.readlines()
        new_logs = new_logs[len(old_logs):]
    return new_logs

# Function to send log data to the endpoint
def send_log_to_endpoint(log_data, endpoint):
    print(log_data)
    try:
        response = requests.post(endpoint, json=log_data)
        if response.status_code == 200:
            print("Log sent successfully!")
        else:
            print(f"Failed to send log. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error occurred while sending log: {e}")

def transform_log_data(log_data):
    transformed_data = {
        "case_id": str(uuid.uuid4()), 
        "src_ip": log_data["src_ip"],
        "time_stamp": log_data["timestamp"],
        "input_cmd": log_data.get("input", ""),  
        "honeypot_name": "cowrie",
        "response_cmd": ""   
    }
    return transformed_data

# Set the path to the cowrie.json file
file_path = "./cowrie-logs/cowrie.json"
# Set the endpoint URL
endpoint = "http://16.171.142.151:3000/item"

# Read all existing logs
old_logs = read_all_logs(file_path)

while True:
    # Read new logs
    new_logs = read_new_logs(file_path, old_logs)
    
    # Update the old logs to include new logs
    old_logs.extend(new_logs)
    
    # Process new logs
    for log in new_logs:
        try:
            log_data = json.loads(log)
            # Transform log_data into the desired format
            transformed_data = transform_log_data(log_data)
            # Process transformed_data (send to endpoint, etc.)
            send_log_to_endpoint(transformed_data, endpoint)
        except json.JSONDecodeError:
            print("Invalid JSON log format")

    # Wait for some time before polling again (e.g., every 1 second)
    time.sleep(1)
