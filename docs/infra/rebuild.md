# Rebuild

O Taz possui um sistema de rebuild que permite reprocessar informações de acordo
com seu escopo, ação e parâmetros adicionais.
Para iniciar o rebuild, basta inserir uma mensagem (com o padrão abaixo)
na fila [SQS](sqs.md) de rebuild.

### Estrutura da mensagem

| Campo | Descrição | Tipo | Obrigatório |
|----------|-----------|----------|----------|
| scope | Escopo a ser reprocessado (`product` ou `price`) | string | Sim |
| action | Ação (`create`, `update` ou `delete`) | string | Sim |
| data | Parâmetros adicionais de acordo com o escopo utilizado | json | Não |

## Escopos

### Seller

Neste escopo é possível reprocessar todos os produtos do seller, a partir da entrada do fluxo de catálogo, desta forma os produtos vão percorrer todo o flow por completo.

| Campo | Descrição | Tipo | Obrigatório |
|----------|-----------|----------| ----------|
| seller_id | Identificador do seller | string | Sim |

#### Exemplo

```json
{
    "scope": "seller",
    "action": "update",
    "data": {
        "seller_id": "magazineluiza"
    }
}
```

### Complete Product by Seller

Neste escopo é possível reprocessar o catálogo de produtos informando um identificador do seller para que todos os produtos ativos, sejam notificados para a fila de `complete_products`.

| Campo | Descrição | Tipo | Obrigatório |
|----------|-----------|----------| ----------|
| seller_id | Identificador do seller | string | Sim |

#### Exemplo

```json
{
    "scope": "complete_products_by_seller",
    "action": "update",
    "data": {
        "seller_id": "magazineluiza"
    }
}
```

### Complete Product by SKU

Neste escopo é possível reprocessar o catálogo de produtos informando uma lista com `sku` e `seller_id`, aonde a lista será notificada na fila de `complete_products`.

| Campo | Descrição | Tipo | Obrigatório |
|----------|-----------|----------| ----------|
| seller_id | Identificador do seller | string | Sim |
| sku | Código do produto | string | Sim |

#### Exemplo

```json
{
    "scope": "complete_products_by_sku",
    "action": "update",
    "data": [
        {"seller_id": "magazineluiza", "sku": "123456789"},
        {"seller_id": "murcho", "sku": "324DE"}
    ]
}
```

### Catalog Notification

Neste escopo é possível reprocessar o catálogo de produtos informando uma lista com `sku` e `seller_id`, aonde a lista será enviar para o SNS de `catalog_notification`.

| Campo | Descrição | Tipo | Obrigatório |
|----------|-----------|----------| ----------|
| seller_id | Identificador do seller | string | Sim |
| sku | Código do produto | string | Sim |

#### Exemplo

```json
{
    "scope": "catalog_notification",
    "action": "update",
    "data": [
        {"seller_id": "magazineluiza", "sku": "123456789"},
        {"seller_id": "murcho", "sku": "324DE"}
    ]
}
```


### Product Score by Seller

Neste escopo é possível reprocessar o score de catálogo de produtos informando um identificador do seller para que todos os produtos, sejam notificados para a fila de `score`.

| Campo | Descrição | Tipo | Obrigatório |
|----------|-----------|----------| ----------|
| seller_id | Identificador do seller | string | Sim |

#### Exemplo

```json
{
    "scope": "product_score_by_seller",
    "action": "update",
    "data": {
        "seller_id": "magazineluiza"
    }
}
```

### Product Score by SKU

Neste escopo é possível reprocessar o score de catálogo de produtos informando uma lista com `sku` e `seller_id` para que todos os produtos, sejam notificados para a fila de `score`.

| Campo | Descrição | Tipo | Obrigatório |
|----------|-----------|----------| ----------|
| seller_id | Identificador do seller | string | Sim |
| sku | Código do produto | string | Sim |

#### Exemplo

```json
{
    "scope": "product_score_by_sku",
    "action": "update",
    "data": [
        {"seller_id": "magazineluiza", "sku": "123456789"},
        {"seller_id": "murcho", "sku": "324DE"}
    ]
}



