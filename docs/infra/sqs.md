# SQS

Relação de filas internas utilizadas pelo TAZ.

### Sandbox

| Nome | Descrição |
|------|------|
| taz-match-products-sandbox | Fila para processamento de unificação de produtos |
| taz-product-writer-sandbox | Fila para envio de produto unificado para o ACME |
| taz-rebuild-products-sandbox | Fila para acionamento de gatilho de rebuild |
| taz-score-sandbox | Fila para processar score do catálogo |

### Produção

| Nome | Descrição |
|------|------|
| taz-match-products | Fila para processamento de unificação de produtos |
| taz-product-writer | Fila para envio de produto unificado para o ACME |
| taz-rebuild-products | Fila para acionamento de gatilho de rebuild |
| taz-score | Fila para processar score do catálogo |

Todos os recursos da AWS estão localizados na região `us-east-1`.
