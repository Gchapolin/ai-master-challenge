from pathlib import Path

import pandas as pd
import pytest
from streamlit.testing.v1 import AppTest

from app.leitura import ResumoAusente, ler_resumo
from src.formato import percentual_br

PASTA_APP = Path(__file__).resolve().parents[1] / "app"
PAGINAS = PASTA_APP / "paginas"


def abrir(pagina, timeout=30):
    return AppTest.from_file(str(PAGINAS / pagina), default_timeout=timeout).run()


def valor_em_dolar(texto):
    return int(texto.replace("US$", "").replace(".", "").strip())


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


def test_brief_abre_com_veredito_e_seis_indicadores():
    at = abrir("brief.py")

    assert not at.exception
    assert len(at.metric) == 6
    assert any("não mude o mix" in m.value for m in at.markdown)


def test_brief_gasto_acompanha_o_custo_por_post():
    at = abrir("brief.py")
    gasto_1500 = valor_em_dolar(next(m.value for m in at.metric if m.label == "Gasto nas práticas a parar"))

    at.slider(key="custo_por_post").set_value(1000).run()
    gasto_1000 = valor_em_dolar(next(m.value for m in at.metric if m.label == "Gasto nas práticas a parar"))

    assert gasto_1000 * 3 == gasto_1500 * 2


def test_brief_sem_resumos_mostra_como_gerar(tmp_path, monkeypatch):
    monkeypatch.setenv("RADAR_RESUMOS", str(tmp_path))

    at = abrir("brief.py")

    assert not at.exception
    assert any("gerar_resumos.py" in e.value for e in at.error)


def test_saude_mostra_veredito_e_numeros_do_laudo():
    laudo = dict(zip(*ler_resumo("laudo.csv", PASTA_APP / "resumos").T.values))

    at = abrir("saude.py")
    textos = " ".join(m.value for m in at.markdown)

    assert not at.exception
    assert "Resultado: sem sinal. Operação: sem critério." in textos
    assert all(f"Teste {i}" in textos for i in range(1, 5))
    assert percentual_br(laudo["fit"], 1) in textos
    assert percentual_br(laudo["patrocinadores_um_post"], 1) in textos
