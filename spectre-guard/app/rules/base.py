class BaseRule:
    rule_id: str = "SPEC-000"
    name: str = "Base Detection Rule"
    mitre_tactics: str = "TA0000"
    description: str = ""

    def evaluate(self, event: dict) -> bool:
        """
        Returns True if the audit event triggers this rule's threat criteria.
        """
        raise NotImplementedError