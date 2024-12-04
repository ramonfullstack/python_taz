## Produtos

### Consulta lista de produtos

Retorna uma lista de produtos

    GET /product/list
    
**Exemplo de requisição**

```
http://localhost:5000/product/list?token=TOKEN
```

**Exemplo de resposta**

```json
{
	"data": [{
		"review_score": 4,
		"description": "Caneca xablau batuta",
		"attributes": [{
			"value": "450ml",
			"type": "capacity"
		}],
		"grade": 500,
		"sells_to_company": false,
		"updated_at": "2016-08-17T06:17:03.503000",
		"title": "Caneca Xablau Branca - 450ml",
		"dimensions": {
			"width": 0.18,
			"weight": 0.47,
			"height": 0.44,
			"depth": 0.13
		},
		"type": "product",
		"main_variation": false,
		"review_count": 9,
		"seller_id": "seller_a",
		"created_at": "2016-08-17T06:17:03.503000",
		"categories": [{
			"subcategories": [{
				"id": "UDCA"
			}, {
				"id": "UDCG"
			}],
			"id": "UD"
		}],
		"reference": "CXB450ML",
		"parent_sku": "82323jjjj3",
		"ean": "3123123999999",
		"disable_on_matching": false,
		"brand": "Canecas Xablau",
		"sold_count": 14,
		"sku": "82323jjjj3",
		"seller_description": "Seller A",
		"matching_strategy": "SINGLE_SELLER"
	}, {
		"review_score": 2,
		"description": "Caneca xablau bacanuda",
		"attributes": [{
			"value": "450ml",
			"type": "capacity"
		}],
		"grade": 500,
		"sells_to_company": false,
		"updated_at": "2016-08-17T06:17:03.503000",
		"title": "Caneca Xablau Branca - 450ml",
		"dimensions": {
			"width": 0.18,
			"weight": 0.47,
			"height": 0.44,
			"depth": 0.13
		},
		"type": "product",
		"main_variation": false,
		"review_count": 12,
		"seller_id": "seller_b",
		"created_at": "2016-08-17T06:17:03.503000",
		"categories": [{
			"subcategories": [{
				"id": "UDCA"
			}, {
				"id": "UDCG"
			}],
			"id": "UD"
		}],
		"reference": "CXB450ML",
		"parent_sku": "098asdwe28",
		"ean": "3123123999999",
		"disable_on_matching": false,
		"brand": "Canecas Xablau",
		"sold_count": 14,
		"sku": "098asdwe28",
		"seller_description": "Seller B GMBH",
		"matching_strategy": "SINGLE_SELLER"
	}, {
		"review_score": 5,
		"description": "Caneca xablau bacaninha",
		"attributes": [{
			"value": "450ml",
			"type": "capacity"
		}],
		"grade": 500,
		"sells_to_company": false,
		"updated_at": "2016-08-17T06:17:03.503000",
		"title": "Caneca Xablau Branca - 450ml",
		"dimensions": {
			"width": 0.18,
			"weight": 0.47,
			"height": 0.44,
			"depth": 0.13
		},
		"type": "product",
		"main_variation": false,
		"review_count": 1,
		"seller_id": "seller_c",
		"created_at": "2016-08-17T06:17:03.503000",
		"categories": [{
			"subcategories": [{
				"id": "UDCA"
			}, {
				"id": "UDCG"
			}],
			"id": "UD"
		}],
		"reference": "CXB450ML",
		"parent_sku": "ou23ou23ou",
		"ean": "3123123999999",
		"disable_on_matching": false,
		"brand": "Canecas Xablau",
		"sold_count": 14,
		"sku": "ou23ou23ou",
		"seller_description": "Seller C Ltda",
		"matching_strategy": "SINGLE_SELLER"
	}]
}
```

**Códigos de retorno**

| Código | Descrição |
|---|---|
| 200 | Sucesso |
| 401 | Não autorizado |

### Consulta detalhe do produto

Retorna detalhe de um produto

    GET /product/seller/{seller_id}/sku/{sku}
    
**Parâmetros**

| Campo | Descrição | Tipo |
|---|---|---|
| seller_id | id do seller | string |
| sku | sku do produto | string |
    
**Exemplo de requisição**

```
http://localhost:5000/product/list?token=TOKEN
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

### Quantidades de variação por seller

Retorna quantidade de variações de um seller especifico.

    GET /product/variation/[seller_id]/count
    
**Exemplo de requisição**

```
http://localhost:5000/product/variation/magazineluiza/count
```

**Exemplo de resposta**

```json
{
	"data": {
        "unavailable_variations": 1,
        "available_variations": 0,
        "total_variations": 1
    }
}
```

**Códigos de retorno**

| Código | Descrição |
|---|---|
| 200 | Sucesso |
| 401 | Não autorizado |
| 404 | Seller Não encontrado |

### Produtos por EAN

Retorna os produtos por EAN, caso seja um produto `magazineluiza`, será retornado apenas um registro.

    GET /product/ean/[ean]
    
**Exemplo de requisição**

```
http://localhost:5000/product/ean/7899091114962
```

**Exemplo de resposta**

```json
{
	"data": [{
		"images": ["http://pis.static-tst.magazineluiza.com.br/{w}x{h}/baixolao-eletroacustico-michael-bm401dt/magazineluiza/213852800/5cc687071950870af77181dfb585b042.jpg"],
		"brand": "michael",
		"description": "O baixol\u00e3o el\u00e9trico Michael BM401DT SH ( Satin Honey) \u00e9 a escolha ideal para quem deseja um instrumento de sonoridade equilibrada, \u00f3timo padr\u00e3o de constru\u00e7\u00e3o e excelente tocabilidade! \n\n\u00c9 constru\u00eddo com mat\u00e9rias-primas de alto padr\u00e3o! Possui tampo em Spruce, bra\u00e7o em Natowood, escala em Rosewood e laterais e fundo em Mahogany, madeiras de excelente qualidade que valorizam ainda mais o equil\u00edbrio, a proje\u00e7\u00e3o e a defini\u00e7\u00e3o sonora.\n\nPodemos destacar tamb\u00e9m o filete m\u00faltiplo ABS na lateral do corpo, o bel\u00edssimo escudo DropStyle (Tortoise Shell) e o cavalete e headstock com design exclusivo Michael, detalhes que elevam o padr\u00e3o visual, deixando o instrumento ainda mais bonito.\n\nEste contrabaixo oferece recursos importantes! Um deles \u00e9 o novo equalizador Michael, SE-40, acess\u00f3rio que traz afinador digital, bot\u00e3o de phase e controles de volume, graves, m\u00e9dios, agudos e presen\u00e7a para um ajuste perfeito das frequ\u00eancias. \n\nOutro detalhe que podemos ressaltar do BM401 \u00e9 o seu captador Piezo que produz um sinal de excelente qualidade, potencializado todo timbre do instrumento. Al\u00e9m disso, vem com sa\u00eddas P10 e XLR (Balanceada) e encordoamento em bronze, material bastante resistente! \n\nDe b\u00f4nus, traz ainda bateria 9V e chave de regulagem do tensor.\n\n ",
		"dimensions": {
			"width": 0.5,
			"depth": 1.24,
			"height": 0.14,
			"weight": 2.7
		},
		"title": "Baixol\u00e3o Eletroac\u00fastico  - Michael BM401DT",
		"attribute": [{"type": "color", "value": "Vermelho"}]
	}]
}
```

**Códigos de retorno**

| Código | Descrição |
|---|---|
| 200 | Sucesso |
| 401 | Não autorizado |
