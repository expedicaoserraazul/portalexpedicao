import json
from pathlib import Path

BASE_PATH = Path("data")
BASE_PATH.mkdir(exist_ok=True)


def load(nome_arquivo):
    caminho = BASE_PATH / f"{nome_arquivo}.json"
    if not caminho.exists():
        return {}

    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)


def save(nome_arquivo, dados):
    caminho = BASE_PATH / f"{nome_arquivo}.json"
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)
