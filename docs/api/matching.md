## Matching

### Consulta matching entre produtos

Retorna payload do matching entre produtos

    GET /matching/seller/{seller_id}/sku/{sku}
    
**Parâmetros**

| Campo | Descrição | Tipo |
|---|---|---|
| seller_id | id do seller | string |
| sku | sku do produto | string |

**Exemplo de requisição**

```
http://localhost:5000/matching/seller/magazineluiza/sku/1234567890?token=TOKEN
```

**Exemplo de resposta**

```json
{
	"data": {
		"categories": [{
			"id": "UD",
			"subcategories": [{
				"id": "UDCA"
			}, {
				"id": "UDCG"
			}]
		}],
		"description": "Caneca xablau batuta",
		"type": "product",
		"url": "caneca-xablau-branca-450ml-cxb450ml/p/99osz5j/ud/udca/",
		"attributes": {
			"capacity": {
				"label": "Capacidade",
				"type": "capacity",
				"values": ["450ml"]
			}
		},
		"title": "Caneca Xablau Branca - 450ml",
		"brand": "Canecas Xablau",
		"variations": [{
			"dimensions": {
				"weight": 0.47,
				"height": 0.44,
				"width": 0.18,
				"depth": 0.13
			},
			"updated_at": "2016-08-17T06:17:03.503000",
			"sellers": [{
				"description": "Seller A",
				"sku": "82323jjjj3",
				"id": "seller_a",
				"sells_to_company": false
			}, {
				"description": "Seller B GMBH",
				"sku": "098asdwe28",
				"id": "seller_b",
				"sells_to_company": false
			}, {
				"description": "Seller C Ltda",
				"sku": "ou23ou23ou",
				"id": "seller_c",
				"sells_to_company": false
			}],
			"attributes": [{
				"label": "Capacidade",
				"type": "capacity",
				"value": "450ml"
			}],
			"factsheet": {
				"seller_id": "seller_a",
				"seller_sku": "82323jjjj3"
			},
			"created_at": "2016-08-17T06:17:03.503000",
			"url": "caneca-xablau-branca-450ml-cxb450ml/p/996bufk/ud/udca/",
			"ean": "3123123999999",
			"id": "996bufk"
		}],
		"canonical_ids": ["99osz5j"],
		"review_score": 3.7,
		"reference": "CXB450ML",
		"review_count": 22,
		"id": "99osz5j"
	}
}
```

**Códigos de retorno**

| Código | Descrição |
|---|---|
| 200 | Sucesso |
| 401 | Não autorizado |
| 404 | Não encontrado |
