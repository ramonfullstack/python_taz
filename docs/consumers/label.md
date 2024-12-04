# Label

Aplicação responsável por processar eventos de adição de dados extras (extra_data na coleção raw_products) que configuram campanhas de vendas de produtos. Essa aplicação deve processar apenas 1p pois 3p será originário do maas-product.


## Estrutura da mensagem

| Campo | Descrição | Tipo |
|----------|-----------|---------|
| seller_id | ID do vendedor | string |
| sku | Código sku do produto | string |
| navigation_id | ID do produto | string |
| in_out | Indica incluir/remover o label | string |
| rules_version | Versão da regra para inclusões | string |
| label | Rotulagem do produto | string |

## Exemplo

```json
{ 
    "seller_id": "magazineluiza",
    "sku": "219832400",
    "navigation_id": "219832400",
    "in_out": "in",
    "rules_version": "v0",
    "label": "is_magalu_indica"
}
```
