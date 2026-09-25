"""Números no formato brasileiro: ponto no milhar, vírgula no decimal."""


def _trocar_separadores(texto):
    return texto.replace(",", "_").replace(".", ",").replace("_", ".")


def numero_br(valor, casas=0) -> str:
    return _trocar_separadores(f"{valor:,.{casas}f}")


def percentual_br(fracao, casas=1, sinal=False) -> str:
    """0,1234 vira "12,3%". Com sinal=True, positivos ganham "+"."""
    mais = "+" if sinal else ""
    return _trocar_separadores(f"{fracao * 100:{mais},.{casas}f}") + "%"
