Markdown
# KubeSpectre 🛡️⚡

> **Automated Kubernetes Incident Response Engine for Real-Time Threat Mitigation**

KubeSpectre is a zero-trust Kubernetes security and incident response engine. It continuously ingests Kubernetes API audit streams, analyzes event patterns for malicious behaviors, and dynamically triggers automated pod-level isolation via granular `NetworkPolicy` enforcement.

---

## Key Features

* 📡 **Real-Time Audit Stream Ingestion:** High-throughput event processing using FastAPI webhooks and Redis event queues.
* 🧠 **Rule-Based Threat Detection:** Identifies execution anomalies, secret access attempts, privilege escalation, and lateral movement signatures.
* 🛡️️ **Autonomous Quarantine Engine:** Dynamically injects label-scoped `NetworkPolicy` objects (`run=<pod-label>`) to isolate compromised workloads without disrupting surrounding cluster services.
* 🎯 **MITRE ATT&CK Mapping:** Designed around container threat tactics including **T1611 (Escape to Host)** and **T1078 (Valid Accounts)**.
* 🪟 **Cross-Platform Host Support:** Fully compatible with local development environments running `k3d` / `k3s` across Linux and Windows.

---

## Architecture Overview

  [ Kubernetes API / Audit Logs ]
                │
                ▼
[ FastAPI Engine ] ──► [ Redis Event Queue ]
                │
                ▼
          [ Spectre-Guard ]
      (Rule Evaluation Engine)
                │
                ▼
      [ Dynamic NetworkPolicy ]
      (Targeted Pod Quarantine)


---

## Core Detection Rules

| Threat Vector | Rule Logic | Mitigation Action |
| :--- | :--- | :--- |
| **ServiceAccount Token Access** | Unexpected access/read on SA token secrets | Automated Pod Quarantine |
| **Privilege Escalation / Exec** | Unauthorized `exec` calls into running target pods | Real-time Isolation Policy Injection |
| **Reconnaissance & Secret Theft** | Bulk secret enumeration across namespaces | Alerting & Workload Quarantine |

---

## Getting Started

### Prerequisites

* **Docker Desktop** / **k3d**
* **Python 3.10+**
* **kubectl CLI**
* **Redis Server**

### Installation & Setup

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/IshitaaMohapatraa/KubeSpectre.git](https://github.com/IshitaaMohapatraa/KubeSpectre.git)
   cd KubeSpectre/spectre-guard
Set Up Python Environment:

Bash
python -m venv venv
source venv/Scripts/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
Start the Audit Ingestion Queue:

Bash
python -m app.queue
Verify Manual Quarantine Execution (Optional Test):

Bash
python -c "from app.rules.responder import quarantine_pod; quarantine_pod('default', 'target-nginx')"
Verify Applied Network Policies:

Bash
kubectl get networkpolicies
Local Verification & Testing
To test the automated isolation mechanism against a target pod:

Bash
# 1. Deploy target application
kubectl run target-nginx --image=nginx --labels="run=target-nginx"

# 2. Simulate unauthorized exec / credential theft attempt
kubectl exec target-nginx -- sh -c "cat /var/run/secrets/kubernetes.io/serviceaccount/token"

# 3. Confirm target pod isolation policy is deployed
kubectl get networkpolicies
Tech Stack
Language: Python 3.10

API Framework: FastAPI, Uvicorn

Message Broker: Redis

Orchestration / SDK: Kubernetes Python Client, kubectl

Local Cluster Environment: k3d / Docker

License
Distributed under the MIT License. See LICENSE for details.


---
