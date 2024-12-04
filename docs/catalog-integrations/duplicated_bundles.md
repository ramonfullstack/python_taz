# Bundles aparecendo duplicados

Thread: https://luizalabs.slack.com/archives/C1Y0WBTH8/p1533667835000269

## Problema
Acme estava devolvendo bundles repetidos em um payload:
```js
        "products": [
            {
                "type": "bundle",
                "variations": [
                    {
                        "is_delivery_available": true,
                        "title": "Cozinha Compacta Itatiaia Rose 7 Portas Aço e",
                        "id": "229021100",
                      "bundles": [
                            {
                                "seller_sku": "073827801",
                                "seller_id": "magazineluiza",
                                "seller_description": "Magazine Luiza",
                                "price": "499.90",
                                "list_price": "499.90",
                                "quantity": 1,
                                "title": "Cozinha Compacta Itatiaia Rose",
                                "brand": "itatiaia",
                                "reference": "7 Portas Aço",
                                "stock_count": 1,
                                "media": {
                                    "videos": [
                                        "http://www.youtube.com/v/wOiTHse3iIw?hl=pt&"
                                    ],
                                    "images": [
                                        "https://a-static.mlcdn.com.br/{w}x{h}/cozinha-compacta-itatiaia-rose-7-portas-aco/magazineluiza/073827801/f6514f7d892192f8762d0a41be6faa7d.jpg",
                                        "https://a-static.mlcdn.com.br/{w}x{h}/cozinha-compacta-itatiaia-rose-7-portas-aco/magazineluiza/073827801/ae579ae7f2013cecb928d0a1d18c5e69.jpg",
                                        "https://a-static.mlcdn.com.br/{w}x{h}/cozinha-compacta-itatiaia-rose-7-portas-aco/magazineluiza/073827801/e109b735cd120dd4c4888271bea430c8.jpg",
                                        "https://a-static.mlcdn.com.br/{w}x{h}/cozinha-compacta-itatiaia-rose-7-portas-aco/magazineluiza/073827801/641b71ef5c830d71a97ce4e028e449f8.jpg",
                                        "https://a-static.mlcdn.com.br/{w}x{h}/cozinha-compacta-itatiaia-rose-7-portas-aco/magazineluiza/073827801/f92582cb9ff351c8a28667d47f9e7534.jpg",
                                        "https://a-static.mlcdn.com.br/{w}x{h}/cozinha-compacta-itatiaia-rose-7-portas-aco/magazineluiza/073827801/9aadb10c5eb3800b577c258b9f8a9143.jpg",
                                        "https://a-static.mlcdn.com.br/{w}x{h}/cozinha-compacta-itatiaia-rose-7-portas-aco/magazineluiza/073827801/4dd5d0a5ed411f56bd1a34d62e0a2e24.jpg",
                                        "https://a-static.mlcdn.com.br/{w}x{h}/cozinha-compacta-itatiaia-rose-7-portas-aco/magazineluiza/073827801/46791db624b8c7f8888396bf11d91ad3.jpg",
                                        "https://a-static.mlcdn.com.br/{w}x{h}/cozinha-compacta-itatiaia-rose-7-portas-aco/magazineluiza/073827801/f9ef6de5e924e1330e0f2de9ece079f8.jpg",
                                        "https://a-static.mlcdn.com.br/{w}x{h}/cozinha-compacta-itatiaia-rose-7-portas-aco/magazineluiza/073827801/a8ea4e9eaf8d538e81e1b8447730a668.jpg"
                                    ],
                                    "podcasts": [],
                                    "audios": []
                                },
                                "factsheet": {}
                            },
                            {
                                "seller_sku": "073827801",
                                "seller_id": "magazineluiza",
                                "seller_description": "Magazine Luiza",
                                "price": "499.90",
                                "list_price": "499.90",
                                "quantity": 1,
                                "title": "Cozinha Compacta Itatiaia Rose",
                                "brand": "itatiaia",
                                "reference": "7 Portas Aço",
                                "stock_count": 1,
                                "media": {
                                    "videos": [
                                        "http://www.youtube.com/v/wOiTHse3iIw?hl=pt&"
                                    ],
                                    "images": [
                                        "https://a-static.mlcdn.com.br/{w}x{h}/cozinha-compacta-itatiaia-rose-7-portas-aco/magazineluiza/073827801/f6514f7d892192f8762d0a41be6faa7d.jpg",
                                        "https://a-static.mlcdn.com.br/{w}x{h}/cozinha-compacta-itatiaia-rose-7-portas-aco/magazineluiza/073827801/ae579ae7f2013cecb928d0a1d18c5e69.jpg",
                                        "https://a-static.mlcdn.com.br/{w}x{h}/cozinha-compacta-itatiaia-rose-7-portas-aco/magazineluiza/073827801/e109b735cd120dd4c4888271bea430c8.jpg",
                                        "https://a-static.mlcdn.com.br/{w}x{h}/cozinha-compacta-itatiaia-rose-7-portas-aco/magazineluiza/073827801/641b71ef5c830d71a97ce4e028e449f8.jpg",
                                        "https://a-static.mlcdn.com.br/{w}x{h}/cozinha-compacta-itatiaia-rose-7-portas-aco/magazineluiza/073827801/f92582cb9ff351c8a28667d47f9e7534.jpg",
                                        "https://a-static.mlcdn.com.br/{w}x{h}/cozinha-compacta-itatiaia-rose-7-portas-aco/magazineluiza/073827801/9aadb10c5eb3800b577c258b9f8a9143.jpg",
                                        "https://a-static.mlcdn.com.br/{w}x{h}/cozinha-compacta-itatiaia-rose-7-portas-aco/magazineluiza/073827801/4dd5d0a5ed411f56bd1a34d62e0a2e24.jpg",
                                        "https://a-static.mlcdn.com.br/{w}x{h}/cozinha-compacta-itatiaia-rose-7-portas-aco/magazineluiza/073827801/46791db624b8c7f8888396bf11d91ad3.jpg",
                                        "https://a-static.mlcdn.com.br/{w}x{h}/cozinha-compacta-itatiaia-rose-7-portas-aco/magazineluiza/073827801/f9ef6de5e924e1330e0f2de9ece079f8.jpg",
                                        "https://a-static.mlcdn.com.br/{w}x{h}/cozinha-compacta-itatiaia-rose-7-portas-aco/magazineluiza/073827801/a8ea4e9eaf8d538e81e1b8447730a668.jpg"
                                    ],
                                    "podcasts": [],
                                    "audios": []
                                },
                                "factsheet": {}
                            },
```


## Passos para identificação/depuração do problema

1. Dump do mongo de produção;
2. Import do dump de produção no mongo local para simulação do problema; (`mongorestore -d acme acme`)
3. Identificou-se que o produto estava duplicado na base. Quando é montado o payload de `bundle`, é realizada; uma busca no mongo pelo `id`, e com isso o produto com sku `073827801` estava retornando duas vezes.

## Solução

Remover os produtos que estão duplicados via mongo. Desta forma, os bundles deixarão de ser repetidos  não aparecerão repetidos.