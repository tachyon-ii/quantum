import json

def dump_json(data: dict, path_or_none: str | None = None):
    s = json.dumps(data, indent=2)
    if path_or_none:
        with open(path_or_none, "w") as f:
            f.write(s)
    else:
        print(s)

