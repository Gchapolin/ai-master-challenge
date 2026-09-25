from pathlib import Path

import pandas as pd
import pytest

from app.leitura import ResumoAusente, ler_resumo

PASTA_APP = Path(__file__).resolve().parents[1] / "app"


def test_ler_resumo_ausente_diz_como_gerar(tmp_path):
    with pytest.raises(ResumoAusente, match="gerar_resumos.py"):
        ler_resumo("semanas.csv", tmp_path)


def test_ler_resumo_com_coluna_faltando_diz_qual(tmp_path):
    pd.DataFrame({"semana": ["2025-05-19"], "posts": [10]}).to_csv(tmp_path / "semanas.csv", index=False)

    with pytest.raises(ResumoAusente, match="dias"):
        ler_resumo("semanas.csv", tmp_path)


def test_ler_resumo_converte_semana_em_data():
    semanas = ler_resumo("semanas.csv", PASTA_APP / "resumos")

    assert semanas["semana"].dtype.kind == "M"
    assert len(semanas) > 100
