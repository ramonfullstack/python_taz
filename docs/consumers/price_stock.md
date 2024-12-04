# Preço / Estoque

Payload necessário para manipulação de preço/estoque.

## Estrutura da mensagem

| Campo | Descrição | Tipo |
|----------|-----------|----------|
| sku | Sku do produto no seller | string |
| seller_id | ID do vendedor | string |
| list_price | Preço De | float |
| price | Preço Por | float |
| delivery_availability | Disponibilidade da entrega (valores descritos logo abaixo na seção apropriada) | string |
| stock_count | Contagem de itens em estoque | integer |
| stock_type | Tipo do estoque (valores descritos logo abaixo na seção apropriada) | string |

### Disponibilidade da entrega

| Nome | Descrição |
|------|-----------|
| nationwide | Nacional (entrega disponível para todo o território brasileiro) |
| regional   | Regional (entrega disponível apenas para algumas regiões do território brasileiro) |
| unavailable| Indisponível (sem estoque disponível para entrega)|

### Tipo do estoque

| Nome | Descrição |
|------|-----------|
| on_seller | Estoque disponível no próprio vendedor |
| on_supplier | Estoque disponível no fornecedor |

## Exemplo

```json
{
    "sku": "012345678",
    "seller_id": "magazineluiza",
    "list_price": 234.56,
    "price": 123.45,
    "delivery_availability": "nationwide",
    "stock_count": 321,
    "stock_type": "on_seller"
}
```
