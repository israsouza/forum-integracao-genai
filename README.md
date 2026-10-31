# Testes de Integração com GenAI — Pedidos × Pagamentos

Atividade do fórum (Unidade III): uso de prompts para apoiar testes de integração.

## Cenário
`POST /orders` (Serviço de Pedidos) chama `POST /payments` (Serviço de Pagamentos), que consulta um gateway externo.
Pedido só vai a `PAID` se o pagamento for `APPROVED`.

Contrato resumido:

| Endpoint | Request | Respostas |
|---|---|---|
| `POST /orders` | `{customer_id, items:[{sku, qty}], payment_method}` | 201 `{order_id, status}`, 400, 409, 502, 504 |
| `POST /payments` | `{order_id, amount, method}` | 200 `{payment_id, status: APPROVED/DECLINED}`, 422, 503 |
| `GET /orders/{id}` | – | 200 `{status: PENDING/PAID/PAYMENT_FAILED/CANCELLED}`, 404 |

## Tipos de prompt usados
1. **Prompt de geração de cenários** (role + contrato + formato Gherkin) → `prompts/01-cenarios.md`
2. **Prompt de dados de teste e casos de erro** (few-shot + restrições de borda/falha) → `prompts/02-dados-e-erros.md`

## Estrutura
- `prompts/` — prompts (v1 inicial e v2 refinada)
- `tests/cenarios_integracao.md` — casos gerados (Gherkin)
- `tests/test_pedidos_pagamentos.py` — esqueleto pytest executável contra `BASE_URL`
- `data/payloads.csv` — massa de dados
- `FORUM.md` — texto do comentário postado no fórum

> Todo conteúdo gerado por LLM foi revisado manualmente antes de entrar aqui.
