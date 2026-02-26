# security/lojas.py

def usuario_tem_acesso_loja(user, loja: str) -> bool:
    """
    Verifica se o usuário pode acessar a loja
    """
    lojas_user = user.get("lojas", [])

    if "Todas" in lojas_user:
        return True

    return loja in lojas_user


def filtrar_por_lojas(user, registros: list, campo_loja: str = "loja"):
    """
    Filtra qualquer lista de registros pelo escopo de lojas do usuário
    """
    lojas_user = user.get("lojas", [])

    # Admin ou acesso total
    if "Todas" in lojas_user:
        return registros

    filtrados = []
    for r in registros:
        loja_registro = r.get(campo_loja)

        if loja_registro in lojas_user:
            filtrados.append(r)

    return filtrados


def lojas_visiveis(user):
    """
    Retorna apenas as lojas que o usuário pode ver
    """
    lojas_user = user.get("lojas", [])

    if "Todas" in lojas_user:
        return [
            "São Geraldo",
            "Conselheiro",
            "Olaria",
            "Mury",
            "Teresópolis",
            "Cordeiro",
            "Centro NF",
            "Bom Jardim"
        ]

    return lojas_user
