## Produtos pendentes

### Consulta lista de produtos pendentes

Retorna uma lista de produtos pendentes

    GET /pending/list
    
**Exemplo de requisição**

```
http://localhost:5000/pending/list?token=TOKEN
```

**Exemplo de resposta**

```json
{
	"data": [{
		"reference": "CXB450ML",
		"grade": 500,
		"categories": [{
			"subcategories": [{
				"id": "UDCA"
			}, {
				"id": "UDCG"
			}],
			"id": "UD"
		}],
		"sold_count": 14,
		"seller_description": "Seller A",
		"parent_sku": "82323jjjj3",
		"seller_id": "seller_a",
		"sells_to_company": false,
		"main_variation": false,
		"ean": "3123123999999",
		"review_count": 9,
		"attributes": [{
			"value": "450ml",
			"type": "capacity"
		}],
		"sku": "82323jjjj3",
		"disable_on_matching": false,
		"brand": "Canecas Xablau",
		"review_score": 4,
		"type": "product",
		"description": "Caneca xablau batuta",
		"dimensions": {
			"weight": 0.47,
			"height": 0.44,
			"width": 0.18,
			"depth": 0.13
		},
		"title": "Caneca Xablau Branca - 450ml",
		"updated_at": "2016-08-17T06:17:03.503000",
		"created_at": "2016-08-17T06:17:03.503000"
	}, {
		"reference": "CXB450ML",
		"grade": 500,
		"categories": [{
			"subcategories": [{
				"id": "UDCA"
			}, {
				"id": "UDCG"
			}],
			"id": "UD"
		}],
		"sold_count": 14,
		"seller_description": "Seller B GMBH",
		"parent_sku": "098asdwe28",
		"seller_id": "seller_b",
		"sells_to_company": false,
		"main_variation": false,
		"ean": "3123123999999",
		"review_count": 12,
		"attributes": [{
			"value": "450ml",
			"type": "capacity"
		}],
		"sku": "098asdwe28",
		"disable_on_matching": false,
		"brand": "Canecas Xablau",
		"review_score": 2,
		"type": "product",
		"description": "Caneca xablau bacanuda",
		"dimensions": {
			"weight": 0.47,
			"height": 0.44,
			"width": 0.18,
			"depth": 0.13
		},
		"title": "Caneca Xablau Branca - 450ml",
		"updated_at": "2016-08-17T06:17:03.503000",
		"created_at": "2016-08-17T06:17:03.503000"
	}, {
		"reference": "CXB450ML",
		"grade": 500,
		"categories": [{
			"subcategories": [{
				"id": "UDCA"
			}, {
				"id": "UDCG"
			}],
			"id": "UD"
		}],
		"sold_count": 14,
		"seller_description": "Seller C Ltda",
		"parent_sku": "ou23ou23ou",
		"seller_id": "seller_c",
		"sells_to_company": false,
		"main_variation": false,
		"ean": "3123123999999",
		"review_count": 1,
		"attributes": [{
			"value": "450ml",
			"type": "capacity"
		}],
		"sku": "ou23ou23ou",
		"disable_on_matching": false,
		"brand": "Canecas Xablau",
		"review_score": 5,
		"type": "product",
		"description": "Caneca xablau bacaninha",
		"dimensions": {
			"weight": 0.47,
			"height": 0.44,
			"width": 0.18,
			"depth": 0.13
		},
		"title": "Caneca Xablau Branca - 450ml",
		"updated_at": "2016-08-17T06:17:03.503000",
		"created_at": "2016-08-17T06:17:03.503000"
	}]
}
```

**Códigos de retorno**

| Código | Descrição |
|---|---|
| 200 | Sucesso |
| 401 | Não autorizado |

### Consulta detalhe do produto pendente

Retorna detalhe de um produto pendente

    GET /pending/seller/{seller_id}/sku/{sku}
    
**Parâmetros**

| Campo | Descrição | Tipo |
|---|---|---|
| seller_id | id do seller | string |
| sku | sku do produto | string |
    
**Exemplo de requisição**

```
http://localhost:5000/pending/seller/{seller_id}/sku/{sku}?token=TOKEN
```

**Exemplo de resposta**

```json
{
	"data": {
		"brand": "Canecas Xablau",
		"ean": "3123123999999",
		"review_count": 9,
		"seller_description": "Seller A",
		"created_at": "2016-08-17T06:17:03.503000",
		"parent_sku": "82323jjjj3",
		"sells_to_company": false,
		"disable_on_matching": false,
		"dimensions": {
			"width": 0.18,
			"weight": 0.47,
			"height": 0.44,
			"depth": 0.13
		},
		"categories": [{
			"id": "UD",
			"subcategories": [{
				"id": "UDCA"
			}, {
				"id": "UDCG"
			}]
		}],
		"grade": 500,
		"title": "Caneca Xablau Branca - 450ml",
		"main_variation": false,
		"type": "product",
		"reference": "CXB450ML",
		"description": "Caneca xablau batuta",
		"sold_count": 14,
		"attributes": [{
			"type": "capacity",
			"value": "450ml"
		}],
		"sku": "82323jjjj3",
		"updated_at": "2016-08-17T06:17:03.503000",
		"review_score": 4,
		"seller_id": "seller_a"
	}
}
```

**Códigos de retorno**

| Código | Descrição |
|---|---|
| 200 | Sucesso |
| 401 | Não autorizado |
| 404 | Não encontrado |

### Deleta produto pendente

Deleta um produto que está como pendente

    DELETE /pending/seller/{seller_id}/sku/{sku}
    
**Parâmetros**

| Campo | Descrição | Tipo |
|---|---|---|
| seller_id | id do seller | string |
| sku | sku do produto | string |
    
**Exemplo de requisição**

```
curl http://localhost:5000/pending/seller/magazineluiza/sku/123456789?token=TOKEN \
-X DELETE
```

**Códigos de retorno**

| Código | Descrição |
|---|---|
| 204 | Sucesso |
| 401 | Não autorizado |

### Aprovar produto pendente

Aprova um produto que está como pendente, gravando a estratégia de buybox

    PUT /pending/seller/{seller_id}/sku/{sku}
    
**Parâmetros**

| Campo | Descrição | Tipo |
|---|---|---|
| seller_id | id do seller | string |
| sku | sku do produto | string |
| sellers | lista de sellers para aprovação | list |
| sellers[*].sku | sku do seller | string |
| sellers[*].seller_id | id do seller | string |
    
**Exemplo de requisição**

```
curl http://localhost:5000/pending/seller/magazineluiza/sku/123456789?token=TOKEN \
-X PUT
-d '[{"seller_id": "murcho", "sku": "23423"}]'
```

**Códigos de retorno**

| Código | Descrição |
|---|---|
| 200 | Sucesso |
| 400 | Requisição invalida |
| 401 | Não autorizado |
