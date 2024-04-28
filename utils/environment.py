import os


class EnvironmentUtils:
    @staticmethod
    def get_env_variable(key: str):
        optional_value = os.getenv(key)
        if not optional_value or optional_value is None:
            raise ValueError(f"Environment variable {key} must be set")

        return optional_value
