## Lista de Entidades

**Exemplo de requisição**

```
curl -X GET http://localhost:5000/entity/list?token=TOKEN
```


**Códigos de retorno**

| Código | Descrição |
|---|---|
| 200 | Sucesso |
| 401 | Não autorizado |

**Exemplo de resposta**
```json
{
  "data": ["Celular", "Fritadeira Elétrica"]
    
}
```
