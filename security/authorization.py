import json
import os

BASE_PATH = os.path.dirname(__file__)
DB_PATH = os.path.join(os.path.dirname(BASE_PATH), "database")

PERMISSOES_FILE = os.path.join(DB_PATH, "permissoes.json")
MODULOS_FILE = os.path.join(DB_PATH, "modulos.json")

# ---------- LOADERS ----------

def load_permissoes():
    if not os.path.exists(PERMISSOES_FILE):
        return {}
    with open(PERMISSOES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def load_modulos():
    if not os.path.exists(MODULOS_FILE):
        return {}
    with open(MODULOS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# ---------- ACL CORE ----------

def modulos_permitidos(role: str):
    permissoes = load_permissoes()
    modulos = load_modulos()

    if role not in permissoes:
        return []

    return [m for m in permissoes[role].keys() if m in modulos]

def acoes_permitidas(role: str, modulo: str):
    permissoes = load_permissoes()

    if role not in permissoes:
        return []

    if modulo not in permissoes[role]:
        return []

    return permissoes[role][modulo]

def pode(role: str, modulo: str, acao: str) -> bool:
    permissoes = load_permissoes()

    if role not in permissoes:
        return False

    if modulo not in permissoes[role]:
        return False

    return acao in permissoes[role][modulo]
