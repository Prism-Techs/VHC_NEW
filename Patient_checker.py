import os
import json
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import threading

class PatientDataSyncer:
    def __init__(self, folder_path, api_endpoint, wifi_status_file):
        """
        Initialize the PatientDataSyncer class.
        :param folder_path: Path to the folder containing JSON files.
        :param api_endpoint: API endpoint to sync patient data.
        :param wifi_status_file: Path to the WiFi status JSON file.
        """
        self.folder_path = folder_path
        self.api_endpoint = api_endpoint
        self.wifi_status_file = wifi_status_file

    def sync_file(self, file_path):
        """
        Check and sync a single JSON file.
        :param file_path: Path to the JSON file.
        """
        if not self._check_wifi_status():
            print("WiFi is not connected. Skipping sync.")
            return

        with open(file_path, "r") as file:
            try:
                data = json.load(file)
                if not data.get("is_sync", True):
                    print(f"Syncing file: {file_path}")
                    if self._sync_to_api(data):
                        data["is_sync"] = True
                        self._update_file(file_path, data)
                        print(f"File synced: {file_path}")
                    else:
                        print(f"Failed to sync file: {file_path}")
            except json.JSONDecodeError:
                print(f"Invalid JSON format in file: {file_path}")

    def _sync_to_api(self, data):
        """
        Sync patient data to the API.
        :param data: Patient data dictionary.
        :return: True if the API call was successful, False otherwise.
        """
        try:
            response = requests.post(self.api_endpoint, json=data)
            if response.status_code == 201:
                return True
            else:
                print(f"API Error: {response.status_code} - {response.text}")
                return False
        except requests.RequestException as e:
            print(f"API Request Failed: {e}")
            return False

    def _update_file(self, file_path, data):
        """
        Update the JSON file with the modified data.
        :param file_path: Path to the JSON file.
        :param data: Updated patient data dictionary.
        """
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

    def _check_wifi_status(self):
        """
        Check if WiFi is connected using the WiFi status JSON file.
        :return: True if WiFi is connected, False otherwise.
        """
        return True  # Placeholder for actual WiFi check logic

class FolderMonitor(FileSystemEventHandler):
    def __init__(self, syncer):
        """
        Initialize the FolderMonitor class.
        :param syncer: Instance of the PatientDataSyncer class.
        """
        self.syncer = syncer

    def on_created(self, event):
        """
        Handle the event when a new file is created in the folder.
        :param event: File system event.
        """
        if not event.is_directory and event.src_path.endswith(".json"):
            print(f"New file detected: {event.src_path}")
            self.syncer.sync_file(event.src_path)

def start_monitoring(folder_path, api_endpoint, wifi_status_file):
    """
    Start monitoring the folder for new JSON files, and sync all unsynced files initially.
    :param folder_path: Path to the folder containing JSON files.
    :param api_endpoint: API endpoint to sync patient data.
    :param wifi_status_file: Path to the WiFi status JSON file.
    """
    syncer = PatientDataSyncer(folder_path, api_endpoint, wifi_status_file)

    # Step 1: Sync all existing unsynced JSON files
    print(f"Checking for unsynced files in: {folder_path}")
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            syncer.sync_file(file_path)

    # Step 2: Start real-time monitoring
    event_handler = FolderMonitor(syncer)
    observer = Observer()
    observer.schedule(event_handler, folder_path, recursive=False)

    print(f"Monitoring folder: {folder_path}")
    observer.start()

    try:
        while True:
            time.sleep(1)  # Keep the script running
    except KeyboardInterrupt:
        print("Stopping folder monitoring.")
        observer.stop()

    observer.join()

def run_in_thread(folder_path, api_endpoint, wifi_status_file):
    """
    Run the folder monitoring in a separate thread to avoid blocking the main thread.
    :param folder_path: Path to the folder containing JSON files.
    :param api_endpoint: API endpoint to sync patient data.
    :param wifi_status_file: Path to the WiFi status JSON file.
    """
    monitoring_thread = threading.Thread(target=start_monitoring, args=(folder_path, api_endpoint, wifi_status_file))
    monitoring_thread.daemon = True
    monitoring_thread.start()

# Example usage
if __name__ == "__main__":
    folder_path = "./patient_data"
    api_endpoint = "https://example.com/api/patient"
    wifi_status_file = "./wifi_status.json"
    run_in_thread(folder_path, api_endpoint, wifi_status_file)
    print("Monitoring started in a separate thread.")
    time.sleep(10)  # Simulate main thread doing other work