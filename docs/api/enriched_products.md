## Produtos Enriquecidos


#### Requisição usando `navigation_id`:
**Exemplo de requisição**

```
curl -X GET http://localhost:5000/enriched_product/0123456?token=TOKEN
```

#### Requisição usando `seller_id` e `sku`:
**Exemplo de requisição**

```
curl -X GET http://localhost:5000/enriched_product/sku/123/seller/epocacosmeticos?token=TOKEN
```

**Códigos de retorno**

| Código | Descrição |
|---|---|
| 200 | Sucesso |
| 404 | Produto enriquecido não encontrado para o navigation id |
| 401 | Não autorizado |

**Exemplo de resposta**
```json
{
  "data": {
      "seller_id": "magazineluiza",
      "product_name_metadata": [
          "Produto",
          "Marca",
          "Modelo",
          "Concentração",
          "Gênero"
      ],
      "filters_metadata": [
          "Produto",
          "Marca",
          "Modelo",
          "Concentração",
          "Gênero",
          "Ocasião",
          "Volume"
      ],
      "source": "omnilogic",
      "metadata": {
          "Modelo": "1 Million",
          "Gênero": "Masculino",
          "Produto": "Perfume",
          "Ocasião": "Diurno",
          "Marca": "Paco Rabanne",
          "Concentração": "Eau de Toilette",
          "Volume": "50ml"
      },
      "sku": "2546",
      "product_matching_metadata": [
          "Produto",
          "Marca",
          "Modelo"
      ],
      "navigation_id": "9452723",
      "sku_metadata": [
          "Volume"
      ],
      "category_id": "CP",
      "product_hash": "b9efe4e50a2529bbe4176812ac208f8a",
      "timestamp": 1524762426.821082
  }
}
```
