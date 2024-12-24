from yamja import lookup


class DictNamespace:
    def __init__(self, data):
        # Convert the input data, handling nested dicts and lists
        if isinstance(data, dict):
            self._data = {k: DictNamespace(v) if isinstance(v, (dict, list)) else v 
                          for k, v in data.items()}
        elif isinstance(data, list):
            self._data = [DictNamespace(item) if isinstance(item, (dict, list)) else item 
                          for item in data]
        else:
            self._data = data

    def __getitem__(self, key):
        value = self._data[key]
        return value if not isinstance(value, dict) else DictNamespace(value)

    def __getattr__(self, attr):
        try:
            value = self._data[attr]
            return value if not isinstance(value, dict) else DictNamespace(value)
        except KeyError:
            raise AttributeError(f"'DictNamespace' object has no attribute '{attr}'")

    def lookup(self, path, default=...):
        return lookup(self._data, path, default)

    def get(self, key, default=None):
        return self._data.get(key, default)

    def to_dict(self):
        """Convert the namespace back to a regular dictionary."""
        return self.convert_to_raw(self._data)

    @staticmethod
    def convert_to_raw(data):
        """Convert nested DictNamespace objects back to raw dictionaries."""
        if isinstance(data, dict):
            return {k: DictNamespace.convert_to_raw(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [DictNamespace.convert_to_raw(item) for item in data]
        elif isinstance(data, DictNamespace):
            return DictNamespace.convert_to_raw(data._data)
        return data

    def __repr__(self):
        return f'DictNamespace({repr(self.convert_to_raw(self._data))})'


if __name__ == "__main__":
    # Simple nested dictionary with a list
    test_data = {
        'user': {
            'name': 'John',
            'contacts': [
                {'email': 'john@example.com'},
                {'phone': '555-0123'}
            ]
        }
    }

    ns = DictNamespace(test_data)
    print(ns)
    print(ns.to_dict())

    print(f"Dot notation: {ns.user.name}")
    print(f"Lookup notation: {ns.lookup('user.name')}")
    print(f"List access: {ns.user.contacts[0].email}")
    print(f"List lookup: {ns.lookup('user.contacts.0.email')}")
    print(f"Missing key with default: {ns.lookup('user.missing', 'not found')}")
