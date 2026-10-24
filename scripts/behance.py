"""Busca os projetos do Behance e atualiza behance.json e as capas em img/behance/.

Roda pela rotina do GitHub (.github/workflows/behance.yml). Usa só a biblioteca padrão do Python.
"""
import html
import json
import os
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET

USUARIO = "ArtieStudio"
FEED = f"https://www.behance.net/feeds/user?username={USUARIO}"
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTA_CAPAS = os.path.join(RAIZ, "img", "behance")
ARQUIVO = os.path.join(RAIZ, "behance.json")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"


def baixar(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def capa_maior(url):
    """O feed traz a capa pequena; tenta as versões maiores primeiro."""
    opcoes = []
    m = re.search(r"/projects/[^/]+/", url)
    if m:
        for tam in ("max_808", "808", "404"):
            opcoes.append(url.replace(m.group(0), f"/projects/{tam}/"))
    opcoes.append(url)
    return list(dict.fromkeys(opcoes))


def main():
    try:
        xml = baixar(FEED)
    except Exception as e:
        print(f"::warning::Não consegui ler o feed do Behance ({e}). Nada foi alterado.")
        return 0

    amostra = xml[:300].decode("utf-8", "replace").replace("\n", " ")
    try:
        raiz = ET.fromstring(xml)
    except ET.ParseError:
        print(f"::warning::O Behance não devolveu um feed válido. Início da resposta: {amostra}")
        return 0
    itens = raiz.findall("./channel/item")
    print(f"::notice::Feed lido: {len(xml)} bytes, {len(itens)} item(ns). Início: {amostra}")
    if itens:
        d = (itens[0].findtext("description") or "")[:300].replace("\n", " ")
        print(f"::notice::Primeiro item: {itens[0].findtext('title')} | {itens[0].findtext('link')} | {d}")
    os.makedirs(PASTA_CAPAS, exist_ok=True)
    projetos = []
    for item in itens:
        nome = html.unescape((item.findtext("title") or "").strip())
        link = (item.findtext("link") or "").strip()
        descricao = item.findtext("description") or ""
        num = re.search(r"gallery/(\d+)", link)
        img = re.search(r"""<img[^>]+src=["']([^"']+)["']""", descricao)
        if not (nome and num and img):
            continue
        destino = os.path.join(PASTA_CAPAS, f"{num.group(1)}.jpg")
        if not os.path.exists(destino):
            for url in capa_maior(img.group(1)):
                try:
                    dados = baixar(url)
                    if len(dados) > 2000:
                        with open(destino, "wb") as f:
                            f.write(dados)
                        break
                except Exception:
                    continue
        if not os.path.exists(destino):
            print(f"::warning::Sem capa para {nome}; projeto ignorado.")
            continue
        projetos.append({
            "nome": nome,
            "tipo": "Ver no Behance",
            "capa": f"img/behance/{num.group(1)}.jpg",
            "capaAlt": f"Capa do projeto {nome}",
            "encaixe": "inteira",
            "link": link,
        })

    if not projetos:
        print("::warning::O feed não trouxe nenhum projeto. Nada foi alterado.")
        return 0

    novo = json.dumps(projetos, ensure_ascii=False, indent=2) + "\n"
    antigo = open(ARQUIVO, encoding="utf-8").read() if os.path.exists(ARQUIVO) else ""
    if novo != antigo:
        with open(ARQUIVO, "w", encoding="utf-8") as f:
            f.write(novo)
    print(f"{len(projetos)} projeto(s) no Behance.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
