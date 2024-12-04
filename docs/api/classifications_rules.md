# Regras de reclassificação de produtos

[Documentação](https://magazine.atlassian.net/wiki/spaces/CAT/pages/3947856098/Plano+90+dias+-+mar+o+24+Corrigir+categoriza+o+errada+de+produtos+exibidos+na+ordena+o+de+menor+pre+o+da+Busca)

## Listando as regras
**Exemplo de requisição**

```bash
curl http://localhost:8000/classifications_rules -H "Authorization: TOKEN"
```

**Códigos de retorno**

| Código | Descrição |
|---|---|
| 200 | Sucesso |

**Exemplo de resposta**
```json
{
  "data": [
    {
      "operation": "MENOR_IGUAL",
      "product_type": "Refrigerador",
      "active": true,
      "created_at": "2024-02-29T19:09:10.741000",
      "price": 400,
      "status": "created",
      "to": {
        "product_type": "Peças para Refrigerador",
        "category_id": "ED",
        "subcategory_ids": [
          "FAPG",
          "REFR",
          "ACRF"
        ]
      },
      "user": "catalogo@luizalabs.com",
      "id": "271b9dea-394b-48ed-a24b-853a7200227b"
    }
  ]
}
```

## Criando uma regra
**Exemplo de requisição**

```bash
curl -X POST "http://localhost:8000/classifications_rules" -H "accept: application/json" -H "Authorization: TOKEN" -H "Content-Type: application/json" -d "{ \"product_type\": \"Refrigerador\", \"operation\": \"MENOR_IGUAL\", \"price\": 400.00, \"to\": { \"product_type\": \"Peças para Refrigerador\", \"category_id\": \"ED\", \"subcategory_ids\": [ \"FAPG\", \"REFR\", \"ACRF\" ] }, \"user\": \"catalogo@luizalabs.com\"}"
```


## Deletando uma regra
**Exemplo de requisição**

```bash
curl -X POST http://localhost:8000/classifications_rules/{id} -H "Authorization: TOKEN"
```
