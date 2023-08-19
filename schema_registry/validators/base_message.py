import json
import os
from jsonschema import validate, ValidationError
from settings import settings


class BaseEventMessage:
    def __init__(self):
        self.schema = self.load_schema()

    def validate(self, message):
        try:
            validate(instance=message, schema=self.schema)
            return True
        except ValidationError as e:
            print(f"Validation error: {e}")
            return False

    def load_schema(self):
        schema_file = os.path.join(
            settings.schema_registry_path, self.get_schema_path()
        )
        with open(schema_file, "r") as f:
            return json.load(f)

    def get_schema_path(self):
        raise NotImplementedError("Subclasses must implement get_schema_path")
