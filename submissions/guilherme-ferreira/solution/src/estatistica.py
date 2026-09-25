"""Regra de sinal definida antes da análise.

Uma diferença só conta como sinal se as três condições valem juntas:
1. passa de 10% sobre a média da base (limiar de efeito prático);
2. continua estatisticamente confiável depois da correção de Benjamini-Hochberg
   para múltiplas comparações (p ajustado < 0,05);
3. vem de pelo menos 30 posts.
"""
import numpy as np
import pandas as pd
from scipy import stats

LIMIAR = 0.10
N_MINIMO = 30
ALFA = 0.05


def welch(n1, media1, var1, n2, media2, var2, confianca=0.95):
    """Compara a média do grupo (1) com a da base (2) pelo teste de Welch, a partir de
    resumos. Aceita números ou arrays. O lift e o intervalo são relativos à média da base."""
    erro1, erro2 = var1 / n1, var2 / n2
    erro_padrao = np.sqrt(erro1 + erro2)
    diferenca = media1 - media2
    graus = (erro1 + erro2) ** 2 / (erro1**2 / (n1 - 1) + erro2**2 / (n2 - 1))
    p = 2 * stats.t.sf(np.abs(diferenca / erro_padrao), graus)
    margem = stats.t.ppf(0.5 + confianca / 2, graus) * erro_padrao
    return {
        "lift": media1 / media2 - 1,
        "ic_inf": (diferenca - margem) / media2,
        "ic_sup": (diferenca + margem) / media2,
        "p": p,
    }


def comparar(grupo, base, confianca=0.95) -> dict:
    """Compara um grupo de posts com a base, métrica por post."""
    g = np.asarray(grupo, dtype="float64")
    b = np.asarray(base, dtype="float64")
    resultado = welch(len(g), g.mean(), g.var(ddof=1), len(b), b.mean(), b.var(ddof=1), confianca)
    return {"n": len(g), "media": g.mean(), "media_base": b.mean(), **{k: float(v) for k, v in resultado.items()}}


def classificar(tabela, limiar=LIMIAR, n_min=N_MINIMO, alfa=ALFA) -> pd.DataFrame:
    """Aplica a regra de sinal a uma tabela com as colunas n, lift e p.

    A correção de Benjamini-Hochberg é feita só entre as linhas com n >= n_min, que são
    as comparações de fato testadas."""
    resultado = tabela.copy()
    testada = resultado["n"] >= n_min
    resultado["p_ajustado"] = np.nan
    if testada.any():
        resultado.loc[testada, "p_ajustado"] = stats.false_discovery_control(
            resultado.loc[testada, "p"].to_numpy(), method="bh"
        )
    confiavel = resultado["p_ajustado"] < alfa
    grande = resultado["lift"].abs() > limiar
    resultado["classe"] = np.select(
        [~testada, confiavel & grande, confiavel],
        ["poucos posts", "sinal", "abaixo do limiar"],
        default="ruído",
    )
    return resultado
