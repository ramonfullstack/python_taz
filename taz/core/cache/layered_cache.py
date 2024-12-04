import json


class LayeredCache:
    def __init__(self):
        self._layers = []

    def set_layers(self, layers: list):
        self._layers = layers

    def set(self, key, value):
        decoded_value = json.dumps(value)
        for layer in self._layers:
            cached_data = layer.get(key)
            if cached_data is not None or value == cached_data:
                continue

            layer.set(key, decoded_value)

    def get(self, key):
        for layer in self._layers:
            cached_data = layer.get(key)
            if cached_data:
                try:
                    return json.loads(cached_data)
                except Exception:
                    return None

        return None
