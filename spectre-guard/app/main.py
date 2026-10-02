from fastapi import FastAPI, Request, BackgroundTasks
import json
import redis
from app.config import REDIS_HOST, REDIS_PORT, REDIS_QUEUE_NAME

app = FastAPI(title="KubeSpectre - Guard Engine")
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

@app.get("/healthz")
def health_check():
    return {"status": "ok", "service": "spectre-guard"}

@app.post("/api/v1/audit-webhook")
async def receive_audit_events(request: Request, background_tasks: BackgroundTasks):
    """
    Ingests raw EventList JSON payload directly streamed from Kubernetes API server.
    """
    try:
        data = await request.json()
        if data.get("kind") == "EventList":
            events = data.get("items", [])
            for event in events:
                # Push event payload to Redis queue for async evaluation
                background_tasks.add_task(r.rpush, REDIS_QUEUE_NAME, json.dumps(event))
        return {"status": "accepted", "ingested": len(data.get("items", []))}
    except Exception as e:
        return {"status": "error", "message": str(e)}