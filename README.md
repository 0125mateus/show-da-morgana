# O Show da Morgana — Confirmação de presença

Sistema simples em Python (Flask) para os convidados confirmarem presença na festinha e a família acompanhar a lista.

## Como rodar (local)

```bash
pip install -r requirements.txt
python app.py
```

- Vídeo: http://127.0.0.1:5000/
- Formulário / convite: http://127.0.0.1:5000/confirmar
- Painel da família: http://127.0.0.1:5000/admin

## Deploy no Render

1. Conecte este repositório no [Render](https://render.com)
2. Crie um **Web Service** (ou use o `render.yaml`)
3. Runtime: **Python**
4. Build: `pip install -r requirements.txt`
5. Start: `gunicorn app:app --bind 0.0.0.0:$PORT`
6. Defina a env var `SECRET_KEY` (qualquer texto secreto)

> As confirmações ficam em `data/confirmacoes.json`. No plano gratuito do Render o disco é temporário — se o serviço reiniciar, a lista pode zerar.

## Dados do convite (já cadastrados)

| Campo | Valor |
|--------|--------|
| Aniversariante | Morgana |
| Festa | 19 de setembro · 16h |
| Local | Av. Mem de Sá, 115 — Santa Efigênia |
| Prazo RSVP | até 9 de setembro |
| WhatsApp | (31) 98731-8684 |

## Tuplas: o que usamos e por quê

No arquivo `models.py`:

1. **`Evento` (NamedTuple)** — dados da festa que **não mudam** (data, local, telefone). Tupla = imutável.
2. **`Confirmacao` (NamedTuple)** — cada resposta vira um registro fixo (`nome`, `adultos`, `criancas`, `status`…).

A **lista** de confirmações cresce com o tempo → fica em `data/confirmacoes.json` (lista + dicionários na hora de salvar).

Exemplo mental:

```python
# Uma confirmação é uma tupla nomeada:
("Ana", 2, 1, "sim")  # nome, adultos, crianças, status

# Com NamedTuple fica mais legível:
confirmacao.nome      # em vez de confirmacao[0]
confirmacao.adultos   # em vez de confirmacao[1]
```

## Fluxo

1. Convidado preenche o formulário no site.
2. A confirmação é salva em JSON.
3. Na tela de obrigado, há um botão para **mandar a mesma confirmação no WhatsApp** do convite.
4. No `/admin`, a família vê totais (adultos, crianças, quem não vai).
