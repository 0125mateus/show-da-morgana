"""
Mini-aula: tupla na confirmação de presença.

Rode: python exemplo_tupla.py
"""

from models import EVENTO, Confirmacao, formatar_data_br

# 1) Tupla "crua" — ordem importa, sem nomes
convidado = ("Ana Clara", 2, 1, "sim")
print("Tupla simples:", convidado)
print("  nome (índice 0):", convidado[0])
print("  adultos (índice 1):", convidado[1])

# 2) NamedTuple — mesma ideia, com nomes (melhor na prática)
c = Confirmacao(
    id="abc123",
    nome="Ana Clara",
    adultos=2,
    criancas=1,
    status="sim",
    mensagem="Mal posso esperar!",
    criado_em="2026-08-09T10:00:00",
)
print("\nNamedTuple:", c)
print("  c.nome =", c.nome)
print("  total de pessoas =", c.total_pessoas)

# 3) Evento também é tupla — não dá para alterar depois
print("\nEvento (imutável):")
print(" ", EVENTO.titulo)
print(" ", formatar_data_br(EVENTO.data_festa), "às", EVENTO.horario)
print(" ", EVENTO.endereco)

try:
    EVENTO.idade = 4  # type: ignore[misc]
except Exception as erro:
    print("\nTentou mudar EVENTO.idade ->", type(erro).__name__)
    print("Tupla nao deixa alterar: isso protege os dados da festa.")

# 4) Lista de tuplas — várias confirmações
lista = [
    Confirmacao("1", "Pedro", 1, 1, "sim", "", "2026-08-10T09:00:00"),
    Confirmacao("2", "Lia", 2, 0, "nao", "", "2026-08-10T10:00:00"),
]
vao = [x for x in lista if x.status == "sim"]
print("\nQuem vai:", [x.nome for x in vao])
print("Pessoas confirmadas:", sum(x.total_pessoas for x in vao))
