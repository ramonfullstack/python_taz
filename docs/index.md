# Consumers

Os consumidores do Taz são responsáveis por processar e publicar informações no ACME.<br>
Essas informações podem ser: categorias, produtos, mídias, preços ou fichas técnicas.<br>
Cada consumidor executa um processamento específico antes de publicar a informação no seu respectivo destino.

## Kinesis

Todas as informações devem ser postadas diretamente no Kinesis.<br>
Para cada tipo de informação existe um stream específico:

### Sandbox

| Tipo | Stream |
|------|------|
| Categoria | taz-category-sandbox |
| Produto | taz-product-sandbox |
| Mídia | taz-media-sandbox |
| Ficha técnica | taz-factsheet-sandbox |
| Preço | taz-price-sandbox |
| Indexação Produtos | taz-indexing-process-sandbox |

### Produção

| Tipo | Stream |
|------|------|
| Categoria | taz-category |
| Produto | taz-product |
| Mídia | taz-media |
| Ficha técnica | taz-factsheet |
| Preço | taz-price |
| Indexação Produtos | taz-indexing-process |

Todos os recursos da AWS estão localizados na região `us-east-1`.

## Mensagens

Todas as mensagens enviadas para o Kinesis devem possuir o mesmo formato. Apenas dois campos são necessários:

- Campo `action` informa a ação que está sendo executada (`create`, `update` ou `delete`)
- Campo `data` contém a informação de acordo com o stream utilizado:

    - [Categoria](consumers/category.md)
    - [Produto](consumers/product.md)
    - [Mídia](consumers/media.md)
    - [Preço e estoque](consumers/price_stock.md)
    - [Ficha técnica](consumers/factsheet.md)

### Exemplo

Enviando um novo preço e estoque para o Kinesis:

```json
{
    "action": "create",
    "data": {
        "sku": "012345678",
        "seller_id": "magazineluiza",
        "list_price": 234.56,
        "price": 123.45,
        "delivery_availability": "nationwide",
        "stock_count": 321,
        "stock_type": "on_seller"
    }
}
```
