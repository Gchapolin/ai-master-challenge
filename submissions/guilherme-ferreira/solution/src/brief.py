"""Brief de segunda: os números da semana e os grupos que se destacaram, ou não."""
import pandas as pd

from src.celulas import comparar_com_resto
from src.formato import percentual_br

TOTAL = "total"


def semana_padrao(semanas):
    """A semana mais recente com os 7 dias; sem nenhuma completa, a mais recente."""
    completas = semanas[semanas["dias"] == 7]
    return pd.Timestamp((completas if len(completas) else semanas)["semana"].max())


def indicadores_semana(semanas, semana, custo_por_post):
    """Posts e parcela patrocinada; entre os patrocinados, as parcelas sem fit, com divulgação implícita
    e em parceria de um post só; e o gasto estimado nas práticas a parar (posts com algum problema x custo)."""
    linha = semanas.loc[pd.to_datetime(semanas["semana"]) == pd.Timestamp(semana)].iloc[0]
    posts = int(linha["posts"])
    patrocinados = int(linha["patrocinados"])

    def sobre_patrocinados(coluna):
        return float(linha[coluna]) / patrocinados if patrocinados else 0.0

    return {
        "posts": posts,
        "patrocinados": patrocinados / posts if posts else 0.0,
        "sem_fit": sobre_patrocinados("sem_fit"),
        "implicita": sobre_patrocinados("implicita"),
        "um_post_so": sobre_patrocinados("um_post_so"),
        "posts_com_problema": int(linha["algum_problema"]),
        "gasto": int(linha["algum_problema"]) * custo_por_post,
    }


def destaques_semana(semanas_grupos, semana, quantos=3):
    """Os `quantos` grupos acima e abaixo do resto da semana, com a classe da regra de sinal.
    Cada grupo é comparado com os outros posts da mesma semana, com a correção entre todos os grupos."""
    da_semana = semanas_grupos[pd.to_datetime(semanas_grupos["semana"]) == pd.Timestamp(semana)]
    total = da_semana[da_semana["dimensao"] == TOTAL].iloc[0]
    grupos = da_semana[da_semana["dimensao"] != TOTAL][["dimensao", "valor", "n", "media", "var"]].reset_index(drop=True)
    tabela = comparar_com_resto(grupos, total["n"], total["media"], total["var"]).sort_values("lift", ascending=False)
    return pd.concat(
        [tabela.head(quantos).assign(posicao="acima"), tabela.tail(quantos).iloc[::-1].assign(posicao="abaixo")],
        ignore_index=True,
    )


def veredito(destaques):
    """Uma frase para o Head sobre os destaques da semana."""
    sinais = destaques[destaques["classe"] == "sinal"].drop_duplicates(["dimensao", "valor"])
    if sinais.empty:
        return "Nenhum grupo virou sinal: não mude o mix por causa disso."
    partes = [f"{linha.valor} ({percentual_br(linha.lift, 1, sinal=True)})" for linha in sinais.itertuples()]
    return "Virou sinal: " + ", ".join(partes) + ". Confirme com um teste antes de mudar o mix."
