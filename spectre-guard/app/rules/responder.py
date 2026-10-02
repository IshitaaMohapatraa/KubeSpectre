from kubernetes import client, config

try:
    # Try in-cluster config first (if running inside Kubernetes pod)
    config.load_incluster_config()
except Exception:
    # Fallback to local kubeconfig (if running directly on Windows host)
    config.load_kube_config()
    
    # --- WINDOWS FIX FOR WINERROR 10049 ---
    # Overrides 0.0.0.0 binding to 127.0.0.1 for local host outbound requests
    c = client.Configuration.get_default_copy()
    if "0.0.0.0" in c.host:
        c.host = c.host.replace("0.0.0.0", "127.0.0.1")
    client.Configuration.set_default(c)
    # --------------------------------------

v1_core = client.CoreV1Api()
v1_networking = client.NetworkingV1Api()

def quarantine_pod(namespace: str, pod_name: str):
    """
    Isolates a targeted pod by applying a default-deny NetworkPolicy.
    """
    policy_name = f"spectre-quarantine-{pod_name}"

    # Fetch pod labels dynamically to isolate ONLY the compromised pod
    try:
        target_pod = v1_core.read_namespaced_pod(name=pod_name, namespace=namespace)
        pod_labels = target_pod.metadata.labels or {"app": pod_name}
    except Exception:
        # Fallback to app label if reading pod fails
        pod_labels = {"app": pod_name}
    
    # Define absolute isolation NetworkPolicy for the targeted pod
    network_policy = {
        "apiVersion": "networking.k8s.io/v1",
        "kind": "NetworkPolicy",
        "metadata": {
            "name": policy_name,
            "namespace": namespace
        },
        "spec": {
            "podSelector": {
                "matchLabels": pod_labels
            },
            "policyTypes": ["Ingress", "Egress"],
            "ingress": [],
            "egress": []
        }
    }

    try:
        v1_networking.create_namespaced_network_policy(
            namespace=namespace,
            body=network_policy
        )
        print(f"[ALERT][QUARANTINE] Successfully isolated pod '{pod_name}' in namespace '{namespace}' via NetworkPolicy!")
    except Exception as e:
        if "AlreadyExists" in str(e):
            print(f"[*] Pod '{pod_name}' is already quarantined.")
        else:
            print(f"[-] Failed to isolate pod: {e}")