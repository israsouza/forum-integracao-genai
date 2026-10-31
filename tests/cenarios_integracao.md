# Cenários de integração — Pedidos × Pagamentos

| ID | Prioridade | Risco de integração |
|---|---|---|
| INT-01 | Alta | Fluxo ponta a ponta |
| INT-02 | Alta | Propagação de recusa |
| INT-03 | Alta | Timeout downstream |
| INT-04 | Alta | Indisponibilidade downstream |
| INT-05 | Alta | Duplicidade de cobrança |
| INT-06 | Média | Contrato violado |
| INT-07 | Média | Status desconhecido |
| INT-08 | Alta | Consistência de estado |
| INT-09 | Baixa | Pedido inexistente |

```gherkin
Feature: Integração Pedidos x Pagamentos

  @INT-01
  Scenario: Pedido pago com sucesso
    Given o serviço de pagamentos responde 200 com status "APPROVED"
    When envio POST /orders com 2 itens válidos e payment_method "CARD"
    Then recebo 201 com status "PAID"
    And GET /orders/{id} retorna status "PAID"
    And o serviço de pagamentos recebeu amount igual à soma dos itens

  @INT-02
  Scenario: Pagamento recusado
    Given o serviço de pagamentos responde 200 com status "DECLINED"
    When envio POST /orders válido
    Then GET /orders/{id} retorna "PAYMENT_FAILED"
    And nenhum estoque permanece reservado

  @INT-03
  Scenario: Timeout no serviço de pagamentos
    Given o serviço de pagamentos demora mais que o timeout configurado
    When envio POST /orders válido
    Then recebo 504
    And o pedido não fica em "PAID"

  @INT-04
  Scenario: Serviço de pagamentos indisponível
    Given o serviço de pagamentos responde 503
    When envio POST /orders válido
    Then recebo 502
    And o pedido fica "PENDING" ou "PAYMENT_FAILED", nunca "PAID"

  @INT-05
  Scenario: Reenvio da mesma requisição não cobra duas vezes
    Given um POST /orders com o header Idempotency-Key "k1" já processado
    When reenvio o mesmo POST /orders com "k1"
    Then recebo o mesmo order_id
    And apenas 1 chamada a POST /payments foi registrada

  @INT-06
  Scenario: Resposta de pagamento sem campo status
    Given o serviço de pagamentos responde 200 com corpo "{}"
    When envio POST /orders válido
    Then recebo 502
    And o erro é registrado em log com o order_id

  @INT-07
  Scenario: Status de pagamento desconhecido
    Given o serviço de pagamentos responde 200 com status "PENDING_REVIEW"
    When envio POST /orders válido
    Then o pedido não é marcado "PAID"

  @INT-08
  Scenario: Pagamento aprovado mas falha ao atualizar o pedido
    Given o pagamento é APPROVED
    And a atualização do pedido para "PAID" falha uma vez
    When o fluxo é reprocessado
    Then o pedido termina "PAID" sem segunda cobrança

  @INT-09
  Scenario: Consulta de pedido inexistente
    When envio GET /orders/inexistente
    Then recebo 404
```
