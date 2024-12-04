## Trava de Preço


Insere trava de preço por seller

    POST /price_lock

**Parâmetros**

| Campo | Descrição | Tipo |
|---|---|---|
| seller_id | Id do seller | string |
| percent | Porcentagem da diferença para trava de preço | float |


**Exemplo de requisição**

```
curl http://localhost:5000/price_lock?token=TOKEN \
-X POST
-d '{"seller_id": "magazineluiza", "percent": 25.0}'
```

**Códigos de retorno**

| Código | Descrição |
|---|---|
| 200 | Sucesso |
| 400 | Requisição inválida |
| 401 | Não autorizado |

Retorna uma lista de travas de preço

**Exemplo de requisição**

```
curl http://localhost:5000/price_lock?token=TOKEN \
-X GET
```

**Códigos de retorno**

| Código | Descrição |
|---|---|
| 200 | Sucesso |
| 400 | Requisição inválida |
| 401 | Não autorizado |

**Exemplo de resposta**
```json
{
        "data": [{
                "seller_id": "a",
                "percent": 30.5,
        }]
}
```

Retorna trava de preço por seller

**Exemplo de requisição**

```
curl http://localhost:5000/price_lock/seller/a?token=TOKEN \
-X GET
```

**Códigos de retorno**

| Código | Descrição |
|---|---|
| 200 | Sucesso |
| 400 | Requisição inválida |
| 404 | Trava de preço não encontrada para o seller |
| 401 | Não autorizado |

**Exemplo de resposta**
```json
{
        "data": {
                "seller_id": "a",
                "percent": 30.5
        }
}
```
