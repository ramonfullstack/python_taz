## Badges

### Paginar campanhas de selo

Lista paginada das campanhas de selos cadastradas.

    GET /v1/badges
    
**Parâmetros**

| Campo | Descrição | Tipo |
|---|---|---|
| offset      | quantidade de registros por página | int |
| page_number | número da página                   | int |

**Exemplo de requisição**

```
curl http://localhost:5000/v1/badges?offset=2&page_number=2&token=TOKEN \
-X GET
```

**Exemplo de retorno**

```
{
    "records": [{
        "tool_tip": "Teste",
        "start_at": "2017-09-28T09:50:51+00:00",
        "active": true,
        "products": [{
            "sku": "123456789",
            "seller_id": "magazineluiza"
        }, {
            "sku": "KDJS98",
            "seller_id": "murcho"
        }],
        "end_at": "2017-09-28T09:50:55+00:00",
        "position": "top-right",
        "text": "Teste",
        "slug": "teste",
        "name": "Teste",
        "image_url": "teste",
        "container": "image"
    }],
    "offset": 1,
    "page_number": 1,
    "total_documents": 4,
    "total_pages": 2
}
```

**Códigos de retorno**

| Código | Descrição |
|---|---|
| 200 | Sucesso |

### Listar campanhas de selo

Lista as campanhas de selos cadastradas.

    GET /badge/list
    
**Parâmetros**

| Campo | Descrição | Tipo |
|---|---|---|
| active | retornar campanhas ativas | bool |

**Exemplo de requisição**

```
curl http://localhost:5000/list?token=TOKEN \
-X GET
```
```
curl http://localhost:5000/list?active=true&token=TOKEN \
-X GET
```

**Exemplo de retorno**

```
[{
	"tool_tip": "Teste",
	"start_at": "2017-09-28T09:50:51+00:00",
	"active": true,
	"products": [{
		"sku": "123456789",
		"seller_id": "magazineluiza"
	}, {
		"sku": "KDJS98",
		"seller_id": "murcho"
	}],
	"end_at": "2017-09-28T09:50:55+00:00",
	"position": "top-right",
	"text": "Teste",
	"slug": "teste",
	"name": "Teste",
	"image_url": "teste",
	"container": "image"
}]
```

**Códigos de retorno**

| Código | Descrição |
|---|---|
| 200 | Sucesso |
| 401 | Não autorizado |

### Obter campanha de selo

Obtém uma campanha de selo já existente.

    GET /badge/{slug}
    
**Parâmetros**

| Campo | Descrição | Tipo |
|---|---|---|
| slug | identificador da campanha | string |

**Exemplo de requisição**

```
curl http://localhost:5000/badge/slug?token=TOKEN \
-X GET
```

**Exemplo de retorno**

```
{
    "image_url": "https://a-static.mlcdn.com.br/{w}x{h}/black_fraude.jpg",
    "position": "bottom",
    "container": "information",
    "text": "Melhores oferta é na BLACK FRAUDE da Magazine Luiza - Procure este selo e compre tranquilo que garantimos o melhor preço.",  # noqa
    "tool_tip": "Black Fraude",
    "start_at": "2017-09-21 14:00:00",
    "end_at": "2017-09-21 15:00:00",
    "products": [
        {"sku": "123456789", "seller_id": "magazineluiza"}
    ],
    "name": "Black Fraude"
}
```

**Códigos de retorno**

| Código | Descrição |
|---|---|
| 401 | Não autorizado |
| 404 | Não encontrado |

### Gerenciar campanha de selo

Adiciona uma nova campanha de selo.

    PUT /badge

Atualiza uma campanha de selo já existente.

    POST /badge
    
**Parâmetros**

| Campo | Descrição | Tipo |
|---|---|---|
| image_url | endereço da imagem | string |
| position | posição de exibição | string |
| container | local de exibição | string |
| text | texto descritivo | string |
| tool_tip | pequeno texto descritivo | string |
| start_at | data de início | datetime |
| end_at | data de termino | datetime |
| products | lista de produtos | dict |
| name | nome da campanha | string |

**Exemplo de requisição**

```
curl http://localhost:5000/badge?token=TOKEN \
-X PUT
-d '{
    "image_url": "https://a-static.mlcdn.com.br/{w}x{h}/black_fraude.jpg",
    "position": "bottom",
    "container": "information",
    "text": "Melhores oferta é na BLACK FRAUDE da Magazine Luiza - Procure este selo e compre tranquilo que garantimos o melhor preço.",  # noqa
    "tool_tip": "Black Fraude",
    "start_at": "2017-09-21 14:00:00",
    "end_at": "2017-09-21 15:00:00",
    "products": [
        {"sku": "123456789", "seller_id": "magazineluiza"}
    ],
    "name": "Black Fraude"
}'
```

**Códigos de retorno**

| Código | Descrição |
|---|---|
| 200 | Atualizado com sucesso |
| 201 | Criado com sucesso |
| 400 | Requisição inválida |
| 401 | Não autorizado |

### Deleta campanha de selo

Delete uma campanha de selo já existente.

    DELETE /badge
    
**Parâmetros**

| Campo | Descrição | Tipo |
|---|---|---|
| slug | identificador da campanha | string |

**Exemplo de requisição**

```
curl http://localhost:5000/badge/slug?token=TOKEN \
-X DELETE
```

**Códigos de retorno**

| Código | Descrição |
|---|---|
| 204 | Atualizado com sucesso |
| 401 | Não autorizado |
| 404 | Não encontrado |

### Deletar produto da campanha de selo

Deleta um produto cadastrado em uma campanha de selo já existente.

    DELETE /badge/{slug}/sku/{sku}/seller/{seller_id}
    
**Parâmetros**

| Campo | Descrição | Tipo |
|---|---|---|
| slug | identificador da campanha | string |
| sku | sku do produto | string |
| seller_id | seller id do produto | string |

**Exemplo de requisição**

```
curl http://localhost:5000/badge/{slug}/sku/{sku}/seller/{seller_id}?token=TOKEN \
-X DELETE
```

**Códigos de retorno**

| Código | Descrição |
|---|---|
| 204 | Atualizado com sucesso |
| 401 | Não autorizado |
| 404 | Não encontrado |