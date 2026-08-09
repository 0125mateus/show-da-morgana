"""Persistência das confirmações em JSON (lista de tuplas serializadas)."""

from __future__ import annotations

import json
import uuid
from pathlib import Path

from models import Confirmacao, agora_iso

DATA_DIR = Path(__file__).resolve().parent / "data"
ARQUIVO = DATA_DIR / "confirmacoes.json"


def _garantir_arquivo() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not ARQUIVO.exists():
        ARQUIVO.write_text("[]", encoding="utf-8")


def listar() -> list[Confirmacao]:
    _garantir_arquivo()
    bruto = json.loads(ARQUIVO.read_text(encoding="utf-8"))
    return [Confirmacao.de_dict(item) for item in bruto]


def salvar_lista(confirmacoes: list[Confirmacao]) -> None:
    _garantir_arquivo()
    dados = [c.para_dict() for c in confirmacoes]
    ARQUIVO.write_text(
        json.dumps(dados, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def adicionar(
    nome: str,
    adultos: int,
    criancas: int,
    status: str,
    mensagem: str = "",
) -> Confirmacao:
    confirmacoes = listar()
    nova = Confirmacao(
        id=str(uuid.uuid4())[:8],
        nome=nome.strip(),
        adultos=max(0, int(adultos)),
        criancas=max(0, int(criancas)),
        status="sim" if status == "sim" else "nao",
        mensagem=(mensagem or "").strip()[:280],
        criado_em=agora_iso(),
    )
    confirmacoes.append(nova)
    salvar_lista(confirmacoes)
    return nova


def excluir(confirmacao_id: str) -> bool:
    """Remove uma confirmação pelo id. Retorna True se achou e apagou."""
    confirmacoes = listar()
    nova_lista = [c for c in confirmacoes if c.id != confirmacao_id]
    if len(nova_lista) == len(confirmacoes):
        return False
    salvar_lista(nova_lista)
    return True


def resumo() -> dict:
    """Agrega totais a partir da lista de tuplas."""
    confirmacoes = listar()
    vao = [c for c in confirmacoes if c.status == "sim"]
    nao_vao = [c for c in confirmacoes if c.status == "nao"]
    return {
        "total_respostas": len(confirmacoes),
        "confirmados": len(vao),
        "nao_vao": len(nao_vao),
        "adultos": sum(c.adultos for c in vao),
        "criancas": sum(c.criancas for c in vao),
        "pessoas": sum(c.total_pessoas for c in vao),
    }
