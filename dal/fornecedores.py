import json
from pathlib import Path

BASE = Path("data/fornecedores.json")

def get_fornecedor_por_id(fornecedor_id: str):
    if not BASE.exists():
        return None

    with open(BASE, "r", encoding="utf-8") as f:
        dados = json.load(f)

    for f in dados:
        if f["id"] == fornecedor_id:
            return f

    return None
