"""Business ID generation helpers."""

import time


class GenerateID:
    @staticmethod
    def create_custom_id(prefix="ID"):
        return f"{prefix}{int(time.time() * 1000)}"
