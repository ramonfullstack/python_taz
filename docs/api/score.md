# Score

### Média de Score de todo o catálogo

Obtém o score médio (em porcentagem) de todos os produtos do catálogo que já possuam pontuação e também o score por categoria.

    GET /score

**Exemplo de requisição**

```
curl http://localhost:5000/score?token=TOKEN \ -X GET
```

**Exemplo de retorno**

```
{
    "data":{
        "catalog_average_score":70.0,
        "categories":[
            {
                "category_id":"CS",
                "category_description":"Casa e Serviços",
                "catalog_average_score":100.0,
                "timestamp":1555476519.4684415
            },
            {
                "category_id":"BR",
                "category_description":"Bijuterias e Relógios",
                "catalog_average_score":60.0,
                "timestamp":1555476519.4684415
            }
        ]
    }
}
```

**Códigos de retorno**

| Código | Descrição |
|---|---|
| 200 | Sucesso |
| 401 | Não autorizado |
| 404 | Nenhum score encontrado |

### Média de Score de produtos

Obtém o score médio (em porcentagem) de um produto passando `seller` e `sku`.

    GET /score/seller/{seller_id}/sku/{sku}
    
**Parâmetros**

| Campo | Descrição | Tipo |
|---|---|---|
| seller_id | Id do seller | string |
| sku | Sku do seller | string |
| debug | retorna os dados utilizados para calcular a média aritmética | bool |
| show_history | retorna o histórico de score do produto | bool | 

**Exemplo de requisição**

```
curl http://localhost:5000/score/seller/magazineluiza/sku/023384700?token=TOKEN \ -X GET
```

**Exemplo de retorno**

```
{
    "data": {
        "catalog_average_score": 35.0,
        "sku": "023384700",
        "seller_id": "magazineluiza"
    }
}
```

**Códigos de retorno**

| Código | Descrição |
|---|---|
| 200 | Sucesso |
| 401 | Não autorizado |
| 404 | Score para o produto não encontrado |

### Média de Score de Produtos por Seller


Obtém a média (em porcentagem) do score de um seller e suas respectivas categorias passando o `seller_id` 

    GET /score/seller/{seller_id}

**Parâmetros**

| Campo | Descrição | Tipo |
|---|---|---|
| seller_id | id do seller | string |

**Exemplo de requisição**

```
curl http://localhost:5000/score/seller/magazineluiza?token=TOKEN \ -X GET
```

**Exemplo de retorno**

```
{
    "data": {
        "catalog_average_score": 100.0,
        "seller_id": "magazineluiza",
        "categories": [
            {
                "category_id": "FS",
                "category_description": "Ferramentas e Segurança",
                "catalog_average_score": 38.0
            },
            {
                "category_id": "ED",
                "category_description": "Eletrodomésticos",
                "catalog_average_score": 76.0
            },
            {
                "category_id": "BR",
                "category_description": "brinquedos",
                "catalog_average_score": 100.0
            }
        ]
    }
}
```

**Códigos de retorno**

| Código | Descrição |
|---|---|
| 200 | Sucesso |
| 401 | Não autorizado |
| 404 | Nenhum score encontrado para o seller |

### Média de Score de Produtos por Categoria

Obtém a média (em porcentagem) do score de uma categoria passando `category_id` 

    GET /score/category/{category_id}
    
**Parâmetros**

| Campo | Descrição | Tipo |
|---|---|---|
| category_id | id da categoria | string |

**Exemplo de requisição**

```
curl http://localhost:5000/score/category/ga?token=TOKEN \ -X GET
```

**Exemplo de retorno**

```
{
    "data": {
        "catalog_average_score": 100.0,
        "category_id": "GA",
        "category_description": "Games"
    }
}
```

**Códigos de retorno**

| Código | Descrição |
|---|---|
| 200 | Sucesso |
| 401 | Não autorizado |
| 404 | Nenhum score encontrado para a categoria |
