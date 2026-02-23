import json
import os

BASE_PATH = os.path.dirname(__file__)

TABLES = {
    "users": "users.json",
    "fornecedores": "fornecedores.json",
    "permissoes": "permissoes.json",
    "modulos": "modulos.json",
    "config": "config.json"
}

def _get_path(table):
    if table not in TABLES:
        raise Exception(f"Tabela '{table}' não registrada no manager")
    return os.path.join(BASE_PATH, TABLES[table])

def load(table):
    path = _get_path(table)
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save(table, data):
    path = _get_path(table)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def insert(table, key, value):
    data = load(table)
    if key in data:
        raise Exception(f"Registro '{key}' já existe em {table}")
    data[key] = value
    save(table, data)

def update(table, key, value):
    data = load(table)
    if key not in data:
        raise Exception(f"Registro '{key}' não existe em {table}")
    data[key] = value
    save(table, data)

def delete(table, key):
    data = load(table)
    if key in data:
        del data[key]
        save(table, data)
