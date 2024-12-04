## Rebuild

### Notificação de catálogo

Insere os produtos do seller especificado no payload, no SNS de notificação de alteração de produtos por escopo para reprocessamento.

    POST /rebuild/notification

**Parâmetros**

| Campo | Descrição | Tipo |
|---|---|---|
| seller_id | Id do seller | string |
| sku | sku do produto | string |
| navigation_id | navigation_id do produto | string |
| type | escopo da notificação (`product`, `price`, `product_score` ou `enriched_product`) | string |
| action | ação no produto (`create`, `update` ou `delete`) | string |

**Exemplo de requisição**

```
curl http://localhost:5000/rebuild/catalog/notification?token=TOKEN \
-X POST
-d '[{"seller_id": "magazineluiza", "sku": "123456789", "navigation_id": "1234567", "type": "product", "action": "update"}]'
```

**Códigos de retorno**

| Código | Descrição |
|---|---|
| 200 | Sucesso |
| 400 | Requisição inválida |
| 401 | Não autorizado |

### Notificação

Insere os produtos do seller especificado no payload, no SNS de notificação de alteração de produtos.

    POST /rebuild/notification
    
**Parâmetros**

| Campo | Descrição | Tipo |
|---|---|---|
| seller_id | Id do seller | string |

**Exemplo de requisição**

```
curl http://localhost:5000/rebuild/notification?token=TOKEN \
-X POST
-d '{"seller_id": "magazineluiza"}'
```

**Códigos de retorno**

| Código | Descrição |
|---|---|
| 200 | Sucesso |
| 400 | Requisição inválida |
| 401 | Não autorizado |
| 404 | Não encontrado |


### Produtos

Insere os produtos que forem postados e adiciona na fila de `complete_products` para serem reenviados com os dados completos do produto para o SNS.

    POST /rebuild/products
    
**Parâmetros**

| Campo | Descrição | Tipo |
|---|---|---|
| seller_id | Id do seller | string |
| sku | Sku do produto | string |

**Exemplo de requisição**

```
curl http://localhost:5000/rebuild/products?token=TOKEN \
-X POST
-d '[{"seller_id": "magazineluiza", "sku": "123456789"}]'
```

**Códigos de retorno**

| Código | Descrição |
|---|---|
| 200 | Sucesso |
| 400 | Requisição inválida |
| 401 | Não autorizado |


### Score de produtos

Insere os produtos que forem postados e adiciona na fila de `score` para serem reprocessados

    POST /rebuild/score
    
**Parâmetros**

| Campo | Descrição | Tipo |
|---|---|---|
| seller_id | Id do seller | string |

**Exemplo de requisição**

```
curl http://localhost:5000/rebuild/score?token=TOKEN \
-X POST
-d '{"seller_id": "magazineluiza"}'
```

**Códigos de retorno**

| Código | Descrição |
|---|---|
| 200 | Sucesso |
| 400 | Requisição inválida |
| 401 | Não autorizado |
| 404 | Não encontrado |



### Score de produtos por SKU

Insere os produtos que forem postados e adiciona na fila de `score` para serem reprocessados

    POST /rebuild/score/products

**Parâmetros**

| Campo | Descrição | Tipo |
|---|---|---|
| seller_id | Id do seller | string |
| sku | Sku do produto | string |

**Exemplo de requisição**

```
curl http://localhost:5000/rebuild/score/products?token=TOKEN \
-X POST
-d '[{"seller_id": "magazineluiza", "sku": "123456789"}]'
```

**Códigos de retorno**

| Código | Descrição |
|---|---|
| 200 | Sucesso |
| 400 | Requisição inválida |
| 401 | Não autorizado |
| 404 | Não encontrado |

