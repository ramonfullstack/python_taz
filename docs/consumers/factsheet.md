# Ficha Técnica

Payload necessário para manipulação de ficha técnica.

## Estrutura da mensagem

| Campo | Descrição | Tipo |
|----------|-----------|----------|
| sku | Código sku do produto | string |
| seller_id | ID do vendedor | string |
| items | Lista de itens | list |
| items[\*].slug | Slug | string |
| items[\*].display_name | Nome do item  | string |
| items[\*].elements | Subitens | list |
| items[\*].elements[\*].key_name | Nome do subitem | string |
| items[\*].elements[\*].value | Valor do subitem | string |
| items[\*].elements[\*].is_html | Se o `value` contém HTML (opcional) | boolean |
| items[\*].elements[\*].elements | Itens do subitem | list |

## Exemplo

```json
{ 
    "sku": "216501100",
    "seller_id": "magazineluiza",
    "items": [
        {
            "slug": "apresentacao",
            "display_name": "Apresentação",
            "elements": [
                {
                    "key_name": "Apresentação do produto",
                    "elements": [
                        {
                            "value": "Procurando Nemo está de volta agora"
                        }
                    ]
                }
            ]
        },
        {
            "slug": "ficha-tecnica",
            "display_name": "Ficha-Técnica",
            "elements": [
                {
                    "key_name": "Informações técnicas",
                    "elements": [
                        {
                            "key_name": "Marca",
                            "value": "Sunny Brinquedos"
                        },
                        {
                            "key_name": "Cor",
                            "value": "Branco"
                        }
                    ]
                },
                {
                    "key_name": "Tipo de gás",
                    "elements": [
                        {
                            "value": "Natural"
                        },
                        {
                            "value": "GLP"
                        }
                    ]
                },


                {
                    "key_name": "Desenvolvimento",
                    "elements": [
                        {
                            "key_name": "Desenvolvimento",
                            "value": "Capacidade visual"
                        },
                        {
                            "key_name": "Desenvolvimento",
                            "value": "Percepção cromática"
                        },
                        {
                            "key_name": "Desenvolvimento",
                            "value": "<h2>Diversão</h2><p>criança</p>",
                            "is_html": true
                        }
                    ]
                }
            ]
        }
    ]
}
```
