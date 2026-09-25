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


def test_mapa_filtra_por_plataforma():
    at = abrir("mapa.py")
    assert not at.exception
    assert len(at.dataframe[0].value) == 60

    at.multiselect(key="plataformas").set_value(["TikTok"]).run()

    assert len(at.dataframe[0].value) == 12  # 1 plataforma x 3 categorias x 4 formatos


def test_mapa_sem_celulas_mostra_aviso():
    at = abrir("mapa.py")

    at.multiselect(key="plataformas").set_value([]).run()

    assert not at.exception
    assert any("Nenhuma célula com esses filtros." in i.value for i in at.info)


def metrica(at, rotulo):
    return next(m.value for m in at.metric if m.label == rotulo)


def test_calculadora_padrao_e_20_por_cento_com_cv_1():
    at = abrir("calculadora.py")

    assert not at.exception
    assert metrica(at, "Posts por grupo") == "393"
    assert metrica(at, "Semanas") == "4"


def test_calculadora_responde_as_tres_perguntas():
    at = abrir("calculadora.py")

    at.radio(key="efeito").set_value("10%").run()
    at.number_input(key="posts_semana").set_value(100).run()

    assert metrica(at, "Posts por grupo") == "1.570"
    assert metrica(at, "Semanas") == "32"  # 2 x 1.570 / 100 = 31,4, arredondado para cima


def test_calculadora_outro_efeito_tem_minimo_de_1():
    at = abrir("calculadora.py")

    at.radio(key="efeito").set_value("Outro").run()

    assert at.number_input(key="efeito_outro").min == 1


def test_calculadora_mostra_a_hipotese_escolhida():
    at = abrir("calculadora.py")

    at.radio(key="hipotese").set_value("H1 · fit").run()

    assert any("60,1%" in m.value for m in at.markdown)
