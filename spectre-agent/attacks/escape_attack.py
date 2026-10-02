from kubernetes import client, config
from kubernetes.stream import stream

def run_escape_simulation():
    config.load_incluster_config()
    v1 = client.CoreV1Api()

    try:
        # Proper WebSocket pod exec simulation (T1611)
        resp = stream(
            v1.connect_get_namespaced_pod_exec,
            name="target-nginx",
            namespace="default",
            command=["sh", "-c", "whoami"],
            stderr=True,
            stdin=False,
            stdout=True,
            tty=False
        )
        print(f"[+] Exec successful: {resp}")
    except Exception as e:
        print(f"[-] Exec simulation failed: {e}")