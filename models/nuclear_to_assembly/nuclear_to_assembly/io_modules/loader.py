import json
from jsonschema import validate
from importlib.resources import files

def _schema_text(name: str) -> str:
    return files("nuclear_to_assembly.data.schemas").joinpath(name).read_text()

def load_json(path: str):
    with open(path) as f:
        return json.load(f)

def validate_assembly(data: dict) -> dict:
    schema = json.loads(_schema_text("assembly.schema.json"))
    validate(instance=data, schema=schema)
    return data

