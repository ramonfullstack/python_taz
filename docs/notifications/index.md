# Notificações

Você pode receber notificações de `create`, `update` e `delete` de produtos e preços através de um tópico SNS, basta fazer a subscription. Para fazer o subscription, procurar a `squad-ops` que pode ajudar com isso, basta informar o tópico `catalog-notification`.

As notificações podem ser enviadas para HTTP/HTTPS, SQS ou Lambda.

Maiores informações sobre utilização do SNS, [clique aqui](https://aws.amazon.com/pt/sns/)

## Estrutura da mensagem

| Campo | Descrição | Tipo |
|----------|----------|----------|
| id | ID de navageação | string |
| sku | SKU do produto | string |
| seller_id | ID do seller | string |
| action | Ação do produto (`create`, `update` e `delete`) | string |
| type | Tipo da notificação (`price`, `product`) | string |

## Exemplo

```json
{
    "id": "123456789",
    "sku": "1234",
    "seller_id": "magazineluiza",
    "action": "update",
    "type": "product"
}
```
