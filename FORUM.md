# Rascunho do comentário para o fórum

> ⚠️ Os trechos marcados com **[AJUSTE]** devem ser conferidos com o que VOCÊ observar ao rodar os prompts na sua LLM. Troque o texto se sua experiência foi diferente.

---

Olá, pessoal!

Repositório: **[COLE AQUI O LINK DO GITHUB]**

**Cenário:** integração REST entre o Serviço de Pedidos e o Serviço de Pagamentos (que consulta um gateway externo). Regra central: o pedido só vira `PAID` se o pagamento for `APPROVED`.

**Tipos de prompt usados**
1. **Geração de cenários** (papel + contrato da API + formato Gherkin + lista de categorias obrigatórias).
2. **Dados de teste e casos de erro** (few-shot com uma linha de exemplo + restrições de borda, falha e formato CSV).

**Como cada tipo influenciou qualidade e diversidade**
- *Cenários:* a versão genérica ("gere casos de teste de integração para pedidos e pagamentos") **[AJUSTE]** devolveu majoritariamente validação de campo e caminho feliz, que são testes unitários disfarçados. Ao informar o contrato e exigir foco só na interação entre serviços, vieram timeout, indisponibilidade, idempotência e inconsistência de estado.
- *Dados/erros:* sem exemplo, o formato variava a cada execução. Com few-shot e lista explícita de falhas (resposta sem `status`, status desconhecido, HTML com HTTP 500), a massa ficou diversa e diretamente utilizável em mocks.

**Ajustes de prompt que mais ajudaram**
1. Colar o **contrato** (endpoints, códigos de status, regra de negócio). Isso reduziu endpoints inventados.
2. Pedir **categorias obrigatórias** em vez de "seja criativo": aumentou a cobertura de falhas.
3. Definir **formato de saída** (Gherkin com ID e prioridade, CSV com colunas fixas): facilitou transformar em pytest.
4. Delimitar o **escopo negativo** ("não teste validação isolada"): reduziu ruído.
5. Pedir a **justificativa do risco** por cenário: ajudou a priorizar e a descartar cenários redundantes.

**Revisão humana:** **[AJUSTE]** a LLM sugeriu alguns status codes que não estavam no contrato; corrigi manualmente. Também vale lembrar que ela não conhece o comportamento real do sistema, então os resultados esperados precisam ser validados com a especificação.

Alguém usou prompts de contract testing (Pact/OpenAPI)? Fiquei curioso sobre como comparar.
