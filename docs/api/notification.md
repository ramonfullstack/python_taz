## Notificação

### Receber notificação de produtos

Enviar notificações por `source`, adicionando em um fila, para ser consumidor por um consumer e assim adicionarmos as informações no flow de catálogo.

    POST /notification/{source}
    
**Parâmetros**

| Campo | Descrição | Tipo |
|---|---|---|
| source | nome do source que está enviando a notificação | string |

**Exemplo de requisição**

```
curl http://localhost:5000/notification/magalu?token=TOKEN \
-X POST
-d '{"product_id": "123456789"}'
```

**Códigos de retorno**

| Código | Descrição |
|---|---|
| 201 | Sucesso |
| 401 | Não autorizado |
