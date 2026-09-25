"""Mapa de sinal e ruído por célula (cada combinação das dimensões escolhidas)."""
import numpy as np

from src.estatistica import ALFA, LIMIAR, N_MINIMO, classificar, welch


def mapa_celulas(df, dimensoes, metrica="engajamento", limiar=LIMIAR, n_min=N_MINIMO, alfa=ALFA):
    """Compara cada célula com todos os outros posts e aplica a regra de sinal.

    A média e a variância do resto saem dos totais pela fórmula de combinação de
    variâncias, sem refazer a conta sobre os posts de fora de cada célula."""
    valores = df[metrica].astype("float64")
    n_total = valores.count()
    media_total = valores.mean()
    m2_total = valores.var(ddof=1) * (n_total - 1)

    resumo = (
        df.assign(_valor=valores)
        .groupby(dimensoes, observed=True)["_valor"]
        .agg(n="count", media="mean", var="var")
        .reset_index()
    )
    n, media = resumo["n"], resumo["media"]
    m2 = (resumo["var"] * (n - 1)).fillna(0.0)
    n_resto = n_total - n
    media_resto = (media_total * n_total - media * n) / n_resto
    m2_resto = m2_total - m2 - (media_resto - media) ** 2 * n * n_resto / n_total
    var_resto = m2_resto / (n_resto - 1)

    with np.errstate(divide="ignore", invalid="ignore"):
        comparacao = welch(n, media, resumo["var"], n_resto, media_resto, var_resto)
    tabela = resumo.drop(columns="var").assign(media_resto=media_resto, **comparacao)
    return classificar(tabela, limiar, n_min, alfa)
