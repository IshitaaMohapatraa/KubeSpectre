# KubeSpectre
> **Automated Kubernetes Incident Response Engine for Real-Time Threat Mitigation**
KubeSpectre is a zero-trust Kubernetes security and incident response engine. It continuously ingests Kubernetes API audit streams, analyzes event patterns for malicious behaviors, and dynamically triggers automated pod-level isolation via granular NetworkPolicy enforcement.

## Features
* **Real-Time Audit Stream Ingestion:** High-throughput event processing using FastAPI webhooks and Redis event queues.
* **Rule-Based Threat Detection:** Identifies execution anomalies, secret access attempts, privilege escalation, and lateral movement signatures.
* **Autonomous Quarantine Engine:** Dynamically injects label-scoped NetworkPolicy objects (run=<pod-label>) to isolate compromised workloads without disrupting surrounding cluster services.
* **MITRE ATT&CK Mapping:** Designed around container threat tactics including T1611 (Escape to Host) and T1078 (Valid Accounts).
* **Multi-Engine Hybrid Injection:** Native prototype setter and DOM injection pipeline designed to support ChatGPT, Claude, Gemini, and DeepSeek.
* **Cross-Platform Host Support:** Fully compatible with local development environments running k3d / k3s across Linux and Windows.

## System Architecture
```text
KubeSpectre uses a webhook-driven ingestion pipeline combined with a Redis queue and an automated response engine to ensure rapid threat mitigation before an attacker can escalate privileges in the cluster.

+-----------------------------------------------------------------------+
|                        KUBERNETES CLUSTER                             |
|                                                                       |
|  +------------------+     Audit Logs      +-------------------+       |
|  | Target Pod       | ------------------> | K3s / K3d API     |       |
|  | (e.g., target-ng)|                     | Server Audit Log  |       |
|  +------------------+                     +-------------------+       |
|           |                                         |                 |
|           v                                         | Webhook         |
|  +------------------+                               v                 |
|  | Exec / Exploit   |                     +-------------------+       |
|  | (Secret Theft)   |                     | FastAPI Engine    |       |
|  +------------------+                     | (app/main.py)     |       |
|                                           +-------------------+       |
|                                                     |                 |
|                                                     v                 |
|                                           +-------------------+       |
|                                           | Redis Queue       |       |
|                                           | (app/queue.py)    |       |
|                                           +-------------------+       |
+-----------------------------------------------------|-----------------+
                                                      |
                                                      v
+-----------------------------------------------------------------------+
|                      SPECTRE-GUARD RESPONDER                          |
|                                                                       |
|  +-----------------------------------------------------------------+  |
|  | Rule Evaluation & Responder (app/rules/responder.py)            |  |
|  | |-- Detects Unauthorised Exec / Token Access                    |  |
|  | '-- Triggers quarantine_pod('namespace', 'pod_name')            |  |
|  +-----------------------------------------------------------------+  |
|                                     |                                 |
|                                     v                                 |
|  +-----------------------------------------------------------------+  |
|  | Dynamic NetworkPolicy Injection                                 |  |
|  | '-- Applies spectre-quarantine-<pod> (isolate run=pod-label)    |  |
|  +-----------------------------------------------------------------+  |
+-----------------------------------------------------------------------+
```

### Data Flow Lifecycle
1. **Ingestion:** Kubernetes audit event streams are intercepted via webhook handlers or processed via detection modules (`app/queue.py`).
2. **Analysis:** The `spectre-guard` rules engine evaluates security anomalies across multiple rule sets (`recon.py, privilege_escalation.py, secret_theft.py, responder.py`)..
3. **Trigger Evaluation:** When a malicious pattern (such as unauthorized token extraction or command execution) is verified, the core engine initiates the isolation workflow.
4. **Autonomous Remediation:** The `quarantine_pod` function dynamically crafts and applies a strict Kubernetes `NetworkPolicy` matching the target pod label, instantly cutting off inbound and outbound traffic.

## Getting Started

### 1. Installation
Clone the repository and install the required dependencies:
```bash
git clone https://github.com/IshitaaMohapatraa/KubeSpectre.git
cd KubeSpectre/spectre-guard
```
### 2. Set Up Python Environment
Create and activate your virtual environment, then install dependencies:
```bash
python -m venv venv
source venv/Scripts/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Start the Ingestion Service
Run the background queue listener/audit processor:
```bash
python -m app.queue
```

### 4. Verify Manual Quarantine Execution (Test Run)
To trigger the automated quarantine logic directly against a test workload:
```bash 
python -c "from app.rules.responder import quarantine_pod; quarantine_pod('default', 'target-nginx')"
  ```

### 5. Check Applied Network Policies in Cluster
Confirm that the isolation policy has been successfully injected into your local cluster (`k3d`/`k3s`):
```bash
kubectl get networkpolicies
```

## Local Verification & Testing:
To test the automated isolation mechanism against a target pod:
```bash
# 1. Deploy a test application
kubectl run target-nginx --image=nginx --labels="run=target-nginx"

# 2. Simulate an execution / credential access attempt
kubectl exec target-nginx -- sh -c "cat /var/run/secrets/kubernetes.io/serviceaccount/token"

# 3. Confirm target pod isolation policy is deployed
kubectl get networkpolicies
```

## Known Limitations:
* **Audit Log Subresources**: Direct `kubectl exec` events generate subresource requests on `/exec` which require specific webhook binding configurations depending on the local cluster provider (`k3d` vs standard bare-metal k8s).

## License:
Distributed under the MIT License. See LICENSE for details.