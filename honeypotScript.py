import time
import json

# Function to read all logs from the file
def read_all_logs(file_path):
    with open(file_path, 'r') as f:
        logs = f.readlines()
    return logs

# Function to read new logs from the file
def read_new_logs(file_path, old_logs):
    with open(file_path, 'r') as f:
        new_logs = f.readlines()
        new_logs = new_logs[len(old_logs):]  # Only consider newly appended logs
    return new_logs

# Set the path to the cowrie.json file
file_path = "./cowrie-logs/cowrie.json"

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
            # Process log_data (send to endpoint, etc.)
            print(log_data)  # For demonstration purposes, print the log data
        except json.JSONDecodeError:
            print("Invalid JSON log format")

    # Wait for some time before polling again (e.g., every 1 second)
    time.sleep(1)
