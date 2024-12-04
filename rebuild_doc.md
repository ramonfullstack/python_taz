## Rebuild

O Taz possui um sistema de rebuild que permite reprocessar informações de acordo com seu escopo, ação e parâmetros adicionais. Para iniciar o rebuild, basta inserir uma mensagem (com o padrão abaixo) na fila [Pub/Sub](https://cloud.google.com/pubsub/docs/overview?hl=pt-br) ou [SQS](https://docs.aws.amazon.com/pt_br/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html) de rebuild.

### Estrutura da mensagem

| Campo | Descrição | Tipo | Obrigatório |
|----------|-----------|----------|----------|
| scope | Escopo a ser reprocessado | string | Sim |
| action | Ação (`create`, `update` ou `delete`) | string | Sim |
| data | Parâmetros adicionais de acordo com o escopo utilizado | json | Não |

Para atender os diferentes tipos de reprocessamento de informações, são criadas diversas rotas para rebuilds específicos, cada uma atendendo a um escopo e ação específicos. Estes endpoints podem seguir basicamente dois fluxos:

**1 -** Após a chamada do endpoint de rebuild uma função Handler é ativada e envia uma mensagem para um tópico específico do Pub/Sub. Em seguida, um Pod (Consumer) é acionado para receber essa mensagem do tópico, e processá-la conforme o escopo especificado.

**2 -** No segundo fluxo, o endpoint envia a solicitação diretamente para um tópico do Pub/Sub sem a intervenção de um Pod intermediário.

# TODO
FILA -> TÓPICO
LINK PARA O TÓPICO
EXISTE SKIP ?

### Rotas

/rebuild/notification
/rebuild/catalog/notification
/rebuild/products
/rebuild/marvin/seller
/rebuild/medias
/rebuild/score
/rebuild/score/products
/rebuild/metabooks/{ean}
/rebuild/matching/omnilogic
/rebuild/product/exporter
/rebuild/matching/product
/rebuild/datalake

---

**`/rebuild/notification`**

**POST:** A classe **RebuildCatalogNotification** é responsável pela repostagem de todos os produtos do catálogo de um seller. O payload inclui apenas o ID do seller.

**Escopo:** catalog_notification

**Tópico:** [catalog-notification](https://console.cloud.google.com/cloudpubsub/topic/detail/catalog-notification?project=magalu-digital-project)

**Aplicação responsável:** 

[Payload](https://taz-api.magazineluiza.com.br/docs#/rebuild/RebuildHandler)

---

**`/rebuild/catalog/notification`**

**POST:** A classe **RebuildCatalogNotificationHandler** valida e formata as informações recebidas e envia uma mensagem de rebuild para o Pub/Sub ou SNS (dependendo do tipo enviado no payload) para cada item enviado na lista do payload. Este processo de rebuild realiza o reprocessamento do catálogo de produtos com base nos SKUs e IDs dos sellers fornecidos na lista do payload.

**Tópico:** [marvin-gateway](https://console.cloud.google.com/cloudpubsub/topic/detail/marvin-gateway?project=magalu-digital-project)

**Aplicação responsável:** 

[Payload](https://taz-api.magazineluiza.com.br/docs#/rebuild/RebuildCatalogNotificationHandler)

---

**`/rebuild/products`**

**POST:** A classe **RebuildCompleteProductBySku** faz a repostagem dos produtos do catálogo de um seller com base no ID do seller e o SKU, enviados no Payload.

**Escopo:** complete_products_by_sku

**Tópico:** [taz-complete-product](https://console.cloud.google.com/cloudpubsub/topic/detail/taz-complete-product?project=magalu-digital-project)

**Aplicação responsável:** 

[Payload](https://taz-api.magazineluiza.com.br/docs#/rebuild/RebuildProductHandler)

---

**`/rebuild/marvin/seller`**

**POST:** A classe **RebuildMarvinSeller** é responsável pelo reprocessamento dos produtos de um seller no contexto do Marvin. Durante o processo a lista de produtos é construída utilizando paginação e envia uma mensagem para a fila do Marvin para cada produto da lista.

**Escopo:** marvin_seller

**Tópico:** [taz-rebuild](https://console.cloud.google.com/cloudpubsub/topic/detail/taz-rebuild?project=magalu-digital-project)

**Aplicação responsável:** Arcoiro

[Payload](https://taz-api.magazineluiza.com.br/docs#/rebuild/RebuildMarvinSellerHandler)

---

**`/rebuild/medias`**

**POST:** A classe **MediaRebuild** é responsável pelo reprocessamento das mídias relacionadas a um produto de um seller. 

**Escopo:** media_rebuild

**Tópico:** [taz-media](https://console.cloud.google.com/cloudpubsub/topic/detail/taz-media?project=magalu-digital-project)

**Aplicação responsável:**

[Payload](https://taz-api.magazineluiza.com.br/docs#/rebuild/RebuildMediaHandler)

---

**`/rebuild/score`**

**POST:** A classe **RebuildProductScoreBySeller** é responsável pelo reprocessamento do score do catálogo de produtos de um seller, filtrando pelo ID do seller no Payload.

**Escopo:** product_score_by_seller

**Tópico:** [taz-score](https://console.cloud.google.com/cloudpubsub/topic/detail/taz-score?project=magalu-digital-project)

**Aplicação responsável:**

[Payload](https://taz-api.magazineluiza.com.br/docs#/rebuild/RebuildProductScoreHandler)

---

**`/rebuild/score/products`**

**POST:** A classe **RebuildProductScoreBySku** é responsável pelo reprocessamento do score de uma lista de produtos do catálogo de um seller, filtrando por SKU e ID do seller no Payload.

**Escopo:** product_score_by_sku

**Tópico:** [taz-score](https://console.cloud.google.com/cloudpubsub/topic/detail/taz-score?project=magalu-digital-project)

**Aplicação responsável:**

[Payload](https://taz-api.magazineluiza.com.br/docs#/rebuild/RebuildProductScoreBySkuHandler)

---

**`/rebuild/metabooks/{ean}`**

**GET:** A classe **RebuildMetabooksHandler** é responsável pelo reprocessamento dos metabooks de um determinado EAN. A classe não tem um escopo e inicia o reprocessamento diretamente no Pub/Sub.

**Tópico:** [taz-metadata-input](https://console.cloud.google.com/cloudpubsub/topic/detail/taz-metadata-input?project=magalu-digital-project)

**Aplicação responsável:**

[Payload](https://taz-api.magazineluiza.com.br/docs#/rebuild/RebuildMetabooksHandler)

---

**`/rebuild/matching/omnilogic`**

**POST:** A classe **RebuildMatchingOmnilogic** é responsável por reprocessar os produtos enriquecidos pela Omnilogic, filtrando por um determinado entity.

**Escopo:** matching_omnilogic

**Tópico:** [taz-rebuild](https://console.cloud.google.com/cloudpubsub/topic/detail/taz-rebuild?project=magalu-digital-project)

**Aplicação responsável:**

Não existente!<<<<>>>>
[Payload](https://taz-api.magazineluiza.com.br/docs#/rebuild/RebuildProductScoreBySkuHandler)

---

**`/rebuild/product/exporter`**

**POST:** A classe **RebuildProductExporterHandler** envia uma mensagem para uma fila SQS e aciona o consumer **ProductExporterConsumer**.

**Fila (SQS):** taz-product-exporter

**Aplicação responsável:**

[Payload](https://taz-api.magazineluiza.com.br/docs#/rebuild/RebuildProductExporterHandler)

---

**`/rebuild/matching/product`**

**POST:** A classe **RebuildMatchingProduct** busca um produto por SKU e ID do seller e faz uso da class **NotificationEnrichment** para enriquecer informações do produto.

**Escopo:** matching_by_sku

**Tópico:** [taz-metadata-product](https://console.cloud.google.com/cloudpubsub/topic/detail/taz-metadata-product?project=magalu-digital-project)

**Aplicação responsável:**

[Payload](https://taz-api.magazineluiza.com.br/docs#/rebuild/RebuildMatchingProductHandler)

---

**`/rebuild/datalake`**

**POST:** A classe **RebuildDatalakeHandler** envia mensagens para o consumer **DataLakeProcessor** que faz o processamento de diferentes fontes de dados como Niagara e Tetrix, e ao final do processamento de cada mensagem faz o envio para o DataLake.

**Tópico:** [taz-datalake](https://console.cloud.google.com/cloudpubsub/topic/detail/taz-datalake?project=magalu-digital-project)

**Aplicação responsável:**

[Payload](https://taz-api.magazineluiza.com.br/docs#/rebuild/RebuildMatchingProductHandler)

### Outros tipos de Rebuild

**`/seller`**

**POST:** O endpoint /seller também ativa um rebuild para cada requisição. Ao receber uma requisição, a classe **SellerHandler** verifica se existe um seller com determinado ID e, caso exista, ativa a função de rebuild **RebuildMarvinSellerIpdv** que é responsável pelo reprocessamento dos dados do seller com os dados de `platform` ou `integration_info` iguais a 'IPDV'.

**Escopo:** marvin_seller_ipdv

## Notification

**`/notification/{source}`**

**POST:** A classe NotificationHandler envia as mensagens para uma fila SQS acionando o Consumer **CatalogNotificationProcessor**.

---

**`/metadatainput/notification/`**

**POST:** MetadataInputRecordProcessor

**Tópico:** taz-metadata-input