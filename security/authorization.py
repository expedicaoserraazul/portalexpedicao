import json
import os

PERMISSOES_FILE = "database/permissoes.json"
MODULOS_FILE = "database/modulos.json"

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

# ---------- AUTORIZAÇÃO ----------

def tem_permissao(role: str, modulo: str) -> bool:
    permissoes = load_permissoes()

    if role not in permissoes:
        return False

    return modulo in permissoes[role]

def filtrar_modulos_por_role(role: str):
    modulos = load_modulos()
    permissoes = load_permissoes()

    if role not in permissoes:
        return []

    permitidos = permissoes[role]
    return [m for m in modulos if m in permitidos]
