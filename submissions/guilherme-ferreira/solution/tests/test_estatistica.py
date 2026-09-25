import numpy as np
import pandas as pd
import pytest
from scipy import stats

from src.estatistica import classificar, comparar


def test_comparar_mede_lift_sobre_a_media_da_base():
    base = [0.19, 0.20, 0.21] * 20  # média 0,20
    grupo = [0.21, 0.22, 0.23] * 20  # média 0,22

    resultado = comparar(grupo, base)

    assert resultado["n"] == 60
    assert resultado["lift"] == pytest.approx(0.10)


def test_comparar_usa_welch_para_grupos_de_tamanho_e_variacao_diferentes():
    rng = np.random.default_rng(7)
    grupo = rng.normal(0.22, 0.03, size=30)
    base = rng.normal(0.20, 0.005, size=300)
    referencia = stats.ttest_ind(grupo, base, equal_var=False)
    ic = referencia.confidence_interval(confidence_level=0.95)

    resultado = comparar(grupo, base)

    assert resultado["p"] == pytest.approx(referencia.pvalue, rel=1e-9)
    assert resultado["ic_inf"] == pytest.approx(ic.low / base.mean(), rel=1e-9)
    assert resultado["ic_sup"] == pytest.approx(ic.high / base.mean(), rel=1e-9)


def test_classificar_aplica_as_tres_condicoes():
    tabela = pd.DataFrame(
        {
            "celula": [
                "forte",
                "real_mas_pequeno",
                "incerto",
                "poucos",
                "forte_para_baixo",
                "n_no_limite",
                "lift_no_limite",
            ],
            "n": [100, 5000, 100, 20, 100, 30, 100],
            "lift": [0.15, 0.02, 0.20, 0.30, -0.12, 0.15, 0.10],
            "p": [0.001, 1e-6, 0.30, 1e-6, 0.001, 0.001, 0.001],
        }
    )

    classes = classificar(tabela).set_index("celula")["classe"].to_dict()

    assert classes == {
        "forte": "sinal",
        "real_mas_pequeno": "abaixo do limiar",
        "incerto": "ruído",
        "poucos": "poucos posts",
        "forte_para_baixo": "sinal",
        "n_no_limite": "sinal",  # 30 posts já bastam
        "lift_no_limite": "abaixo do limiar",  # precisa passar de 10%
    }


def test_classificar_corrige_para_multiplas_comparacoes():
    # Sozinho, p = 0,04 passaria. Entre 10 comparações, o p ajustado (BH) vira 0,4.
    tabela = pd.DataFrame({"n": [100] * 10, "lift": [0.20] + [0.0] * 9, "p": [0.04] + [0.9] * 9})

    resultado = classificar(tabela)

    assert resultado.loc[0, "p_ajustado"] == pytest.approx(0.4)
    assert resultado.loc[0, "classe"] == "ruído"


def test_classificar_so_corrige_entre_celulas_com_posts_suficientes():
    tabela = pd.DataFrame({"n": [100] + [10] * 9, "lift": [0.20] + [0.0] * 9, "p": [0.04] + [0.9] * 9})

    resultado = classificar(tabela)

    assert resultado.loc[0, "classe"] == "sinal"
