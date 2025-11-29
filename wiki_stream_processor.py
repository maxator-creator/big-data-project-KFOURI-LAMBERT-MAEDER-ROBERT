# wiki_stream_processor_v3_FIXED.py
import json
import time
import requests
from requests_sse import EventSource 

# --- 1. Configuration ---

TRACKED_ENTITIES = {
    "The_Shawshank_Redemption",
    "The_Dark_Knight_(film)",
    "Tom_Hanks",
    "Christopher_Nolan",
    "Science_fiction_film"
}
ALERT_USER = "ClueBot NG"
METRICS_FILE = "wiki_metrics.json"
ALERTS_FILE = "wiki_alerts.log"
STATE_FILE = "stream_state.json"
STREAM_URL = "https://stream.wikimedia.org/v2/stream/recentchange"

# --- 2. State Management (in-memory) ---
metrics = {
    "total_events_processed": 0,
    "tracked_edits": {entity: 0 for entity in TRACKED_ENTITIES}
}
last_save_time = time.time()

# --- 3. Helper Functions ---
# (save_metrics, log_alert, load_last_id, save_last_id functions are unchanged)

def save_metrics():
    """Saves the current metrics dictionary to a JSON file."""
    try:
        with open(METRICS_FILE, 'w', encoding='utf-8') as f:
            json.dump(metrics, f, indent=2)
        print(f"Metrics saved at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    except IOError as e:
        print(f"Error saving metrics: {e}")

def log_alert(event_data):
    """Appends a raw event JSON to the alert log file (JSON-Lines format)."""
    try:
        with open(ALERTS_FILE, 'a', encoding='utf-8') as f:
            json.dump(event_data, f)
            f.write('\n')
        
        title = event_data.get('title', 'N/A')
        print(f"*** ALERT! User '{ALERT_USER}' edited '{title}' ***")
    except IOError as e:
        print(f"Error writing alert: {e}")

def load_last_id():
    """Loads the last saved event ID from the state file."""
    try:
        with open(STATE_FILE, 'r') as f:
            state = json.load(f)
            return state.get('latest_event_id')
    except (IOError, json.JSONDecodeError):
        return None

def save_last_id(event_id):
    """Saves the last processed event ID to the state file."""
    try:
        with open(STATE_FILE, 'w') as f:
            json.dump({'latest_event_id': event_id}, f)
    except IOError as e:
        print(f"Error saving stream state: {e}")

# --- 4. Main Processing Loop ---

def start_stream():
    """Connects to the stream and processes events."""
    
    current_event_id = load_last_id()

    print(f"Connecting to Wikimedia EventStream: {STREAM_URL}")
    if current_event_id:
        print(f"Resuming from last event ID: {current_event_id}")
    else:
        print("Starting new stream.")
        
    print(f"Tracking {len(TRACKED_ENTITIES)} entities...")
    print(f"Alerting on edits by user: '{ALERT_USER}'")
    
    #
    # --- THIS IS THE NEW HEADER TO FIX THE 403 ERROR ---
    # (Change the email to your own)
    #
    http_headers = {
        'User-Agent': 'My-ECE-BigData-Project/1.0 (maximemaeder15@gmail.com)'
    }
    
    try:
        #
        # --- PASS THE NEW HEADERS TO THE EventSource ---
        #
        with EventSource(STREAM_URL, latest_event_id=current_event_id, headers=http_headers) as stream:
            for event in stream:
                
                if event.last_event_id:
                    current_event_id = event.last_event_id

                if event.type != 'message':
                    continue

                try:
                    data = json.loads(event.data)
                except json.JSONDecodeError:
                    print("Warning: Received a malformed JSON event, skipping.")
                    continue
                
                if data.get('meta', {}).get('domain') == 'canary':
                    continue

                metrics["total_events_processed"] += 1
                page_title = data.get('title')

                if page_title in TRACKED_ENTITIES:
                    metrics["tracked_edits"][page_title] += 1
                    user = data.get('user', 'N/A')
                    edit_type = data.get('type', 'N/A')
                    print(f"--- Tracked Edit on '{page_title}' by '{user}' (Type: {edit_type}) ---")

                    if user == ALERT_USER:
                        log_alert(data)

                global last_save_time
                if time.time() - last_save_time > 15:
                    save_metrics()
                    if current_event_id:
                        save_last_id(current_event_id)
                    last_save_time = time.time()

    except KeyboardInterrupt:
        print("\nStream stopped by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        print("Saving final metrics...")
        save_metrics()
        if current_event_id:
            print(f"Saving final stream position (ID: {current_event_id})...")
            save_last_id(current_event_id)
        print("Exiting.")

if __name__ == "__main__":
    start_stream()