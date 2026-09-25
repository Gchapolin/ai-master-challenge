import math
import sys
from pathlib import Path

PASTA_APP = Path(__file__).resolve().parents[1]
for pasta in (PASTA_APP, PASTA_APP.parent):
    if str(pasta) not in sys.path:
        sys.path.insert(0, str(pasta))

import altair as alt  # noqa: E402
import pandas as pd  # noqa: E402
import streamlit as st  # noqa: E402

import tema  # noqa: E402
from leitura import carregar_resumos  # noqa: E402
from src.formato import numero_br, percentual_br  # noqa: E402

OBJETIVOS = {
    "engajamento": "Engajamento (likes, shares e comentários por view)",
    "alcance": "Alcance (views)",
    "conversa": "Conversa (comentários por view)",
    "compartilhamento": "Compartilhamento (shares por view)",
}
CLASSES = ["sinal", "abaixo do limiar", "ruído", "poucos posts"]


def preparar(celulas):
    return celulas.assign(
        celula=celulas["platform"] + " · " + celulas["content_category"] + " · " + celulas["content_type"],
        diferenca=celulas["lift"] * 100,
        inicio=celulas["ic_inf"] * 100,
        fim=celulas["ic_sup"] * 100,
        diferenca_txt=celulas["lift"].map(lambda v: percentual_br(v, 2, sinal=True)),
        intervalo_txt=[
            f"{percentual_br(a, 2, sinal=True)} a {percentual_br(b, 2, sinal=True)}"
            for a, b in zip(celulas["ic_inf"], celulas["ic_sup"])
        ],
        posts_txt=celulas["n"].map(numero_br),
    ).sort_values("diferenca", ascending=False)


def grafico(dados):
    limite = max(12, math.ceil(max(dados["fim"].abs().max(), dados["inicio"].abs().max())) + 1)
    x = alt.X(
        "inicio:Q", title="diferença contra o resto dos posts", scale=alt.Scale(domain=[-limite, limite]),
        axis=alt.Axis(labelExpr="datum.value + '%'", grid=False),
    )
    y = alt.Y("celula:N", sort=list(dados["celula"]), title=None, axis=alt.Axis(labelLimit=260))
    faixa = alt.Chart(pd.DataFrame({"de": [-10], "ate": [10]})).mark_rect(color=tema.DOURADO, opacity=0.12).encode(x="de:Q", x2="ate:Q")
    limites = alt.Chart(pd.DataFrame({"x": [-10, 10]})).mark_rule(color=tema.DOURADO_ESCURO, strokeWidth=1).encode(x="x:Q")
    intervalos = alt.Chart(dados).mark_rule(color=tema.AZUL, strokeWidth=2).encode(x=x, x2="fim:Q", y=y)
    pontos = alt.Chart(dados).mark_point(filled=True, size=70, color=tema.AZUL, stroke="#FFFFFF", strokeWidth=2).encode(
        x="diferenca:Q",
        y=y,
        tooltip=[
            alt.Tooltip("celula:N", title="célula"),
            alt.Tooltip("posts_txt:N", title="posts"),
            alt.Tooltip("diferenca_txt:N", title="diferença"),
            alt.Tooltip("intervalo_txt:N", title="intervalo de 95%"),
            alt.Tooltip("classe:N", title="classe"),
        ],
    )
    return (
        (faixa + limites + intervalos + pontos)
        .properties(height=max(220, 18 * len(dados)))
        .configure(font="Manrope")
        .configure_axis(labelColor=tema.AZUL, titleColor=tema.AZUL, domainColor="#C3C2B7", tickColor="#C3C2B7")
        .configure_view(stroke=None)
    )


def main():
    tema.cabecalho("Mapa de sinal e", "ruído")
    resumos = carregar_resumos("celulas.csv")
    if resumos is None:
        return
    celulas = resumos[0]

    objetivo = st.radio("Objetivo", list(OBJETIVOS), format_func=OBJETIVOS.get, horizontal=True, key="objetivo")
    do_objetivo = celulas[celulas["objetivo"] == objetivo]
    contagem = do_objetivo["classe"].value_counts().reindex(CLASSES, fill_value=0)
    st.caption(
        f"{len(do_objetivo)} células de plataforma, categoria e formato: "
        + ", ".join(f"{numero_br(v)} {k}" for k, v in contagem.items())
        + ". Os filtros só escondem células; a classe vem do mapa completo."
    )

    coluna1, coluna2, coluna3 = st.columns(3)
    todas_plataformas = sorted(celulas["platform"].unique())
    todas_categorias = sorted(celulas["content_category"].unique())
    todos_formatos = sorted(celulas["content_type"].unique())
    plataformas = coluna1.multiselect("Plataformas", todas_plataformas, default=todas_plataformas, key="plataformas")
    categorias = coluna2.multiselect("Categorias", todas_categorias, default=todas_categorias, key="categorias")
    formatos = coluna3.multiselect("Formatos", todos_formatos, default=todos_formatos, key="formatos")

    visiveis = do_objetivo[
        do_objetivo["platform"].isin(plataformas)
        & do_objetivo["content_category"].isin(categorias)
        & do_objetivo["content_type"].isin(formatos)
    ]
    if visiveis.empty:
        st.info("Nenhuma célula com esses filtros.")
        return

    dados = preparar(visiveis)
    st.altair_chart(grafico(dados), width="stretch")
    st.dataframe(
        dados[["celula", "posts_txt", "diferenca_txt", "intervalo_txt", "classe"]].rename(
            columns={
                "celula": "Célula", "posts_txt": "Posts", "diferenca_txt": "Diferença",
                "intervalo_txt": "Intervalo de 95%", "classe": "Classe",
            }
        ),
        hide_index=True,
    )
    st.caption("Faixa dourada: de -10% a +10%. Dentro dela, nenhuma diferença conta como sinal.")


main()
