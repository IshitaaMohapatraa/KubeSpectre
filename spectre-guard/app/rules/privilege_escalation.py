from app.rules.base import BaseRule

class PrivilegeEscalationRule(BaseRule):
    rule_id = "SPEC-101"
    name = "Privileged Pod / Container Exec Detected"
    mitre_tactics = "T1611"
    description = "Detected execution command inside pod or privileged creation."

    def evaluate(self, event: dict) -> bool:
        verb = event.get("verb")
        uri = event.get("requestURI", "")
        
        # Trigger on high-risk subresource verbs like 'exec' or 'attach'
        if verb in ["create"] and ("pods/exec" in uri or "pods/attach" in uri):
            return True
        return False