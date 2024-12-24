import sqlite3
from pathlib import Path


class DbConnectionFactory:
    _instances = {}

    @classmethod
    def connect(cls, path):
        if path not in cls._instances:
            if path != ':memory:':
                Path(path).parent.mkdir(parents=True, exist_ok=True)
            cls._instances[path] = sqlite3.connect(path)
        return cls._instances[path]
