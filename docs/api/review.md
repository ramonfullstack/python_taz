## Review

### Enviar review de produto

Enviar código do produto para que seja obtida informações do review e enviado para fila de processamento.

    PUT /review
    
**Parâmetros**

| Campo | Descrição | Tipo |
|---|---|---|
| product_id | código do produto | string |

**Exemplo de requisição**

```
curl http://localhost:5000/review?token=TOKEN \
-X PUT
-d '{"product_id": "123456789"}'
```
**Exemplo de resposta para erro**

```
{
    "error_message": "Invalid request",
    "error_detail": "Missing product_id field",
    "error_reason": "bad request"
}
```

**Códigos de retorno**

| Código | Descrição |
|---|---|
| 201 | Sucesso |
| 400 | Requisição inválida |
| 401 | Não autorizado |
