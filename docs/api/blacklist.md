## Blacklist

### Inserir blacklist

Insere um novo termo para campo especifíco para a blacklist.

    POST /blacklist
    
**Parâmetros**

| Campo | Descrição | Tipo |
|---|---|---|
| term | termo que deve ser bloqueado | string |
| field | campo aonde deverá conter o termo | string |

**Exemplo de requisição**

```
curl http://localhost:5000/blacklist?token=TOKEN \
-X POST
-d '{"term": "apple", "field": "brand"}'
```

**Códigos de retorno**

| Código | Descrição |
|---|---|
| 201 | Sucesso |
| 400 | Requisição inválida |
| 401 | Não autorizado |

### Deletar blacklist

Deletar um termo existente na blacklist.

    DELETE /blacklist
    
**Parâmetros**

| Campo | Descrição | Tipo |
|---|---|---|
| term | termo que deve ser bloqueado | string |
| field | campo aonde deverá conter o termo | string |

**Exemplo de requisição**

```
curl http://localhost:5000/blacklist?token=TOKEN \
-X DELETE
-d '{"term": "apple", "field": "brand"}'
```

**Códigos de retorno**

| Código | Descrição |
|---|---|
| 201 | Sucesso |
| 400 | Requisição inválida |
| 401 | Não autorizado |

### Listar blacklist

Listar termos cadastrados na blacklist

    GET /blacklist/list
    
**Exemplo de requisição**

```
curl http://localhost:5000/blacklist/list?token=TOKEN \
-X GET
```

**Exemplo de retorno**

```
[
	{
		"term": "apple",
		"field": "brand"
	}
]
```

**Códigos de retorno**

| Código | Descrição |
|---|---|
| 201 | Sucesso |
| 401 | Não autorizado |
