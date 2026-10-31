# Prompt 1 — Geração de cenários de integração

## v1 (inicial, genérico)
```
Gere casos de teste de integração para um sistema de pedidos e pagamentos.
```

## v2 (refinado)
```
Atue como engenheiro de QA sênior especialista em testes de integração de APIs REST.

Contexto: o Serviço de Pedidos chama o Serviço de Pagamentos, que chama um gateway externo.
Contrato:
- POST /orders {customer_id, items:[{sku, qty}], payment_method} -> 201 | 400 | 409 | 502 | 504
- POST /payments {order_id, amount, method} -> 200 {status: APPROVED|DECLINED} | 422 | 503
- GET /orders/{id} -> 200 {status: PENDING|PAID|PAYMENT_FAILED|CANCELLED} | 404
Regra: pedido só vira PAID se o pagamento for APPROVED.

Tarefa: gere cenários focados EXCLUSIVAMENTE na interação entre os serviços
(não teste validação isolada de campos de um serviço).

Cubra obrigatoriamente: caminho feliz, pagamento recusado, timeout do pagamento,
serviço de pagamentos indisponível, idempotência/reenvio, inconsistência de estado
entre serviços e contrato violado (campo ausente/tipo errado na resposta).

Formato: Gherkin (Dado/Quando/Então), um ID por cenário (INT-01...), prioridade (Alta/Média/Baixa)
e a justificativa do risco de integração em uma linha. Não invente endpoints fora do contrato.
```
