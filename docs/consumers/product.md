# Produto

Payload necessário para manipulação de produtos.

## Estrutura da mensagem

| Campo | Descrição | Tipo | Obrigatório |
|----------|-----------|----------|----------|
| ean | Código ean do produto | integer | Sim |
| seller\_id | ID do vendedor | string | Sim |
| seller\_description | Descrição do vendedor | string | Sim |
| sku | Código sku do produto | string | Sim |
| parent\_sku | Código sku do produto pai | string | Não |
| type | Tipo do produto (`product`, `bundle` ou `gift`) | string | Sim |
| main\_variation | Indica se esta é a variação principal (caso seja a única, o valor esperado é `true`) | boolean | Sim |
| title | Título do produto | string | Sim |
| description | Descrição do produto | string | Sim |
| reference | Referência do produto | string | Sim |
| brand | Marca do produto | string | Sim |
| sold\_count | Quantidade de produtos vendidos | integer | Sim |
| review\_count | Quantidade de reviews | integer | Não |
| review\_score | Média das avaliações (as notas possíveis vão de `1.0` a `5.0` com uma casa decimal) | decimal | Não |
| categories | Lista de categorias | list | Sim |
| categories[\*].id | ID da categoria | string | Sim |
| categories[\*].description | Descrição da categoria | string | Sim |
| categories[\*].subcategories | Lista de subcategorias | list | Sim |
| categories[\*].subcategories[\*].id | ID da subcategoria | string | Sim |
| categories[\*].subcategories[\*].description | Descrição da subcategoria | string | Sim |
| dimensions | Dimensões do produto | object | Sim |
| dimensions.width | Largura do produto | decimal | Sim |
| dimensions.depth | Profundidade do produto | decimal | Sim |
| dimensions.weight | Peso do produto | decimal | Sim |
| dimensions.height | Altura do produto | decimal | Sim |
| attributes | Lista de variações do produto | list | Não |
| attributes[\*].type | Tipo da variação | string | Não |
| attributes[\*].value | Valor da variação | string | Não |
| release\_date | Data de lançamento | string (ISO 8601) | Não |
| updated\_at | Data da última atualização | string (ISO 8601) | Não |
| created\_at | Data de criação | string (ISO 8601) | Sim |
| sells\_to\_company | Informa se o produto pode ser vendido para empresas | boolean | Não |
| main\_category.id | ID da categoria principal | string | Não |
| main\_category.subcategory.id | ID da subcategoria principal | string | Não |

### Lista de variações

No campo `attributes[*].type` as seguintes opções serão aceitas:

| Tipo | Exemplo de valores |
|------|-----------|
| size | P, PP, M, ÚNICO, 12, 13, 15/16, 30cm, A2 |
| volume | 100 ml, 200 ml, 300 ml |
| weight | 10g, 20g, 30g, 1,5Kg, 3Kg |
| flavor | Abacaxi, Açai, Banana, Chocolate, Cookies, Napolitano |
| capacity | 1 GB, 2 GB, 5 GB, 10 GB, 100 GB, 1 TB, 5 TB |
| quantity | 1, 2, 3, 4, 5, 10, 20, 30, 50, 80, 90, 100 |
| inch | 1", 2", 10", 15,4", 21,5", 40", 43", 50" |
| console | Xbox One, Xbox 360, PSP, PS3, Wii, PC, 3DS |
| capsule | 14, 40, 60, 100, 120, 150, 200, 220, 240, 330 |
| piece | 1, 2, 3, 5, 10, 20, 30, 50, 100, 200, 500 |
| operator | Sem operadora, Vivo, Claro, Tim, Oi |
| additional | dual drive 2GB, cartão 2GB, pen drive 2GB, sem cartão |
| color | Branco, Azul, Amarelo, Vermelho, Cinza |
| side | Esquerdo, Direito |
| voltage | Bivolt, 110 Volts, 220 Volts, Pilha, Energia Solar, 12 Volts |

* O tipo da variação deve estar exatamente igual as opções acima
* Os valores da variações são apenas alguns exemplos, outros valores podem ser usados

## Exemplo

```json
{
    "ean": "841667100531",
    "seller_id": "magazineluiza",
    "seller_description": "Magazine Luiza",
    "sku": "216501900",
    "parent_sku": "216500000",
    "type": "product",
    "main_variation": true,
    "title": "Kindle Paperwhite Wi-Fi 4GB Tela 6",
    "description": "Especialmente feito para os amantes da leitura",
    "reference": "Amazon",
    "brand": "amazon",
    "sold_count": 35,
    "review_count": 12,
    "review_score": 4.5,
    "categories": [
        {
            "id": "TB",
            "description": "Tablets",
            "subcategories": [
                {
                    "id": "KIND",
                    "description": "Leitores de Livros Digitais"
                }
            ]
        }
    ],
    "dimensions": {
        "width": 0.18,
        "depth": 0.13,
        "weight": 0.47,
        "height": 0.44
    },
    "attributes": [
        {
            "type": "color",
            "value": "Azul"
        },
        {
            "type": "voltage",
            "value": "Bivolt"
        }
    ],
    "release_date": "2016-04-22T14:50:44.925065-03:00",
    "updated_at": "2016-07-05T13:40:44.925065-03:00",
    "created_at": "2016-04-12T22:20:44.925065-03:00"
}
```
