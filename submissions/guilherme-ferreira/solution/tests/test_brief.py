import numpy as np
import pandas as pd

from src.brief import destaques_semana, indicadores_semana, semana_padrao, veredito


def semanas_exemplo():
    return pd.DataFrame(
        {
            "semana": pd.to_datetime(["2025-05-12", "2025-05-19", "2025-05-26"]),
            "dias": [7, 7, 3],
            "posts": [500, 400, 200],
            "patrocinados": [200, 100, 0],
            "sem_fit": [120, 60, 0],
            "implicita": [90, 50, 0],
            "so_hashtag": [50, 30, 0],
            "um_post_so": [140, 70, 0],
            "algum_problema": [190, 95, 0],
        }
    )


def grupos_da_semana(semente=2):
    """Uma semana com quatro grupos: A rende 30% a mais em 30 posts; B e C rendem igual; D tem só 10 posts."""
    rng = np.random.default_rng(semente)
    posts = pd.concat(
        [
            pd.DataFrame({"valor": nome, "y": rng.normal(media, 0.01, n)})
            for nome, media, n in [("A", 0.26, 30), ("B", 0.20, 100), ("C", 0.20, 100), ("D", 0.20, 10)]
        ],
        ignore_index=True,
    )
    grupos = posts.groupby("valor")["y"].agg(n="count", media="mean", var="var").reset_index().assign(dimensao="platform")
    total = pd.DataFrame({"valor": ["total"], "dimensao": ["total"], "n": [len(posts)], "media": [posts["y"].mean()], "var": [posts["y"].var()]})
    return pd.concat([grupos, total], ignore_index=True).assign(semana=pd.Timestamp("2025-05-19"))


def test_semana_padrao_e_a_ultima_completa():
    assert semana_padrao(semanas_exemplo()) == pd.Timestamp("2025-05-19")


def test_semana_padrao_sem_semana_completa_usa_a_ultima():
    assert semana_padrao(semanas_exemplo().assign(dias=3)) == pd.Timestamp("2025-05-26")


def test_indicadores_semana_divide_problemas_pelos_patrocinados():
    ind = indicadores_semana(semanas_exemplo(), pd.Timestamp("2025-05-19"), custo_por_post=1500)

    assert ind == {
        "posts": 400, "patrocinados": 0.25, "sem_fit": 0.60, "implicita": 0.50,
        "um_post_so": 0.70, "posts_com_problema": 95, "gasto": 142_500,
    }


def test_indicadores_semana_sem_patrocinados():
    ind = indicadores_semana(semanas_exemplo(), pd.Timestamp("2025-05-26"), custo_por_post=1500)

    assert (ind["patrocinados"], ind["sem_fit"], ind["implicita"], ind["um_post_so"], ind["gasto"]) == (0.0, 0.0, 0.0, 0.0, 0)


def test_destaques_poem_o_grupo_com_efeito_no_topo():
    destaques = destaques_semana(grupos_da_semana(), pd.Timestamp("2025-05-19"), quantos=1)

    assert destaques["posicao"].tolist() == ["acima", "abaixo"]
    assert destaques.loc[0, "valor"] == "A"
    assert destaques.loc[0, "classe"] == "sinal"
    assert destaques.loc[1, "classe"] != "sinal"


def test_destaques_marcam_grupo_pequeno_como_poucos_posts():
    destaques = destaques_semana(grupos_da_semana(), pd.Timestamp("2025-05-19"), quantos=4)

    assert destaques.set_index("valor").loc["D", "classe"].tolist()[0] == "poucos posts"


def test_veredito_sem_sinal():
    destaques = pd.DataFrame({"dimensao": ["platform"], "valor": ["TikTok"], "lift": [0.004], "classe": ["ruído"]})

    assert veredito(destaques) == "Nenhum grupo virou sinal: não mude o mix por causa disso."


def test_veredito_com_sinal():
    destaques = pd.DataFrame(
        {"dimensao": ["platform", "platform"], "valor": ["TikTok", "TikTok"], "lift": [0.152, 0.152], "classe": ["sinal", "sinal"]}
    )

    assert veredito(destaques) == "Virou sinal: TikTok (+15,2%). Confirme com um teste antes de mudar o mix."
