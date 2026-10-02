import time
import json
import redis
from app.config import REDIS_HOST, REDIS_PORT, REDIS_QUEUE_NAME

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

def start_worker():
    print(f"[*] Spectre-Guard background worker started, listening to Redis queue: {REDIS_QUEUE_NAME}")
    while True:
        try:
            # Block and pop audit events from Redis list
            item = r.blpop(REDIS_QUEUE_NAME, timeout=1)
            if item:
                _, raw_data = item
                event = json.loads(raw_data.decode("utf-8"))
                
                # Extract core audit properties for detection
                verb = event.get("verb")
                uri = event.get("requestURI", "")
                user = event.get("user", {}).get("username", "unknown")
                resource = event.get("objectRef", {}).get("resource", "")
                namespace = event.get("objectRef", {}).get("namespace", "default")
                
                print(f"[AUDIT] User: {user} | Verb: {verb} | Resource: {resource} | NS: {namespace} | URI: {uri}")
                
                # TODO: Evaluate detection rules here in the next step
                
        except Exception as e:
            print(f"[-] Worker error: {e}")
            time.sleep(1)

if __name__ == "__main__":
    start_worker()