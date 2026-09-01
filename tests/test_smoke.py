"""Testes de fumaça: verificam que os módulos do framework importam e os scripts compilam."""

import importlib
import pathlib
import py_compile

SCRIPTS_DIR = pathlib.Path(__file__).resolve().parents[1] / "scripts"

MODULOS = [
    "scripts.cli",
    "scripts.gerar_monografia",
    "scripts.formata_documento",
    "scripts.formatador_abnt",
    "scripts.contar_palavras",
    "scripts.extrair_pdf",
    "scripts.criar_template",
    "scripts.sincronizar_termos_ingles",
    "scripts.material",
    "scripts.formatacao.abnt",
]


def test_todos_os_scripts_compilam():
    for py in SCRIPTS_DIR.rglob("*.py"):
        py_compile.compile(str(py), doraise=True)


def test_modulos_importam():
    for modulo in MODULOS:
        importlib.import_module(modulo)


def test_cli_tem_subcomandos():
    from scripts.cli import SUBCOMANDOS

    for esperado in ["gerar", "formatar", "figuras", "palavras", "template", "termos", "material"]:
        assert esperado in SUBCOMANDOS


def test_termos_base_e_config_somados(tmp_path):
    import scripts.formatacao.abnt as abnt

    assert "multi-cloud" in abnt.TERMOS_INGLES  # vindo de config/termos_ingles.txt
    assert "cloud" in abnt.TERMOS_INGLES  # vindo da base genérica

    extras = tmp_path / "termos.txt"
    extras.write_text("# comentario\n\nad hoc\ndata lake\nmulti-cloud\n", encoding="utf-8")
    somados = abnt.todos_termos_ingles(extras)
    assert "data lake" in somados
    assert "ad hoc" in somados  # base + extra


def test_sincronizar_termos_adiciona_sem_duplicar(tmp_path):
    from scripts.sincronizar_termos_ingles import adicionar_termos

    p = tmp_path / "termos.txt"
    p.write_text("# t\n\nbatch\n", encoding="utf-8")
    n = adicionar_termos(["data lake", "multi-cloud", "batch"], p)
    assert n == 2  # já existia "batch"
    conteudo = p.read_text(encoding="utf-8")
    assert p.read_text(encoding="utf-8").count("batch") == 1
    assert "data lake" in conteudo and "multi-cloud" in conteudo


def test_material_extrai_e_dedup_urls():
    from scripts.material import extrair_urls

    texto = "veja https://exemplo.com/artigo e https://exemplo.com/artigo, " \
            "fim https://docs.site/guia.pdf."
    urls = extrair_urls(texto)
    assert urls == ["https://exemplo.com/artigo", "https://docs.site/guia.pdf"]


def test_material_ler_links_ignora_comentarios(tmp_path):
    from scripts.material import ler_links

    p = tmp_path / "links.md"
    p.write_text("# comentario\n\nhttps://exemplo.com/mat\nhttps://docs.site/x.pdf\n", encoding="utf-8")
    assert ler_links(p) == ["https://exemplo.com/mat", "https://docs.site/x.pdf"]
