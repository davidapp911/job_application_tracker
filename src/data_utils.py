from typing import Dict


def filter_empty_fields(data: dict) -> Dict:
    return {k: v for k, v in data.items() if v is not None and v.strip() != ""}
