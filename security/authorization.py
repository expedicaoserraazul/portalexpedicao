import streamlit as st
from database.manager import load

# =========================
# TABELAS
# =========================
PERMISSOES_TABLE = "permissoes"
MODULOS_TABLE = "modulos"

# =========================
# LOADERS
# =========================

def load_permissoes():
    return load(PERMISSOES_TABLE)

def load_modulos():
    return load(MODULOS_TABLE)

# =========================
# RBAC CORE
# =========================

def tem_permissao(modulo: str, acao: str) -> bool:
    """
    Verifica permissão no modelo RBAC:
    role -> modulo -> ação
    """
    if "user" not in st.session_state:
        return False

    role = st.session_state.user.get("role")
    permissoes = load_permissoes()

    if not permissoes:
        return False

    if role not in permissoes:
        return False

    if modulo not in permissoes[role]:
        return False

    return acao in permissoes[role][modulo]

# =========================
# PROTEÇÃO DE TELAS
# =========================

def proteger_tela(modulo: str, acao: str = "view"):
    """
    Bloqueia automaticamente a tela se não houver permissão
    """
    if not tem_permissao(modulo, acao):
        st.error("⛔ Acesso negado — Permissão insuficiente")
        st.stop()

# =========================
# FILTRO DE MÓDULOS (MENU)
# =========================

def modulos_permitidos():
    """
    Retorna os módulos permitidos para o usuário logado
    """
    if "user" not in st.session_state:
        return []

    role = st.session_state.user.get("role")
    permissoes = load_permissoes()

    if not permissoes:
        return []

    if role not in permissoes:
        return []

    return list(permissoes[role].keys())
