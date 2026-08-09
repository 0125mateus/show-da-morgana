"""
Modelos da festa — usando NamedTuple (tupla com nome).

Por que tupla aqui?
- Dados do EVENTO não mudam (data, local, telefone): tupla = imutável.
- Cada CONFIRMAÇÃO, depois de salva, também é um registro fixo.
- NamedTuple = tupla + acesso por nome (confirmacao.nome em vez de confirmacao[0]).

Para listas que crescem (várias confirmações), usamos list + JSON.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import NamedTuple, Literal


class Evento(NamedTuple):
    """Dados fixos da festinha — uma tupla imutável."""

    aniversariante: str
    titulo: str
    idade: int
    data_festa: date
    horario: str
    local: str
    endereco: str
    prazo_confirmacao: date
    whatsapp: str  # só números, com DDI: 5531987318684
    missao: str
    pergunta: str
    hipotese: str


class Confirmacao(NamedTuple):
    """Uma confirmação de presença — também uma tupla."""

    id: str
    nome: str
    adultos: int
    criancas: int
    status: Literal["sim", "nao"]
    mensagem: str
    criado_em: str  # ISO datetime

    @property
    def total_pessoas(self) -> int:
        return self.adultos + self.criancas

    def para_dict(self) -> dict:
        return self._asdict()

    @classmethod
    def de_dict(cls, dados: dict) -> Confirmacao:
        return cls(
            id=dados["id"],
            nome=dados["nome"],
            adultos=int(dados["adultos"]),
            criancas=int(dados["criancas"]),
            status=dados["status"],
            mensagem=dados.get("mensagem", ""),
            criado_em=dados["criado_em"],
        )


# --- Evento da Morgana (preenchido com o convite) ---
EVENTO = Evento(
    aniversariante="Morgana",
    titulo="O Show da Morgana",
    idade=3,
    data_festa=date(2026, 9, 19),
    horario="16h",
    local="Santa Efigênia",
    endereco="Av. Mem de Sá, 115 — Santa Efigênia",
    prazo_confirmacao=date(2026, 9, 9),
    whatsapp="5531987318684",
    missao="Descobrir como fazer o dia mais divertido do universo!",
    pergunta="Será que juntos vamos criar a festa mais científica e divertida?",
    hipotese="Com amigos especiais, a diversão será garantida!",
)


def prazo_aberto(hoje: date | None = None) -> bool:
    """Retorna True se ainda dá para confirmar (até o dia do prazo)."""
    hoje = hoje or date.today()
    return hoje <= EVENTO.prazo_confirmacao


def formatar_data_br(d: date) -> str:
    meses = (
        "janeiro", "fevereiro", "março", "abril", "maio", "junho",
        "julho", "agosto", "setembro", "outubro", "novembro", "dezembro",
    )
    return f"{d.day} de {meses[d.month - 1]}"


def agora_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")
