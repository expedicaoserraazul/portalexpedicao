from database.manager import load

def get_permissions(role):
    permissoes = load("permissoes")
    return permissoes.get(role, [])

def has_permission(user, module):
    if not user:
        return False

    role = user.get("role")
    perms = get_permissions(role)

    if "ALL" in perms:
        return True

    return module in perms
