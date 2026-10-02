#!/usr/bin/env bash
set -e

CLUSTER_NAME="kubespectre-dev"

echo "[+] Cleaning up previous cluster if present..."
k3d cluster delete $CLUSTER_NAME 2>/dev/null || true

echo "[+] Creating k3d cluster '$CLUSTER_NAME' with API Audit Webhook..."

# Convert Git Bash path to Windows format for Docker volume mounts
WIN_PWD=$(cygpath -w "$(pwd)")

k3d cluster create $CLUSTER_NAME \
  --agents 1 \
  --volume "${WIN_PWD}\\.k3d\\audit-policy.yaml:/etc/kubernetes/audit/policy.yaml@server:0" \
  --volume "${WIN_PWD}\\.k3d\\webhook-config.yaml:/etc/kubernetes/audit/webhook-config.yaml@server:0" \
  --k3s-arg "--kube-apiserver-arg=audit-policy-file=/etc/kubernetes/audit/policy.yaml@server:0" \
  --k3s-arg "--kube-apiserver-arg=audit-webhook-config-file=/etc/kubernetes/audit/webhook-config.yaml@server:0" \
  --k3s-arg "--kube-apiserver-arg=audit-webhook-batch-max-wait=1s@server:0"

echo "[+] Cluster '$CLUSTER_NAME' created successfully!"
echo "[+] Current context:"
kubectl cluster-info