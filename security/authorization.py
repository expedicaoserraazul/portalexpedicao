import streamlit as st
from database.manager import load

# =========================
# RBAC REAL + DAL
# =========================

def get_user():
    if "user" not in st.session_state:
        return None
    return st.session_state.user

def get_role():
    user = get_user()
    if not user:
        return None
    return user.get("role")

# ---------- LOADERS ----------

def load_permissoes():
    return load("permissoes")

def load_modulos():
    return load("modulos")

# ---------- AUTORIZAÇÃO ----------

def tem_permissao(modulo: str, acao: str) -> bool:
    """
    Verifica permissão real por ação (RBAC)
    Ex: tem_permissao("fornecedores", "write")
    """
    role = get_role()
    if not role:
        return False

    permissoes = load_permissoes()

    if role not in permissoes:
        return False

    if modulo not in permissoes[role]:
        return False

    return acao in permissoes[role][modulo]

# ---------- FILTRO DE MÓDULOS (MENU) ----------

def modulos_permitidos():
    """
    Retorna módulos permitidos para o menu lateral
    """
    role = get_role()
    if not role:
        return []

    permissoes = load_permissoes()

    if role not in permissoes:
        return []

    # permissoes[role] agora é dict {modulo: [acoes]}
    return list(permissoes[role].keys())
