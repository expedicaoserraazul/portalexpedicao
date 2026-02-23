import streamlit as st
from database.manager import load_json

PERMISSOES_FILE = "database/permissoes.json"
MODULOS_FILE = "database/modulos.json"

# ---------- LOADERS ----------

def load_permissoes():
    return load_json(PERMISSOES_FILE)

def load_modulos():
    return load_json(MODULOS_FILE)

# ---------- RBAC CORE ----------

def tem_permissao(modulo: str, acao: str) -> bool:
    """
    Verifica permissão por:
    role -> modulo -> ação
    """
    if "user" not in st.session_state:
        return False

    role = st.session_state.user.get("role")
    permissoes = load_permissoes()

    if role not in permissoes:
        return False

    if modulo not in permissoes[role]:
        return False

    return acao in permissoes[role][modulo]

# ---------- PROTEÇÃO DE TELA ----------

def proteger_tela(modulo: str, acao: str = "view"):
    if not tem_permissao(modulo, acao):
        st.error("⛔ Acesso negado — Permissão insuficiente")
        st.stop()

# ---------- FILTRO DE MENU ----------

def modulos_permitidos():
    """
    Retorna apenas módulos permitidos para o usuário logado
    """
    if "user" not in st.session_state:
        return []

    role = st.session_state.user.get("role")
    permissoes = load_permissoes()

    if role not in permissoes:
        return []

    return list(permissoes[role].keys())
