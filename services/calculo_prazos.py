from datetime import datetime, timedelta

FLAG_DIAS = {
    "3 DIAS DENTRO DA CIDADE": 3,
    "5 DIAS FORA DA CIDADE": 5,
    "7 DIAS FORA DO ESTADO": 7
}

def extrair_dias(condicao_pagamento: str) -> int:
    """
    Ex: '35 dias' -> 35
    """
    numeros = [int(s) for s in condicao_pagamento.split() if s.isdigit()]
    if not numeros:
        raise ValueError("Condição de pagamento inválida")
    return numeros[0]


def calcular_vencimentos(condicao_pagamento: str, prazo_estendido_flag: str):
    """
    Retorna:
    - vencimento_normal
    - vencimento_estendido
    """

    hoje = datetime.now().date()

    dias_base = extrair_dias(condicao_pagamento)
    vencimento_normal = hoje + timedelta(days=dias_base)

    dias_extra = FLAG_DIAS.get(prazo_estendido_flag, 0)
    vencimento_estendido = vencimento_normal + timedelta(days=dias_extra)

    return {
        "data_base": hoje,
        "dias_condicao": dias_base,
        "vencimento_normal": vencimento_normal,
        "dias_extra": dias_extra,
        "vencimento_estendido": vencimento_estendido
    }
