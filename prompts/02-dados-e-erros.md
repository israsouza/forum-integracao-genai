# Prompt 2 — Dados de teste e casos de erro (few-shot)

## v1 (inicial)
```
Crie dados de teste para a API de pedidos.
```

## v2 (refinado, com exemplo e restrições)
```
Com base no contrato de POST /orders e POST /payments (anexo no prompt 1), gere massa de dados em CSV
com as colunas: id, descricao, payload_json, status_esperado, servico_origem_do_erro.

Inclua:
- 3 válidos (1 item, vários itens, valor alto)
- Valores de borda: qty=0, qty=-1, qty=999999, amount com 3 casas decimais
- Falhas de integração: resposta do pagamento sem campo "status", status desconhecido ("PENDING_REVIEW"),
  corpo vazio, JSON malformado, HTTP 500 com HTML, latência > timeout
- Unicode e injeção em customer_id (ex.: "'; DROP TABLE--")

Exemplo de linha esperada:
D01,"pedido simples","{""customer_id"":""c1"",""items"":[{""sku"":""A1"",""qty"":1}],""payment_method"":""CARD""}",201,-

Restrições: máx. 20 linhas, sem dados pessoais reais, status_esperado deve ser um código do contrato.
```
