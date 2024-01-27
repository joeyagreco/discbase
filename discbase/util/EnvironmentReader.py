import os


class EnvironmentReader:
    @classmethod
    def get(cls, name: str, *, as_type: type = str) -> any:
        value = os.getenv(name)
        if value == None:
            return None
        return as_type(os.getenv(name))
