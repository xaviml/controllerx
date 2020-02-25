from core.integration import Integration
from core.integration.state import StateIntegration


class Z2MIntegration(StateIntegration):
    def get_name(self):
        return "z2m"
