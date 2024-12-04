## Pontuação de pesos

### Listagem de pesos

Lista os pesos de score cadastrados.

    GET /score/weight/list
    
**Exemplo de requisição**

```
curl http://localhost:5000/score/weight/list?token=TOKEN \
-X GET
```

**Exemplo de retorno**

```
[
    {
        "entity_name": "default",
        "criteria_name": "titles",
        "weight": 30
    },
    {
        "entity_name": "default",
        "criteria_name": "description",
        "weight": 30
    },
    {
        "entity_name": "livros",
        "criteria_name": "titles",
        "weight": 100
    }
]
```

**Códigos de retorno**

| Código | Descrição |
|---|---|
| 200 | Sucesso |
| 401 | Não autorizado |

### Obter peso

Obtem o peso do score por nome

    GET /score/weight/{entity_name}/{criteria_name}
    
**Parâmetros**

| Campo | Descrição | Tipo |
|---|---|---|
| entity_name | identificador da entidade | string |
| criteria_name | identificador do critério | string |

**Exemplo de requisição**

```
curl http://localhost:5000/score/weight/{entity_name}/{criteria_name}?token=TOKEN \
-X GET
```

**Exemplo de retorno**

```
{
    "entity_name": "livros",
    "criteria_name": "titles",
    "weight": 100
}
```

**Códigos de retorno**

| Código | Descrição |
|---|---|
| 200 | Sucesso |
| 401 | Não autorizado |
| 404 | Não encontrado |

### Deletar peso

Deleta um peso de score por nome

    DELETE /score/weight/{entity_name}/{criteria_name}
    
**Parâmetros**

| Campo | Descrição | Tipo |
|---|---|---|
| entity_name | identificador da entidade | string |
| criteria_name | identificador do critério | string |

**Exemplo de requisição**

```
curl http://localhost:5000/score/weight/{entity_name}/{criteria_name}?token=TOKEN \
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

    POST /score/weight
    
**Exemplo de requisição**

```
curl http://localhost:5000//score/weight?token=TOKEN \
-X POST
-d '{
    "entity_name": "livros",
    "criteria_name": "titles",
    "weight": 100
}
```

**Códigos de retorno**

| Código | Descrição |
|---|---|
| 200 | Salvo com sucesso |
| 400 | Requisição inválida |
| 401 | Não autorizado |