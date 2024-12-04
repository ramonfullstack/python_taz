# Mídia

Payload necessário para manipulação de mídias.

## Estrutura da mensagem

| Campo | Descrição | Tipo |
|----------|-----------|---------|
| seller_id | ID do vendedor | string |
| sku | Código sku do produto | string |
| videos | Lista de vídeos | list (string) |
| audios | Lista de áudios | list (string) |
| podcasts | Lista de podcasts | list (string) |
| images | Lista de imagens | list |
| images[*].url | URL da imagem | string |
| images[*].hash | Hash da imagem | string |

## Exemplo

```json
{ 
    "seller_id": "magazineluiza",
    "sku": "219832400",
    "videos": [
        "http://www.youtube.com/v/5NGQMzmslRE"
    ],
    "audios": [
        "http://s.mlcdn.com.br/audio/219/832/400/219832400.mp3"
    ],
    "podcasts": [
        "http://i.mlcdn.com.br/podcast/219832400.mp3"
    ],
    "images": [
        {
            "url": "http://i.mlcdn.com.br/1500x1500/x-219832400.jpg",
            "hash": "1091bf7739ed40fe8e23ac2a09aed49f"
        },
        {
            "url": "http://i.mlcdn.com.br/1500x1500/x-219832400-A.jpg",
            "hash": "49376583712046a6890096a5778fd10d"
        }
    ]
}
```
