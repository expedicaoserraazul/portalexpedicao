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

# ---------- RBAC CORE ----------

def modulos_permitidos(role: str):
    """
    Retorna lista de módulos permitidos para o role
    """
    permissoes = load_permissoes()
    modulos = load_modulos()

    if role not in permissoes:
        return []

    permitidos = permissoes[role]

    # garante que só retorna módulos existentes
    return [m for m in permitidos if m in modulos]

def tem_permissao(role: str, modulo: str) -> bool:
    permissoes = load_permissoes()

    if role not in permissoes:
        return False

    return modulo in permissoes[role]
