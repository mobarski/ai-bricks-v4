import sqlite3
from pathlib import Path


class DatabaseFactory:
    _instances = {}

    @classmethod
    def get_connection(cls, path):
        if path not in cls._instances:
            if path != ':memory:':
                Path(path).parent.mkdir(parents=True, exist_ok=True)
            cls._instances[path] = sqlite3.connect(path)
        return cls._instances[path]
