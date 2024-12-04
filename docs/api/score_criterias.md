## Criterias

### Listagem de critérios

Lista os critérios de score cadastrados.

    GET /score/criteria/list
    
**Exemplo de requisição**

```
curl http://localhost:5000/score/criteria/list?token=TOKEN \
-X GET
```

**Exemplo de retorno**

```
[{
	'name': 'default',
	'elements': [{
		'criteria': [{
			'max': 30,
			'points': 20,
			'name': 'between_1_and_30_characters',
			'min': 1
		}, {
			'max': 60,
			'points': 30,
			'name': 'between_31_and_60_characters',
			'min': 31
		}, {
			'points': 50,
			'name': 'greater_than_60_characters',
			'min': 60
		}],
		'type': 'range',
		'name': 'title'
	}, {
		'criteria': [{
			'max': 250,
			'points': 20,
			'name': 'between_1_and_250_characters',
			'min': 1
		}, {
			'max': 1000,
			'points': 20,
			'name': 'between_251_and_1000_characters',
			'min': 251
		}, {
			'points': 60,
			'name': 'greater_than_1000_characters',
			'min': 1000
		}],
		'type': 'range',
		'name': 'description'
	}]
}, {
	'name': 'murcho',
	'elements': [{
		'criteria': [{
			'max': 99999,
			'points': 100,
			'name': 'greater_than_1_characters',
			'min': 1
		}],
		'type': 'range',
		'name': 'title'
	}]
}]
```

**Códigos de retorno**

| Código | Descrição |
|---|---|
| 200 | Sucesso |
| 401 | Não autorizado |

### Obter critério

Obtem o critério do score por nome

    GET /score/criteria/{name}
    
**Parâmetros**

| Campo | Descrição | Tipo |
|---|---|---|
| name | identificador do critério | string |

**Exemplo de requisição**

```
curl http://localhost:5000/score/criteria/{name}?token=TOKEN \
-X GET
```

**Exemplo de retorno**

```
{
	'name': 'default',
	'elements': [{
		'criteria': [{
			'max': 30,
			'points': 20,
			'name': 'between_1_and_30_characters',
			'min': 1
		}, {
			'max': 60,
			'points': 30,
			'name': 'between_31_and_60_characters',
			'min': 31
		}, {
			'points': 50,
			'name': 'greater_than_60_characters',
			'min': 60
		}],
		'type': 'range',
		'name': 'title'
	}, {
		'criteria': [{
			'max': 250,
			'points': 20,
			'name': 'between_1_and_250_characters',
			'min': 1
		}, {
			'max': 1000,
			'points': 20,
			'name': 'between_251_and_1000_characters',
			'min': 251
		}, {
			'points': 60,
			'name': 'greater_than_1000_characters',
			'min': 1000
		}],
		'type': 'range',
		'name': 'description'
	}]
}
```

**Códigos de retorno**

| Código | Descrição |
|---|---|
| 200 | Sucesso |
| 401 | Não autorizado |
| 404 | Não encontrado |

### Deletar critério

Deleta um critério de score por nome

    DELETE /score/criteria/{name}
    
**Parâmetros**

| Campo | Descrição | Tipo |
|---|---|---|
| name | identificador do critério | string |

**Exemplo de requisição**

```
curl http://localhost:5000/score/criteria/{name}?token=TOKEN \
-X DELETE
```

**Códigos de retorno**

| Código | Descrição |
|---|---|
| 204 | Sucesso |
| 401 | Não autorizado |
| 404 | Não encontrado |

### Salvar critério

Salvar (criar e atualizar) um critério

    POST /score/criteria
    
**Exemplo de requisição**

```
curl http://localhost:5000/score/criteria?token=TOKEN \
-X POST
-d '{
    "name": "murcho",
    "elements": [
        {
            "name": "title",
            "type": constants.RANGE_TYPE,
            "criteria": [
                {
                    "name": "greater_than_1_characters",
                    "min": 1,
                    "max": 99999,
                    "points": 100
                }
            ]
        }
    ]
}
```

**Códigos de retorno**

| Código | Descrição |
|---|---|
| 200 | Salvo com sucesso |
| 400 | Requisição inválida |
| 401 | Não autorizado |