# Categoria

Payload necessário para manipulação de categorias.

## Estrutura da mensagem

| Campo | Descrição | Tipo |
|----------|----------|----------|
| id | ID da categoria | string |
| description | Descrição da categoria | string |
| slug | Slug | string |
| parent_id | ID da categoria pai | string |
| active | Status da categoria | bool |

## Exemplo

```json
{
    "id": "MO",
    "description": "Móveis e Decoração",
    "slug": "moveis-decoracao",
    "parent_id": "ML",
    "active": true
}
```
