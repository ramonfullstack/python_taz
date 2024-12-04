# Changelog

## [2.485.3](https://gitlab.luizalabs.com/luizalabs/taz/compare/v2.485.2...v2.485.3) (2024-06-27)


### Bug Fixes

* send custom attributes to pubsub ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/3e021cb))

## [2.485.2](https://gitlab.luizalabs.com/luizalabs/taz/compare/v2.485.1...v2.485.2) (2024-06-25)


### Bug Fixes

* skip message on non-existent product consumer-update-category ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/92bb3f3))

## [2.485.1](https://gitlab.luizalabs.com/luizalabs/taz/compare/v2.485.0...v2.485.1) (2024-06-25)


### Bug Fixes

* fixed generate verified images on taz-consumer-media ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/2eefe23))

# [2.485.0](https://gitlab.luizalabs.com/luizalabs/taz/compare/v2.484.0...v2.485.0) (2024-06-25)


### Features

* Adjust endpoint products ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/e18589d))

# [2.484.0](https://gitlab.luizalabs.com/luizalabs/taz/compare/v2.483.0...v2.484.0) (2024-06-25)


### Features

* **media:** Skip media processing on input by its hash ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/9b8f461))

# [2.483.0](https://gitlab.luizalabs.com/luizalabs/taz/compare/v2.482.1...v2.483.0) (2024-06-24)


### Features

* add currency to product_writer and datalake consumer ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/8c37b17))


### Improvements

* fix requirements error ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/df371c4))

## [2.482.1](https://gitlab.luizalabs.com/luizalabs/taz/compare/v2.482.0...v2.482.1) (2024-06-17)


### Bug Fixes

* logs being exported as errors to gcp ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/7238327))

# [2.482.0](https://gitlab.luizalabs.com/luizalabs/taz/compare/v2.481.2...v2.482.0) (2024-06-17)


### Features

* update consumer product count_update ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/058d289))

# 1.0.0 (2024-06-05)


### Bug Fixes

* add schema validation to RebuildProductExporterHandler ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/a28702f))
* **notification:** validate identifier field ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/379e791))
* **poller_product:** convert active field to boolean ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/dec2871))
* **poller-product:** adjust env type ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/f2d65a6))
* **poller-product:** fix env type ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/9068160))
* **poller-product:** remove active and date filter ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/1f5ca17))
* addicionando teste ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/de5d045))
* adjust assembler slow correlations query ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/5bb0a53))
* adjust highest score slow query ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/93c4c7d))
* adjust json ordering method ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/5426ce2))
* adjust pubsub payload ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/8463ada))
* ajusta callback de despublicacao ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/bd4e448))
* change product poller bundle active field ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/fa7b256))
* change taz-poller-video to pubsub. ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/978d5a0))
* change the poller product query to not change bundles to product type ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/355211f))
* check blobs with letters order ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/382d603))
* check message datetime on nack ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/8fd2298))
* check message datetime on nack ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/f790b30))
* check pubsub sbuscription id environment ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/9b5c1f0))
* check pubsub sbuscription id environment ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/2065433))
* corrigi orientacao de imagens ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/133a120))
* dont process disabled products messages ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/9bb58e2))
* dont raise not found error ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/3007680))
* gchat notification crontab ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/2248291))
* get new mssql connection ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/d77fad8))
* get new redis connection ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/10de3f2))
* get variation field ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/7a3bde7))
* ignore inexistent identifiers ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/6894612))
* renew msql connection ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/2dba2ea))
* revert makefile ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/ec68152))
* update google pubsub lib to latest [BUG-2B2D] ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/6933066))
* **enriched_product:** log when a product does not exists ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/00823c3))
* **matching:** dont return a falsy value when product does not exists ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/940064e))
* **media:** ignore medias without content error ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/415e704))
* **metadata_verify:** accept null categories ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/e28d6aa))
* **product:** save raw_product bucket data if it does not exists ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/2ce42dd))
* **rebuild_marvin_sellers:** filter disabled on matching ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/6486b32))
* get variation field ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/845a151))
* increase image max pixels ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/72eae3f))
* raise error on generic error ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/05a633d))
* remove regex and user storage as parameter ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/282a55c))
* review topic name ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/2b9508c))
* rollback product poller query ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/40f1381))
* send metadata-input data to pubsub ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/862b90b))
* send to taz-complete-product pubsub ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/883219f))
* set default list on media itens ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/fc9cb8d))
* set ordering key on publisher ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/090c53e))
* set project id ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/adfbab2))
* sonar fix ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/8173771))
* sonar issue ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/d7de4d0))
* tratando retorno da omnilogic  de json invalido ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/6bcd64a))
* tratando retorno da omnilogic  de json invalido ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/c9b7383))
* tratando retorno da omnilogic  de json invalido ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/1a786d9))
* tratando retorno da omnilogic de json invalido ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/027194c))
* update google oauth lib ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/ae9a1fb))
* use default sub category if product does not has a subcategory ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/edb2478))
* use https on metabooks api ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/a2e1b53))
* use media images ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/101655c))
* validate router config only on scope catalog_notification ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/ed22733))


### Continuous Integration

* fixing deploy ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/79ced79))


### Features

* **notifications:** change datasheet validation from consumer to api ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/26a1ef1))
*  product poller circuit breaker ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/a5e38a5))
* add error trace on log ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/204f199))
* add process skip user reviews ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/0b0cf8d))
* add process skip user reviews ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/ae959b5))
* add process skip user reviews ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/022942a))
* add process skip user reviews ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/37f6eb4))
* add process skip user reviews ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/99a5d9c))
* add process skip user reviews ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/09dff7a))
* add process skip user reviews ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/0ebf031))
* add process skip user reviews ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/61505b9))
* add process skip user reviews ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/113aa35))
* add process skip user reviews ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/5663460))
* add process skip user reviews ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/51dff44))
* add process skip user reviews ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/8231eff))
* add process skip user reviews ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/10ee9b7))
* add process skip user reviews ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/2d4505b))
* add RebuildLockHandle to catalog_notification and rebuild_marvin_seller_paginator ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/b6d7040))
* adding thundera to consumers and pollers ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/29440b1))
* ajust test ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/ff5bcd0))
* ajuste de log ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/da987dc))
* ajuste de logica ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/f672496))
* ajuste de variavel ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/a1bcaa8))
* catalog notification router ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/548d83a))
* change complete product to pubsub ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/e16efe9))
* change ID_LENGTH to 9 ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/242fcb7))
* change marvin seller rebuild sctructure ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/4a8e250))
* change rebuild  to pubsub ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/f76e229))
* change rebuild to pubsub ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/0053648))
* change rebuild to pubsub ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/f1cbbc0))
* change rebuild to pubsub ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/afb1585))
* change rebuild to pubsub ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/505cacb))
* change rebuild to pubsub ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/991575c))
* change rebuild to pubsub ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/e191b3b))
* change rebuild to pubsub ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/216340b))
* change rebuild to pubsub ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/27340a7))
* change storage http poll size ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/5ea5a47))
* change taz consumer datalake to pubsub ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/588fcf4))
* change taz consumer metadata verify to pubsub ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/af7e106))
* change taz-consumer-product-writer to pubsub ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/e658dca))
* change taz-indexing-process  to pubsub ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/213ec7f))
* change taz-indexing-process  to pubsub ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/b44e27f))
* change taz-indexing-process  to pubsub ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/625b9fc))
* change taz-poller-base-price to pubsub [TST-C72E] ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/534e798))
* change taz-poller-factsheet to pubsub ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/cecf903))
* change taz-poller-product to pubsub ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/484acd2))
* change taz-product-exporter to pubsub ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/dcb9d46))
* change unpublish query to use or statement ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/708ece8))
* complete media rebuild ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/aa67695))
* flag inactive seller flow ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/b897840))
* flag inactive seller flow ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/c6be00a))
* flag inactive seller skus flow ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/41e95e9))
* flag inactive seller skus flow ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/3e7ba48))
* ignore messages without variations ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/7369c9f))
* **notification:** set custom attributes notification ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/6a5ee9d))
* change taz-notification to pubsub ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/7e205ff))
* **metadata-verify:** default category and subcategory ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/d634fbd))
* changing broker from sqs to pubsub taz-score ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/56a515e))
* delete category cache on delete, update and create ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/1c51c2e))
* dont send matching type messages to retry ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/720665f))
* ignore results with error ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/174c7b9))
* improve non existent correlations log ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/5cdaaba))
* insere categoria nos atributos ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/b9b63ee))
* keep mongodb connection open ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/bc11def))
* list media timeout ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/2020052))
* media bucket consumer ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/b669747))
* media rebuild ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/e9ec548))
* remove cron rebuild sellers ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/97f7d16))
* remove field images from required_fields ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/6655982))
* remove images from required fields ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/b33d9a2))
* removendo configuracao porta fixa mongodb ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/bb23d9d))
* removendo configuracao porta fixa mongodb ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/1d12478))
* send 1P products to kinesis ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/e977d4b))
* send handlers rebuild to pubsub ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/01c5765))
* send handlers rebuild to pubsub ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/7b389d3))
* set pubsub delay on catalog-notification ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/86f1aa2))
* stk174 envia o atributo event_type na msg do metadata-verify ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/6418b18))
* stk593 notificar skip patolino maas-product ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/3c25ece))
* taz mathing product queue to pubsub topic ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/fce2731))
* taz mathing product queue to pubsub topic ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/3947522))
* update category send messages to pubsub ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/f14b22c))
* update lib google-cloud-pubsub ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/065ebb7))
* update lib google-cloud-pubsub ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/6fd43fa))
* update scope db settings ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/4ec78bf))
* use layered cache to find categories ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/2cb0cff))
* video poller ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/fd99142))


### Improvements

* **cicd:** commit lint and create realease ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/1d2d1ba))
* add branch_id on stock log ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/de382fd))
* add changelog ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/f76bb66))
* add pubsub subscription id default as a empty string ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/bdf308d))
* adding check gmud ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/c7e73c0))
* adding count and rating log ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/6e7c2fa))
* adding poll(0) to kafka producer ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/48cff9d))
* adjust conflicts ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/5c1c9ae))
* adjust mr ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/6cd7262))
* ajuste de log ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/1e50f75))
* changelog ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/c00e347))
* check-gmud deploy ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/86fcd5e))
* debug flag message ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/98b7e2c))
* debug flag message ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/17e2237))
* getting sku using sku and seller_id ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/5d58322))
* improve debug logs ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/0a6f980))
* inserido log debug ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/ccddfba))
* lint ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/67de607))
* opentelemetry ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/a67a9b1))
* opentelemetry ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/12f62ac))
* otel config ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/7cc5a4e))
* production settings media rebuild stream name ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/fbdf3bf))
* release file ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/69c1352))
* release file ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/166e76d))
* remove cron report_products routine, tests and ci [TST-8E4B] ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/433bc3d))
* remove unnecessary debug level ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/e0adb1f))
* remove unnecessary debug level ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/dd9bcb4))
* removidos indices sem uso ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/d98f37a))
* set default media if it does not exists ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/11720af))
* show error on log ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/c7b5a36))
* subscription_name ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/2754b5f))
* use simple_settings typing ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/8a11d08))
* use simple_settings typing ([](https://gitlab.luizalabs.com/luizalabs/taz/commit/718dd66))

## [2.481.1]() 2024-06-04


### Bugfixes

- Fixed issues on sonar


## [2.481.0]() 2024-06-04


### Features

- Creation of mechanisms to download media directly from the bucket


## [2.480.0]() 2024-06-03


### Features

- Add schema validation to RebuildProductExporterHandler


## [2.479.0]() 2024-06-03


No significant changes.


## [2.478.4]() 2024-06-03


### Bugfixes

- - Fixed pipeline build to use dind 26


## [2.478.3]() 2024-05-31


### Features

- fix fortify issues


## [2.478.2]() 2024-05-29


### Features

- fix minimum order quantity product-writer validation


## [2.478.1]() 2024-05-28


### Bugfixes

- convert active field to boolean.


## [2.478.0]() 2024-05-28


### Features

- change datasheet validation from consumer to api.


## [2.477.0]() 2024-05-27


### Features

- add minimum_order_quantity field on product-writer
- add minimum_order_quantity field on simple-product scope
- change scope stock on consumer taz-datalake
- add endpoint delete to minimum order quantity
- add endpoint get to minimum order quantity
- add endpoint put to minimum order quantity


## [2.476.0]() 2024-05-27


### Features

- Identifier validation when enriching with datasheet.


## [2.475.9]() 2024-05-22


### Bugfixes

- adjust env type.
- ignore inexistent identifiers.


## [2.475.8]() 2024-05-22


### Features

- config tetrix for all scopes


## [2.475.7]() 2024-05-22


### Bugfixes

- adjust env type.


## [2.475.6]() 2024-05-21


### Bugfixes

- fix env type.


## [2.475.5]() 2024-05-21


### Bugfixes

- remove active and date filter.


## [2.475.4]() 2024-05-21


No significant changes.


## [2.475.3]() 2024-05-17


### Features

- Adding poll(0) to kafka producer


## [2.475.2]() 2024-05-16


### Bugfixes

- Remove empty dict from factsheet


## [2.475.1]() 2024-05-16


### Bugfixes

- change the poller product query to not change bundles to product type.


## [2.475.0]() 2024-05-16


### Bugfixes

- skip empty dict in factsheet


## [2.474.2]() 2024-05-13


### Bugfixes

- get new mssql connection.


## [2.474.1]() 2024-05-13


### Bugfixes

- get new redis connection.


## [2.474.0]() 2024-05-13


### Features

- product poller circuit breaker.


## [2.473.0]() 2024-05-06


### Features

- ignore messages without variations.

### Bugfixes

- adjust json ordering method.


## [2.472.2]() 2024-05-06


### Bugfixes

- update `google-cloud-pubsub` lib to latest version.


## [2.472.1]() 2024-05-06


### Deprecations and Removals

- remove cron report_products routine, tests and ci.


## [2.472.0]() 2024-05-02


### Features

- Add trace ID in messages to product-metadata topic

### Bugfixes

- Fixed query for scanning products by product type
  Added parameter for no_cursor_timeout on pagination key set
  Fixed environment variable for change time to wait on pollers
  Configured mongo version equal to production


## [2.471.0]() 2024-04-29


No significant changes.


## [2.470.0]() 2024-04-24


### Features

- Add tests to increase covarege.


## [2.469.1]() 2024-04-24


### Features

- fix datalake config tetrix


## [2.469.0]() 2024-04-23


No significant changes.


## [2.468.0]() 2024-04-23


### Features

- Send the source field in the rebuild datalake endpoint

### Bugfixes

- log when a product does not exists.


## [2.467.1]() 2024-04-19


### Deprecations and Removals

- remove matching_product scope from taz-consumer-datalake


## [2.467.0]() 2024-04-18


### Bugfixes

- filter disabled on matching on marvin_seller rebuild.


## [2.466.0]() 2024-04-17


### Features

- adding thundera to taz workers (consumers and pollers).


## [2.465.0]() 2024-04-17


No significant changes.


## [2.464.0]() 2024-04-17


### Features

- change taz-notification to pubsub.


## [2.463.3]() 2024-04-17


### Bugfixes

- ignore medias without content error.


## [2.463.2]() 2024-04-16


No significant changes.


## [2.463.1]() 2024-04-16


### Bugfixes

- return true on matching product.


## [2.463.0]() 2024-04-16


### Features

- adding PUT method to classification_rule endpoint
- change logs from price-rule and product-writer


## [2.462.0]() 2024-04-16


### Features

- set custom attributes notification.


## [2.461.2]() 2024-04-16


### Features

- default category and subcategory.


## [2.461.1]() 2024-04-15


### Features

- fix sonar


## [2.461.0]() 2024-04-15


### Features

- adding chester strategy on matching
- change matchers for chester and omnilogic in matching strategy
- change merger to set chester strategy when is necessary
- remove product hash reference from product-writer
- refactoring merger to set matching strategy process


## [2.460.10]() 2024-04-12


### Bugfixes

- save raw_products bucket data if it does not exists.


## [2.460.9]() 2024-04-10


### Features

- change taz-product-exporter to pubsub.


## [2.460.8]() 2024-04-10


### Bugfixes

- raise error on generic error.


## [2.460.7]() 2024-04-10


### Features

- change taz-poller-base-price to pubsub.


## [2.460.6]() 2024-04-09


### Bugfixes

- get variation field.


## [2.460.5]() 2024-04-09


### Bugfixes

- get variation field.


## [2.460.4]() 2024-04-09


### Bugfixes

- adjust highest score slow query.


## [2.460.3]() 2024-04-09


### Bugfixes

- adjust assembler slow correlations query.


## [2.460.2]() 2024-04-08


### Features

- Add enriched products DELETE endpoint in swagger


## [2.460.1]() 2024-04-08


### Deprecations and Removals

- remove flag of poller-price-campaign to switch to kinesis.


## [2.460.0]() 2024-04-05


### Features

- add RebuildLockHandle to catalog_notification and rebuild_marvin_seller_paginator


## [2.459.0]() 2024-04-05


### Bugfixes

- use https on metabooks api.


## [2.458.0]() 2024-04-05


### Features

- delete category cache on delete, update and create.


## [2.457.0]() 2024-04-05


### Features

- dont send matching type messages to retry.


## [2.456.0]() 2024-04-05


### Features

- Updating the default schema for sending enriched products to the data lake

### Bugfixes

- Fixed md5 calculation in the logical delete of enriched products


## [2.455.0]() 2024-04-04


### Features

- change taz-consumer-product-writer to pubsub.


## [2.454.1]() 2024-04-03


### Improved Documentation

- Added documentation of enriched products indexes

### Deprecations and Removals

- remove badge consumer/poller from pipeline.


## [2.454.0]() 2024-04-02


### Features

- send 1P products to kinesis.


## [2.453.1]() 2024-04-02


### Features

- change taz-poller-partner to pubsub.


## [2.453.0]() 2024-04-01


### Features

- use layered cache to find categories.


## [2.452.0]() 2024-03-28


### Bugfixes

- Adjustment of recursion to search for prohibited terms


## [2.451.0]() 2024-03-28


### Features

- fixed active field for all enriched products sources in taz-datalake
- add endpoint get enriched products with source
- add metadata field on product-features scope
- change endpoint delete enriched product
- Change the FactsheetMerger to use generic_content enrichment

### Deprecations and Removals

- Removed product review consumer and endpoint


## [2.450.0]() 2024-03-28


### Features

- adding new endpoint to rebuild price-rules scope


## [2.449.3]() 2024-03-27


### Features

- Adjust swagger taz for the notification endpoint.


## [2.449.2]() 2024-03-26


### Bugfixes

- change taz-poller-video to pubsub.


## [2.449.1]() 2024-03-25


### Bugfixes

- adjust sonar


## [2.449.0]() 2024-03-25


### Features

- create price-rule consumer
- saved to datalake when removing product from a price rule
- create price-rules cron
- change simple product scope to select entity from reclassification price rules when exists
- improve price_rules cron code for performance
- Added classifications rules endpoints
- Include reclassifier in product type export to product_features queue.


## [2.448.0]() 2024-03-25


### Features

- change marvin seller rebuild structure.


## [2.447.1]() 2024-03-25


No significant changes.


## [2.447.0]() 2024-03-22


### Features

- add videos, podcasts and audios on simple product

### Deprecations and Removals

- remove media stream env.


## [2.446.2]() 2024-03-19


No significant changes.


## [2.446.1]() 2024-03-18


No significant changes.


## [2.446.0]() 2024-03-18


No significant changes.


## [2.445.3]() 2024-03-18


### Features

- fix datasheet data in taz-datalake consumer


## [2.445.2]() 2024-03-14


No significant changes.


## [2.445.1]() 2024-03-14


### Bugfixes

- set ordering key on publisher.


## [2.445.0]() 2024-03-13


### Features

- change taz poller product to pubsub.


## [2.444.0]() 2024-03-11


### Deprecations and Removals

-


## [2.443.0]() 2024-03-11


### Bugfixes

- renew msql connection.


## [2.442.0]() 2024-03-08


### Bugfixes

- use default sub category if product does not has a subcategory.


## [2.441.0]() 2024-03-07


### Features

- change taz-match-product to pubsub.


## [2.440.0]() 2024-03-01


### Bugfixes

- check pubsub sbuscription id environment.


## [2.439.0]() 2024-02-29


### Features

- metadata-verify media producer to pubsub


## [2.438.0]() 2024-02-28


### Features

- change taz media consumer to pubsub


## [2.437.0]() 2024-02-28


### Features

- change rebuild to pubsub


## [2.436.0]() 2024-02-27


### Features

- update lib google-cloud-pubsub


## [2.435.0]() 2024-02-22


### Features

- update category send messages to pubsub.


## [2.434.1]() 2024-02-20


### Bugfixes

- send to taz-complete-product pubsub.


## [2.434.0]() 2024-02-20


### Features

- send handlers rebuild to pubsub.


## [2.433.5]() 2024-02-20


### Bugfixes

- send metadata-input data to pubsub.


## [2.433.4]() 2024-02-19


### Features

- changing broker from sqs to pubsub taz-score

### Bugfixes

- fix: dont raise not found error.


## [2.433.3]() 2024-02-19


### Bugfixes

- remove message nack.


## [2.433.2]() 2024-02-19


### Features

- change complete product to pubsub.
- set pubsub delay on catalog-notification.


## [2.433.1]() 2024-02-14


No significant changes.


## [2.433.0]() 2024-02-07


### Features

- change taz consumer metadata verify to pubsub


## [2.432.0]() 2024-02-07


### Features

- change taz-indexing-process to pubsub.


## [2.431.1]() 2024-02-06


### Features

- change taz consumer datalake to pubsub.


## [2.431.0]() 2024-02-05


### Bugfixes

- validate router config only on scope catalog_notification.

### Deprecations and Removals

- remove unused pollers media and media_active code


## [2.430.0]() 2024-02-05


No significant changes.


## [2.429.0]() 2024-02-05


### Features

- catalog notification router.


## [2.428.0]() 2024-02-01


### Features

- remove acme factsheet notification kinesis
  remove acme media notification kinesis


## [2.427.0]() 2024-01-31


### Features

- Add notification type metadata-verify on rebuild data lake


## [2.426.0]() 2024-01-31


### Features

- Change sending error notification when executing crontab to gchat


## [2.425.0]() 2024-01-30


### Bugfixes

- dont process disabled products messages.


## [2.424.4]() 2024-01-30


### Features

- improve non existent correlations log.


## [2.424.3]() 2024-01-29


### Features

- fix scope product and original-product in datalake consumer


## [2.424.2]() 2024-01-25


### Bugfixes

- poller product query rollback


## [2.424.1]() 2024-01-23


### Bugfixes

- change product poller bundle active field.


## [2.424.0]() 2024-01-19


### Features

- rebuild medias with bucket data


## [2.423.1]() 2024-01-19


### Features

- fix md5 validation in taz-factsheet-consumer


## [2.423.0]() 2024-01-18


### Features

- adding metadata-verify scope on taz-consumer-datalake
- changing the metadata-verify consumer to be responsible for execute the merge process
- remove merger process from enriched product consumer
- remove merger process from product consumer
- Allow the product to have enriched content on `taz-consumer-metadata-verify`


## [2.422.0]() 2024-01-17


### Features

- new taz media worker


## [2.421.0]() 2024-01-16


### Bugfixes

- update taz-poller-video config


## [2.420.0]() 2024-01-16


### Features

- new taz-poller-video


## [2.419.0]() 2024-01-15


### Features

- changing consumers price_3p and stock_3p to use CacheLock and remove MongoLock
- remove images from required fields and validate if media has least one required field.


## [2.418.0]() 2024-01-15


### Features

- thundera telemetry


## [2.417.0]() 2024-01-11


### Features

- payload processing with product type for product_feature scope
- add product_type field on raw_products collection
- change config product-exporter scopes
- change type datasheet to matching_product sns notification


## [2.416.0]() 2024-01-10


### Features

- add branch_id on stock log


## [2.415.0]() 2024-01-09


### Features

- remove field images from required fields.


## [2.414.0]() 2024-01-08


### Bugfixes

- use get blob by letters order instead of list blobs.
- unit test for category attribute


## [2.412.0]() 2023-12-14


### Features

- send categorie on attributes payload


## [2.411.0]() 2023-12-12


### Bugfixes

- add try/except to igonore medias when Listmedia throws a exception


## [2.410.0]() 2023-12-11


### Bugfixes

- add new http connection poll size


## [2.409.0]() 2023-12-11


### Bugfixes

- remove regex and use storage manager as parameter.


## [2.408.0]() 2023-12-11


### Features

- list media timeout config


## [2.407.0]() 2023-12-08


### Features

- remove listmedia api and create a class to listmedia.


## [2.406.0]() 2023-12-05


### Features

- change image resize algorithm.


## [2.405.0]() 2023-11-27


### Bugfixes

- add media fields on rebuild


## [2.404.0]() 2023-11-08


### Features

- create skip consumer user review


## [2.403.0]() 2023-11-08


No significant changes.


## [2.402.0]() 2023-10-26


No significant changes.


## [2.401.0]() 2023-10-26


No significant changes.


## [2.400.2]() 2023-10-26


### Features

- adding disable_on_matching filter on v1/products


## [2.400.1]() 2023-10-25


### Features

- new reprocessing scopes in catalog notifications


## [2.400.0]() 2023-10-23


### Features

- Remove sending rule for matching products without ean


## [2.399.0]() 2023-10-19


### Features

- changing endpoint unpublish api to publish events in pubsub and kafka
- create kafka connection
  changing taz-datalake to publish events in pubsub and kafka topic


## [2.398.0]() 2023-10-17


No significant changes.


## [2.397.0]() 2023-10-16


No significant changes.


## [2.396.0]() 2023-10-09


No significant changes.


## [2.395.0]() 2023-10-09


### Features

- Change algorithm of election product_id on matching and exporting on simple-product as offer_id


## [2.394.2]() 2023-10-02


### Features

- change checkout-price topic publish


## [2.394.1]() 2023-09-28


### Features

- change pubsub topic and data in marvin-seller scope


## [2.394.0]() 2023-09-28


No significant changes.


## [2.393.0]() 2023-09-25


### Bugfixes

- insert debug log


## [2.392.1]() 2023-09-20


### Bugfixes

- Fixed removing isbn when removing ean


## [2.392.0]() 2023-09-18


### Features

- Upload original factsheet on bucket raw-factsheet


## [2.391.2]() 2023-09-18


### Features

- Adjustment of enrichment removal flow via Metabooks


## [2.391.1]() 2023-08-31


### Bugfixes

- Fix for incorrect sku message on consumer label


## [2.391.0]() 2023-08-28


### Features

- Remove obligation to inform seller_description in taz-consumer-product


## [2.390.0]() 2023-08-24


No significant changes.


## [2.389.0]() 2023-08-23


No significant changes.


## [2.388.0]() 2023-08-21


### Features

- changing EAN value to thirteen digits adding leading zeros by default
- Adding a schema validator in taz-consumer-label


## [2.387.0]() 2023-08-21


### Features

- changing `taz-consumer-media` to send events to new pubsub `taz-media-export`


## [2.386.1]() 2023-08-14


### Features

- Change product url formation


## [2.386.0]() 2023-08-11


### Features

- delete fixed mongodb port


## [2.385.0]() 2023-08-08


### Features

- new flag to disable seller product inactivation flow


## [2.384.2]() 2023-08-07


### Features

- Problem in the field number of pages extracted from metabooks enrichments


## [2.384.1]() 2023-08-07


### Bugfixes

- fix download images metadata-input to make ack when occurred exception


## [2.384.0]() 2023-08-07


### Features

- refactoring complete-product consumer removing things no longer needed


## [2.383.0]() 2023-08-02


### Features

- changing metadata-input flow to use pubsub taz-metadatainput and remove SQS


## [2.382.2]() 2023-07-31


### Features

- reprocess maas-product validate if product has factsheet to resend info or not


## [2.382.1]() 2023-07-31


### Bugfixes

- tratando retorno da omnilogic de json invalido


## [2.382.0]() 2023-07-27


### Features

- Add endpoint rebuild to datalake


## [2.381.2]() 2023-07-27


### Bugfixes

- Fix payload sent to BigQuery on `taz-datalake`


## [2.381.1]() 2023-07-26


### Bugfixes

- fix special content in `taz-consumer-factsheet` when product has datasheet


## [2.381.0]() 2023-07-26


### Features

- adds flow for datasheet's scope processing
- create merger execution priority
- ignore event on factsheet merger if product has datasheet
- refactoring the slower unit tests
- add enrichment undo action by datasheet
- Add datasheet scope in `taz-metadata-verify`


## [2.380.1]() 2023-07-18


### Bugfixes

- fix settings mongodb options


## [2.380.0]() 2023-07-17


### Features

- adding extra data field on product-writer
- changing config mongodb to accept options from environment variable


## [2.379.1]() 2023-07-17


### Features

- changing endpoint extra-data to save field fulfillment when exists


## [2.379.0]() 2023-07-13


### Features

- adding endpoint extra data
- added consumer of labels for 1p products


## [2.378.1]() 2023-07-10


### Features

- fix read timeout google storage upload

### Improved Documentation

- Updated documentation for dags


## [2.378.0]() 2023-07-10


### Features

- add function to replace normalized term by approximation
- change default value of ID_LENGTH to create navigation_id with 9 characters in staging environment
- normalize forbidden terms keys


## [2.377.0]() 2023-07-04


### Features

- change unpublish query to use or statement


## [2.376.0]() 2023-07-03


### Features

- Added endpoints for exporting source_product and simple_product


## [2.375.0]() 2023-06-22


### Features

- Changed status sent to Patolino in the consumer product
- Changed statuses sent to Patolino in consumer product-writer


## [2.374.0]() 2023-06-15


### Features

- add endpoint to get forbidden terms info from database
  add endpoint to delete keys forbidden terms in redis


## [2.373.0]() 2023-06-13


### Features

- add token handling with cache control


## [2.372.0]() 2023-06-07


### Features

- replaces forbidden terms within factsheet values
- add new endpoints api to handle with forbidden terms
- add forbidden terms replace in `taz-consumer-product`
- add md5 validation in `taz-consumer-factsheet`
- Changing how the md5 hash works in the raw products collection and making some improvements to taz-consumer-product


## [2.371.0]() 2023-06-01


### Features

- changing mongodb production config


## [2.370.10]() 2023-05-31


### Bugfixes

- fix get categories on scope simple-product


## [2.370.9]() 2023-05-22


### Features

- changing redishot instance sandbox environment

### Bugfixes

- Discard inactive product images as main_media candidates


## [2.370.8]() 2023-05-15


### Bugfixes

- Uses orientation of exif tags to rotate the image


## [2.370.7]() 2023-05-10


### Bugfixes

- Fixes orientation issue for images using EXIF tags


## [2.370.6]() 2023-04-27


### Features

- Changing log level to debug from `taz-poller-product`
- Removing consumers that are no longer running

### Bugfixes

- Gitlab pipeline fix adding a sync app command in argocd


## [2.370.5]() 2023-04-19


### Deprecations and Removals

- Removing prohibited terms validation


## [2.370.4]() 2023-04-11


### Bugfixes

- Fix code send to patolino in `taz-consumer-stock-3p`


## [2.370.3]() 2023-04-04


### Bugfixes

- fix scope stock in taz-consumer-datalake to only receive messages when product has already been created


## [2.370.2]() 2023-04-03


### Bugfixes

- fix taz-consumer-datalake to send stock from product 3P to BQ


## [2.370.1]() 2023-03-31


### Features

- fix query taz-consumer-stock-3p


## [2.370.0]() 2023-03-30


### Features

- create taz-consumer-price-3p
- create taz-consumer-stock-3p


## [2.369.0]() 2023-03-29


### Features

- Changing `price` scope on `consumer-datalake` to send price data to Big Query


## [2.368.0]() 2023-03-27


### Features

- Create BaseStorage and RawProductsStorage and changing structure from FactsheetStorage


## [2.367.1]() 2023-03-17


### Features

- Removing html tags from product attribute values
- Gitlab pipeline execution order adjustment
- Configuring a fixed scheme for sending media data to the datalake


## [2.367.0]() 2023-03-15


### Features

- Changing CacheLock to connect with Redis using param socket_connect_timeout and socket_timeout

### Bugfixes

- Removal of categorization for RC on product update event


## [2.366.0]() 2023-03-14


### Features

- Adding automated creation of gmud

### Bugfixes

- Fixed command to generate version


## [2.365.2]() 2023-03-13


### Bugfixes

- Fixing issue with unit tests looping because of grpcio lib

### [2.365.1] - 2023-03-13

### Changed

* Changing notification endpoint to not return payload when receive a request

### [2.365.0] - 2023-03-02

### Changed

- Updating python version and dependencies from project

### [2.364.1] - 2023-03-01

### Fix

* Fix sonar

### [2.364.0] - 2023-02-28

### Added

* Added checking of categorization on merge

### [2.363.0] - 2023-02-27

### Changed

* Send success status to patolino in the media creation flow regardless of whether the product has been created

### [2.362.1] - 2023-02-23

### Fix

* Fix Smartcontent scope to validate if title from enriched exists to process title normalize and cleanup

### [2.362.0] - 2023-02-15

### Fix

* Fix smartcontent scope to clean reference when category not allowed to have this value

### [2.361.2] - 2023-02-15

### Fix

* Price and stock update fix on `taz-consumer-price`

### [2.361.1] - 2023-02-13

### Added

* Add theme type to ProductSpecification Enum

### [2.361.0] - 2023-02-06

### Changed

* Changing taz `consumer-factsheet` and `consumer-product-exporter` to send ordering key to PubSub

### [2.360.0] - 2023-02-02

### Fix

* Fix getting variation categories on matching

### [2.359.0] - 2023-02-02

### Added

* Add skin_color type to ProductSpecification Enum

### [2.358.2] - 2023-01-30

### Changed

* Changing slugify in taz `consumer-product-writer`, `consumer-price` and `consumer-matching`

### [2.358.1] - 2023-01-24

### Fix

* Correction in production environment of header in `poller-badge`

### [2.358.0] - 2023-01-23

### Changed

* Put authentication via header in poller-badge

### [2.357.2] - 2023-01-18

### Changed

* Removed new relic

### [2.357.1] - 2023-01-16

### Changed

* Setting pollers database password to use environment variable

### [2.357.0] - 2023-01-13

### Fix

* Fixing send images to product-metadata topic

### Changed

* Changing endpoint delete and post from unpublish product to search product by navigation_id with 7 and 9 digits

### [2.356.0] - 2023-01-10

### Changed

* Changing `consumer-product` delete method when product already disabled then only notify patolino and skip process
* Changing `consumer-product` delete method to make upload to bucket with original data from seller

### [2.355.0] - 2023-01-10

### Changed

* Changing `consumer-factsheet` to send factsheet data to pubsub `taz-factsheet`

### [2.354.2] - 2022-12-20

### Changed

* Change `consumer-product-score` queries to only update active scores

### [2.354.1] - 2022-12-08

### Changed

* Changing `consumer-product-writer` to send payload with delete action to patolino when product is disable_on_matching true

### [2.354.0] - 2022-12-08

### Changed

* Change `consumer_review` flow

### [2.353.1] - 2022-12-06

### BugFix

* Fix slug validation in `taz-consumer-product-score`

### [2.353.0] - 2022-12-06

### Add

* Adding score v3 to calculate score with data from factsheet product

### Changed

* Changing score endpoints to work with more than one score versions

### [2.352.0] - 2022-12-01

### Bugfix

* Remove rule to check if the product has an identifier for the type of event classify

### Changed

* Add hector scope in `taz-consumer-product-exporter`

### [2.351.0] - 2022-10-25

### Bugfix

* Fix `sells_to_company` field `null` in raw_products collection

### [2.350.1] - 2022-10-21

### Changed

* Changing `consumer-product` to clean whitespace from ean value

### [2.350.0] - 2022-10-20

### Changed

* Changing merger and categoryMerger to handle with hector source from enriched products data

### [2.349.0] - 2022-10-13

### Add

* Adding endpoint to rebuild product in classifier flow
* Adding new scope classifier_product in `consumer-rebuild` to process event from classifier rebuild endpoint

### [2.348.0] - 2022-10-11

### Changed

* Rule change to select winning variation on matching, 1p has preference

### [2.347.0] - 2022-10-10

### Changed

* Add distributed lock for consumer price

### [2.346.0] - 2022-10-07

### Changed

* Added source parameter to skip return of original attributes on merge of `consumer-product`

### [2.345.0] - 2022-10-06

### Changed

* Changing `consumer-factsheet`, `consumer-media`, `consumer-price`, `consumer-product`, `consumer-product-writer` to always send notifications about a SKU process result (SKIP / ERROR / PUBLISH / UNPUBLISH)

### [2.344.0] - 2022-10-06

### Changed

* Change marvin notifications from sns to pubsub

### [2.343.3] - 2022-10-04

### Changed

* Update certifi library

### [2.343.2] - 2022-10-04

### Add

* Adding logs for product enrichment flow

### [2.343.1] - 2022-09-29

### Fix

* Fix in publishing products that have duplicate price records in the collection

### [2.343.0] - 2022-09-28

### Changed

* Offers published even with sku with missing price
* Change swagger authentication to use header

### [2.342.2] - 2022-09-27

### Changed

* Change 1p book enrichments to smartcontent in consumers `metdata_verify` and `media`

### [2.341.0] - 2022-09-27

### Changed

* Removing option to receive token from query string

### [2.340.0] - 2022-09-26

### Fix

* getting sku using sku and seller_id to update review

### [2.339.0] - 2022-09-26

### Changed

* Add attribute `event_type` to pubsub messages that metadata_verify consumer sends

### [2.338.0] - 2022-09-22

### Changed

* Change sandbox mongo database server

### [2.337.0] - 2022-09-19

### Fix

* Using review component to retrieve review

### [2.336.0] - 2022-09-14

### Add

* Add authentication oath of gcp

### [2.335.0] - 2022-09-08

* Changing `user_review` consumer to increase logs

### [2.334.0] - 2022-09-08

### Fix

* Fix seller_description in `consumer-product`

### [2.333.0] - 2022-09-05

### Fix

* Fix list_price error in `consumer-product-writer`

### [2.332.2] - 2022-08-29

### Add

* Adding tag runner-gcp in gitlab pipeline

### [2.332.1] - 2022-08-29

### Changed

* Changing `consumer-datalake` to send parent_matching_uuid to Big query

### [2.332.0] - 2022-08-22

### Changed

* Changing `product-writer` consumer to add `parent_matching_uuid` for indexing-process
* Changing `consumer-matching` to store `parent_matching_uuid`

### [2.331.4] - 2022-08-17

### Changed

* Changing `product-writer` consumer to use info from `unified_objects` to mount media path

### [2.331.3] - 2022-08-15

### Changed

* Removed `_id` of return of find on `consumer-product-writer`

### [2.331.2] - 2022-08-12

### Changed

* Changing `consumer-product-exporter` scope simple product to send parent matching uuid

### [2.331.1] - 2022-08-12

### Changed

* Changing `consumer-matching-product` to update raw_products with parent matching value

### [2.331.0] - 2022-08-11

### Add

* MagaluCloud integration (S3) to Taz

### [2.330.3] - 2022-08-10

### Fix

* Fix variation without price in `product writer` consumer

### [2.330.2] - 2022-08-09

### Changed

* Changing notification Chester to send parent_sku from product

### [2.330.1] - 2022-08-04

### Changed

* Sort subcategories in consumer datalake

### [2.330.0] - 2022-08-01

### Changed

* Changing endpoint `v1/products` to accept navigation_id to get product

### [2.329.0] - 2022-08-01

### Changed

* Changing Dag Product Writer
* Removed token in API log

### Fix

* Allowing to run taz api in local environment

### [2.328.0] - 2022-07-26

### Fix

* Remove selector when empty value

### Changed

* Allow disabling all categories when enriching selectors coming from omnilogic

### [2.327.0] - 2022-07-21

### Add

* Adding extra data when sending the product to the data lake

### Changed

* Inclusion of fulfillment and matching_uuid fields in `consumer-datalake`

### [2.326.0] - 2022-07-20

### Changed

* Change in in-memory cache clear interval
* Pipeline `Security Gate` running only on master

### Add

* Class creation to work with cached badges

### [2.325.1] - 2022-07-18

### Change

* fix production settings file

### [2.325.0] - 2022-07-15

### Add

* Add security step in gitlab pipeline

### Fix

* Fix security issues

### [2.324.0] - 2022-07-14

### Add

* Adding extra data in simple_product payload

### [2.323.0] - 2022-07-12

### Add

* Adding the matching_uuid field in the `product-writer` consumer

### [2.322.0] - 2022-07-12

### Changed

* Add skip for media consumer

### [2.321.3] - 2022-07-11

### Changed

* Securing the context of seller registration endpoints

### [2.321.2] - 2022-07-06

### Fix

* Fixed exception raising when posting message in kinesis

### [2.321.1] - 2022-07-06

### Changed

* Change in the order of sending messages in the consumer `product-writer`

### [2.321.0] - 2022-07-01

### Changed

* Changing consumer `product-writer` to use cache when search categories

### [2.320.0] - 2022-06-30

### Fix

* Fixed scope factsheet on consumer datalake
* Add escape character in element of invalid character

### [2.319.0] - 2022-06-30

### Fixed

* Payload fix sent to `taz-indexing-process`

### [2.318.2] - 2022-06-29

### Changed

* Changing `consumer-price` to not skip update product when verify md5

### [2.318.1] - 2022-06-24

### Changed

* Changing the enriched product count in product writer consumer

### [2.318.0] - 2022-06-24

### Changed

* Refactoring product writer queries

### [2.317.0] - 2022-06-23

### Add

* Add endpoint to remove enriched product source

### [2.316.0] - 2022-06-17

### Fix

* Fixing merger flow to verify if field isbn exists to remove Smartcontent source

### Changed

* Changing endpoint v1/products to return medias information

### [2.315.2] - 2022-06-13

### Changed

* Changing merger flow if product is book and has enriched by Metabooks and Smartcontent

### [2.315.1] - 2022-06-13

### Fix

* Fix price check in product writer

### [2.315.0] - 2022-06-10

### Add

* Adding type to attributes published by product-exporter

### Changed

* Change of logs in taz-consumer-stock

### [2.314.0] - 2022-06-09

### Add

* Changing `matching-product` consumer to save matching_type in raw products

### [2.313.0] - 2022-06-09

### Changed

*  Remove omnilogic brand enrichment

### [2.312.1] - 2022-06-09

### Changed

* Enabling LOG_LEVEL environment variable to change log dump level

### [2.312.0] - 2022-06-07

### Add

*  Adding to product endpoint the possibility to search by matching uuid

### [2.311.0] - 2022-06-06

### Add

* Add project parameter in pagination class
* Remove products field from /v1/badges

### [2.310.0] - 2022-06-02

### Add

* Verify if title field has value to send notification to Chester

### Fix

* Fix path poller badge

### [2.309.2] - 2022-06-02

### Fix

* Fix settings poller badge


### [2.309.1] - 2022-06-02

### Fix

* Fix badge list
* Remove endpoint swagger: GET /badge and DELETE /badge

### [2.309.0] - 2022-05-31

### Add

* Adding endpoint /v1/products with pagination of open api

### [2.308.1] - 2022-05-31

### Fix

* Fix bug skip md5 consumer price

### [2.308.0] - 2022-05-24

### Add

* Add the field `matching-uuid` in consumer `product-exporter` scope simple_product

### [2.307.0] - 2022-05-17

### Add

* Add endpoint to send products to matching

### [2.306.4] - 2022-05-16

### Fix

* Add nullable validation in enriched datalake scope

### [2.306.3] - 2022-05-16

### Fix

* Update enriched products in datalake consumer for parse timestamp from string to float

### [2.306.2] - 2022-05-16

### Add

* Add metadata verify consumer for monitoring in New Relic
* Add product writer consumer for monitoring in New Relic

### [2.306.1] - 2022-05-05

### Fix

* Removing exception when cannot update raw_products in matching product consumer

### [2.306.0] - 2022-05-03

### Add

* Adding fulfillment in product writer payload

### [2.305.1] - 2022-04-28

### Fix

* Fixed of ALLOW_PUBLISH_PRODUCT_METADATA environment variable loading
* Fixed pipeline for python 3.6

### [2.305.0] - 2022-04-25

### Add

* It was developed a sent of message for product metadata publisher in metadata verify

### [2.304.0] - 2022-04-19

### Add

* Adding fulfillment in simple_product payload

### [2.303.0] - 2022-04-13

### Add

* create the new consumer matching product
* Adding datasheet scope in consumer datalake

### [2.302.0] - 2022-04-11

### Fix

* Fix resizing images with transparency

### [2.301.0] - 2022-04-04

### Add

* Adding CORS in the api

### [2.300.1] - 2022-03-28

### Fix

* fix matching of product with attributes nulls

### [2.300.0] - 2022-03-22

### Fix

* Fixing SNS topic off review notification

### [2.299.0] - 2022-03-22

### Changed

* removing duplicity from user review data

### [2.298.0] - 2022-03-17

### Add

* Adding seller data submission in a pubsub taz-sellers topic

### [2.297.1] - 2022-02-23

### Add

* Add selections in log info in poller product

### [2.297.0] - 2022-02-21

### Changed

* Changed the integration with `patolino` by sending the notification directly to pubsub

### [2.296.0] - 2022-02-17

#### Changed

* Change creation of sells_to_company key in taz-consumer-product
* Change sellers handler of taz-api to check if sells_to_company key has changed and notify rebuild SQS

### Add

* Add escope 'seller_sells_to_company' in taz-consumer-rebuild

### [2.295.0] - 2022-02-14

### Add

* Send factsheet to data lake using niagara
### Changed

* Changed the integration with `patolino` by sending the notification directly to pubsub

#### Changed

* Notification type `review` in user-reviews consumer

### [2.294.0] - 2022-02-08

### Add

* Add wrapper to map methods from consumers to be monitored in New Relic

### [2.293.2] - 2022-01-19

### Fix

* Fix category fallback flow in consumer datalake

### [2.293.1] - 2022-01-18

### Add

* add newrelic in requirements to use new relic agent

### [2.293.0] - 2022-01-13

### Changed

* Send to Marvin Api all of seller types

### [2.292.2] - 2022-01-13

### Add

* Adding a new non alphanumeric characteres in method clean_data in `consumer product`

### [2.292.1] - 2022-01-13

### Add

* Add dags folder in sonar exclusion coverage

### [2.292.0] - 2022-01-12

### Add

* Add field `sells_to_company` in simple product payload
### Change

* add checkpoint in dag taz_ingestion to process data every day

### [2.291.1] - 2021-12-15

### Add

* Selections `24466`, `24467`, `24468`, `24469`, `24470`, `24471`, `24472`, `24473`, `24474` and `24475` in product poller query

### Changed

* Refactor DAG taz_ingestion
### Changed

* Use `simple_settings` to set selections in product poller query

### [2.291.0] - 2021-12-14

#### Changed

* Optimizations in the api

### [2.290.0] - 2021-12-14

### Fix

* When exist a product category in feature toogle, normalize attributes with seller data
* Add debug logger for help troubleshootings
* Fixed the labeling in assembler

### [2.289.0] - 2021-12-13

### Add

* Add database pagination to inactivate seller products consumer rebuild

### [2.288.0] - 2021-12-13

### Add

* Adding new badge request with pagination

### [2.287.3] - 2021-12-09

### Fix

* Fix marvin-seller flow changing cursor to list

### [2.287.2] - 2021-12-09

### Fix

* Fix marvin-seller scope in consumer rebuild

### [2.287.1] - 2021-12-03

### Fix

* Fix marvin-seller flow to use cursor to access data in rebuild process

### [2.287.0] - 2021-11-30

#### Changed

* Accept only `navigation_id` in user reviews consumer

### [2.286.0] - 2021-11-30

#### Changed

* Config to run cron range by env var

### [2.285.1] - 2021-11-25

### Fix

* Add timeout in patolino request

### [2.285.0] - 2021-11-19

### Add

* Add database pagination to marvin-seller consumer rebuild

### [2.284.0] - 2021-11-18

#### Fixed

* Send XML products to Bazaarvoice with original and cutted id when is main seller

### [2.283.4] - 2021-11-17

### Add

* Add timeout parameter in ipdv put request

### [2.283.3] - 2021-11-17

### Fixed

* Add entity and filters_metadata in simple_product payload when without metadata in omnilogic response

### [2.283.2] - 2021-11-12

### Fix

* Fix seller inactivation flow query in consumer rebuild

### [2.283.1] - 2021-11-10

### Add

* Add selection 24465

### [2.283.0] - 2021-11-09

### Add

* Add smartcontent enrichment for attributes and titles when category is MD

### [2.282.1] - 2021-10-17

### Fixed

* Fix of deletion in poller-product

### [2.282.0] - 2021-10-14

### Fixed

* Fix on unpublishing when attributes are duplicated

### [2.281.0] - 2021-10-13

#### Add

* Update brand in raw_product with original brand when brand is not enriched by omnilogic

#### Changed

* Notify slack when error occurs in crontabs
* Configure channel and webhook from slack crontabs by env var

### [2.280.0] - 2021-10-08

### Added

* Add presentation field to factsheet payload in consumer metadata_verify

### [2.279.1] - 2021-10-06

#### Changed

* Remove unused method _check_trusted_seller
* Change taz mongodb endpoint for production

### [2.279.0] - 2021-10-05

#### Changed

* Change organization in gitci file

### Added

* Add endpoint `/trusted_product/ean`

### [2.278.1] - 2021-09-30

#### Changed

* Change stagint url used in sast properties to https

### [2.278.0] - 2021-09-30

#### Added

* Add log to track wrong price x cubage in consumer price

### Fixed

* Remove old metabooks enrichments

#### Changed

* Update Fortify

### [2.276.0] - 2021-09-16

### Changed

* Toggle feature disable internal omnilogic

### [2.275.0] - 2021-09-15

### Added

* Add field "normalized_filters" in the payload of product_exporter

### [2.274.1] - 2021-09-15

### Changed

* Change `or` query in single seller matching

### [2.274.0] - 2021-09-13

### Added

* implemented new feature for send product manual to factsheet

### Added

* Add user-review argocd pipeline in gitlabci

### [2.273.4] - 2021-09-03

### Fixed

* Fix the unfinished process log on the patolino

### Added

* Add a 404 handle when call acme to delete a category

### [2.273.3] - 2021-08-26

### Fixed

* Adding poller and cron step for deploy in argocd

### [2.273.2] - 2021-08-24

### Added

* Selections `24459`, `24460` e `24461` in product poller query

### [2.273.1] - 2021-08-24

### Added

* Add taz-api and consumers to argocd in gitci
* Selections `24459`, `24460` e `24461` in product poller query

### [2.273.0] - 2021-08-23

### Added

* Add special content in factsheet for smartcontent scope

### [2.272.0] - 2021-08-20

#### Added

* User review consumer

### [2.271.8] - 2021-08-20

### Added

* Add source Omnilogic in search enriched product with product hash

### [2.271.7] - 2021-08-12

### Added

* Add taz dags on project
* Add toggle feature in smartcontent atributtes merge

### [2.271.6] - 2021-08-10

### Fixed

* fix generation of product_hash for rebuild product and fix raw_product validation

### [2.271.5] - 2021-08-09

### Changed

* generate partition keys for each data

### Fixed

* Fix wait time environment variable for pollers

### [2.271.4] - 2021-08-04

#### Added

* Selection `24458` in product poller query

### [2.271.3] - 2021-08-03

### Fixed

* Fix title overwrite in Omnilogic merge scope

### [2.271.2] - 2021-07-28

### Fixed

* Fix navigation_id formatting five digits for nine digits

### [2.271.1] - 2021-07-26

### Fixed

* Fix conection error in pymssql to free memory

### [2.271.0] - 2021-07-23

### Changed

* Adding media download timeout in `consumer-media`

### [2.270.0] - 2021-07-22

### Changed

* generate new product_hash when it doesn't exist

### [2.269.0] - 2021-07-20

### Changed

* Change webhook on slack notifier

### [2.268.0] - 2021-07-19

### Added

* Redis migration to redishot

### [2.267.2] - 2021-07-19

### Fixed

* Fix product-exporter to sort canonical_ids list to change less the offer id

### [2.267.1] - 2021-07-19

### Added

* Add pontecy type to ProductSpecification Enum

### [2.267.0] - 2021-07-13

### Changed

* Change flow on process message to call less database when retry occurred
* Change `complete-product` to verify if message source is external OL and category_id allowed

### [2.266.0] - 2021-07-08

### Changed

* Unpublish product now unpublish only the variation sent to unpublish

### Fixed

* Fix datalake consumer

### [2.265.4] - 2021-07-05

### Added

* Add logs in consumer media

### [2.265.3] - 2021-07-05

### Added

* Add log debug in Kinesis broker

### [2.265.2] - 2021-07-05

### Fixed

* Change scope name 'score' to 'product_score'

### [2.265.1] - 2021-07-01

### Fixed

* Removed useless self-assignment

### [2.265.0] - 2021-07-01

### Changed

* Send original data from seller to datalake in new GCP topic name
* Remove method title from reference field

### [2.264.6] - 2021-06-23

### Fixed

* Stop closing session at the end of a poller process

### [2.264.5] - 2021-06-21

### Fixed

* Fix poller product creating a new query
* Fix poller product query

### [2.264.4] - 2021-06-17

### Fixed

* Fix poller product sql

### [2.264.3] - 2021-06-16

### Fixed

* Improve poller product data fetch

### [2.264.2] - 2021-06-15

### Fixed

* Add read uncommitted in poller product query to fix nolock error

### [2.264.1] - 2021-06-15

### Fixed

* Add nolock in all tables at poller product query

### [2.264.0] - 2021-06-10

### Changed

* Update attributes with seller original data when sku_metadata is null

### [2.263.3] - 2021-06-10

### Fixed

* Fix sonar bug

### [2.263.2] - 2021-06-09

### Changed

* Change assembler Single Seller Strategy in matching to use skus disable_on_matching

### [2.263.1] - 2021-06-08

### Changed

* Change pubsub broker message log.

### [2.263.0] - 2021-06-08

* #### Changed

*  Include enrichment by smartcontent when not enriched by metabooks in `metadata-verify` for books

### [2.262.0] - 2021-06-08

### Changed

* Change in the frequency of updating the cron `metabooks_ftp` to hourly

### [2.261.1] - 2021-06-08

### Changed

* Revert query from price-campaign poller.

### [2.261.0] - 2021-06-01

### Changed

* Change sender of the price campaign poller from kinesis to pubsub

### [2.260.0] - 2021-05-28

#### Fixed

* Fix product-exporter to choose offer_id based on the stock number
* Add new field id_correlations in payload from product-exporter

#### Changed

* Categorization bigdatacorp to magalu in `consumer-bigdatacorp`

### [2.259.0] - 2021-05-24

#### Changed

* Configuration of renewing the processing of the kinesis and time limit processing 600 seconds

### [2.258.0] - 2021-05-24

### Changed

* Verify if scope are allowed to send images to media consumer
* Add prefix BIG in seller_id on bigdatacorp consumer

### [2.257.3] - 2021-05-19

#### Fixed

* Stop sending every product TM that appears in metadata-verify, send only Metabooks

### [2.257.2] - 2021-05-19

#### Changed

* Merge scope smartcontent stop normalizing title

#### Fixed

* Remove token from metadata-input-media-exception

#### Changed

* Add prefix BIG in seller_id on bigdatacorp consumer

### [2.257.1] - 2021-05-18

#### Fixed

* Fix endpoint that count products from a seller

### Changed

* Verify if scope are allowed to send images to media consumer

#### Changed

* update project readme file

### [2.257.0] - 2021-05-12

#### Changed

* Apply event nack when response is false and exception
* Change IPDV consumer to use pubsub broker

### [2.256.0] - 2021-05-10

#### Fixed

* Fix a bug related to media when an update overwrites what came from the Metabooks.
* Fix bug when `consumer-factsheet` updates info, check if source is metadata_verify

### [2.255.0] - 2021-05-10

#### Fixed

* Remove disable_on_matching from criteria to match products in single_seller strategy

### [2.254.0] - 2021-05-05

#### Changed

* Add notification type `checkout_price` in CatalogNotificationSchema
* Product writer now send message to kinesis and to pubsub

### [2.253.0] - 2021-05-03

#### Changed

* Scope `source product` in product exporter can skip `enriched product` sources

#### Fixed

* Fix bug showed in Sonar

### [2.252.0] - 2021-04-26

#### Added

* Add smartcontent source to product_exporter helpers
* Add smartcontent scope in metadata-verify
* Add smartcontent to merger

### [2.251.1] - 2021-04-20

#### Fixed

* Fix topic to poller price

### [2.251.0] - 2021-04-20

#### Added

* Add smartcontent to metadata input

#### Changed

* Change metadata input to use scope

### Fixed

* Fix bug when trying to delete product_id list in find_product_id on matching assembler

### [2.250.0] - 2021-04-19

### Changed

* Omnilogic strategy returns all similar products instead of only actives

### Fixed

* Fix matching throwing error when product has no matching variations.
* Update all id correlations with the last product id, preventing to unpublish products

### Added

* Add type 'matching' in the schema of rebuild catalog notification endpoint

### [2.249.0] - 2021-04-13

#### Changed

* remove product writer v2

### [2.248.0] - 2021-04-05

#### Changed

* Notify patolino about error and unfinished process in product consumer
* Notify patolino when product was unpublished in product-writer

### [2.247.1] - 2021-04-05

#### Fixed

* Fix errors in core matching

### [2.247.0] - 2021-03-30

#### Changed

* Refactor in matching consumer

### [2.246.0] - 2021-03-23

#### Changed

* Update dependencies

### [2.245.1] - 2021-03-22

#### Changed

* Change query of unpublished_products in product-writer to use navigation_id converted to nine digits

### [2.245.0] - 2021-03-16

#### Changed

* Publish price poller to pubsub

### [2.244.3] - 2021-03-10

#### Changed

* Remove retries in consumer complete product and split message in 2 sources to SQS

### [2.244.2] - 2021-03-09

#### Fixed

* Fix json call in complete product

### [2.244.1] - 2021-03-09

#### Fixed

* Fix complete product consumer to send valid payload and check for error in payload

### [2.244.0] - 2021-03-08

#### Added

* Add unblockable list in inactivate_seller_products scope in rebuild consumer

#### Changed

* remove active seller check in product writer

### [2.243.0] - 2021-03-04

#### Changed

* Complete product start sending notification to Omnilogic and not to SNS

### [2.242.4] - 2021-02-26

#### Added

* Stock information from tabEstoque in price poller

### [2.242.3] - 2021-02-26

### Fixed

* Remove abstract class from code coverage

### [2.242.2] - 2021-02-25

#### Fixed

* fix product writer consumer for when the price document is not complete
* Fix logger message to be generic between partner and product on sqlserver poller

### [2.242.1] - 2021-02-24

#### Changed

* set default value for stock_count, stock_type and delivery_availability from product writer

### [2.242.0] - 2021-02-23

#### Added

* Add seller inactive reason in seller post endpoint

### [2.241.0] - 2021-02-23

#### Added

* Add Patolino notification in consumer price

### [2.240.4] - 2021-02-19

#### Fixed

* Fix tracking_id in consumers

### [2.240.3] - 2021-02-18

#### Fixed

* remove for zero in list price and price from product writer
* fix force bool in OUT_OF_STOCK_RULE_IS_ACTIVE

### [2.240.2] - 2021-02-17

#### Fixed

* Send notification in stock consumer when no stock in `prices` collection
* fix use var env for OUT_OF_STOCK_RULE_IS_ACTIVE

#### Added

* Selection `24456` in product poller query

### [2.240.1] - 2021-02-10

#### Added

* Add price type in product-exporter settings

### [2.240.0] - 2021-02-09

#### Fixed

* Always notify catalog when default seller stock changes

### [2.239.0] - 2021-01-28

#### Changed

* Add `tracking_id` in catalog notification for consumer price

### [2.238.0] - 2021-01-26

#### Added

* Add bigdatacorp consumer

### [2.237.0] - 2021-01-20

#### Changed

* Update hamilton lib

### [2.236.0] - 2021-01-19

#### Fixed

* fix stock_count value error in product-exporter and datalake consumer

#### Changed

* add disable price for magazineluiza in price consumer
* fix list_price value error from product-writer and product-writer-v2

### [2.235.0] - 2021-01-18

#### Fixed

* fix remove unavailable image from media poller

#### Added

* add tracking_id in flow

#### Changed

* remove tabEstoque from product query poller
* Remove stock restriction based in tabEstoque from base_price, price_campaign and price pollers
* aplly active and validity bundles in product query poller
* remove enable notification (patolino) key in settings
* set log level as debug from notification

### [2.234.0] - 2021-01-14

#### Changed

* kinesis paylaod compress / decompress with zlib
* metadata verify consumer refactoring

### [2.233.0] - 2021-01-14

#### Fixed

* remove "find possible relatives excluding direct" method from single seller strategy, for not to return large quantities of products

#### Added

* Added url field into patolino notification payload

#### Changed

* Set log level as debug
* remove duplicate code
* Change update to update_many in price consumer

### [2.232.0] - 2021-01-13

#### Changed

* remove consumers (doory, linx, quarantine, shipping, solr indexing) and crons (metrics, bazaarvoice reviews)

### [2.231.0] - 2021-01-13

#### Added

* Adding products classification data to metadata

#### Changed

* verify seller status for disable_on_matching in product consumer
* reducing notification for inventory update
* add metadata input notification
* metadata input accept smart content
* set log level as debug for matching

### [2.230.0] - 2021-01-12

#### Added

* add stock endpoint
* add redis poller to get and delete endpoint

#### Changed

* Change consumer price _delete method to turn stock zero
* Set product unvailable in product exporter when is unpublished

#### Fixed

* unset gift_product field from raw_products

### [2.229.0] - 2021-01-11

#### Fixed

* fix get stock 3p from price collection
* fix typo badge from product writer consumer
* when there is no price the product was falling in the out of stock rule
* fix get stock from price collection for marketplace products in simple prduct scope

#### Changed

* Set product unvailable in product exporter when is unpublished
* media consumer improvements
* bazaar voice products log improvements
* remove exception for product not found in price consumer
* add raise for status in babel callback consumer
* matching and media only in source product from product exporter
* save stock in collection from price consumer
* remove delay in queue broker
* product writer v2 log improvements

### [2.228.1] - 2021-01-07

#### Changed

* Add condition to skip cache set in badge consumer if already exists

### [2.228.0] - 2020-12-04

#### Changed

* Remove delay validation from sqs broker

### [2.227.0] - 2020-12-02

#### Changed

* Patolino sandbox token
* remove md5 from pricing consumer
* datalake, product writer log improvements
* remove update price for magalu from price consumer

#### Fixed

* not save stock when document not exists in price collection
* fix media in bv cron
* fix last_updated_at when not exist in collection
* Fix return 400 for pickustore calls

### [2.226.5] - 2020-11-30

#### Fixed

* Do not save on medias collection on delete

### [2.226.4] - 2020-11-25

#### Changed

* Separate AWS Kinesis region

### [2.226.3] - 2020-11-25

#### Changed

* add aws region env

### [2.226.2] - 2020-10-30

#### Fixed

* Description now returns empty string and not None in product-exporter

### [2.226.1] - 2020-10-27

#### Changed

* Payload in simple_product should use stock from stocks collection

### [2.226.0] - 2020-10-26

#### Changed

* Delete message when Kinises Throw error for BadRequest
* add scope in payload to sent topic for product exporter
* Scope source product in product-exporter use enriched category
* bagde poller log improvement

#### Fixed

* force string in branch_id from stock helper

### [2.225.0] - 2020-10-21

#### Added

* Add source product scope in product-exporter

#### Changed

* Improve Merge tests
* Seller post log improvements
* Remove ipdv consumer try catch

#### Fixed

* Fix md5 attribution in enriched_product

### [2.224.0] - 2020-10-07

#### Changed

* Change OL merge to use only sellers attributes when category is `MD`

### [2.223.0] - 2020-10-06

#### Fixed

* Fix image url without hash
* Fix position to generate new md5

#### Added

* Add env var to show product log from determined sellers

#### Changed

* Remove seller condition in omnilogic merge scope to keep attributes
* Change merge omnilogic scope to look in category from enriched_product
* changes order of criteria for product query

### [2.222.0] - 2020-09-28

#### Changed

* Keep attributes from raw_products when OL did not extracted

### [2.221.1] - 2020-09-23

#### Added

* Add ci-knife to deploy/rollback apps

#### Fixed

* fix coverage command for show result in terminal

### [2.221.0] - 2020-09-23

#### Fixed

* set price, list_price and stock_count for zero when field not exist in complete product

#### Changed

* check if seller is active in product_writer
* join values from merge in wakko scope
* normalize attributes for product when exist in metadata
* entity "microondas" merge with scope for omnilogic luizalabs

### [2.220.1] - 2020-09-22

#### Fixed

* Remove `_id` from raw_product before updating many
* fix enriched product flow

### [2.220.0] - 2020-09-18

#### Added

* Add log to check how many documents have been updated per sku and seller in product consumer

#### Changed

* update dependency file
* enriched product log improvement

#### Fixed

* Fix merger update to regenerate new md5 and update all documents with same seller_id and sku
* fix stock_count not exist in price document from datalake consumer

### [2.219.0] - 2020-09-17

#### Changed

* notification class accepting origin
* catalog notification sending origin rebuild

#### Fixed

* fix log only seller magalu
* reorganize condition to remove price and list_price
* send magalu images without md5 from media poller

### [2.218.0] - 2020-09-14

#### Changed

* Add log for create and update product only magalu on poller and consumer

#### Fixed

* remove price and list_price only if it exists in collection

### [2.217.0] - 2020-09-11

#### Changed

* create product writer v2 consumer
* add navigation_id in factsheet payload

### [2.216.0] - 2020-09-08

#### Added

* Log to compare enriched product from database and incoming message

#### Fixed

* fix product bundle without children in product exporter consumer
* discards products categorized as temporary in product exporter consumer
* discard empty message from product exporter consumer
* fix pickup store information on product exporter consumer

### [2.215.1] - 2020-09-02

#### Fixed

* fix code smells pointed by sonar

#### Added

* create more unit tests to improve coverage
* create BadgeNotFound to remove duplicated raises

#### Fixed

* fix pricing consumer when price not found in collection

### [2.215.0] - 2020-08-26

#### Fixed

* fix bugs pointed by sonar
* format price in simple product for product exporter

#### Changed

* add bundle information in simple product from product exporter

### [2.214.1] - 2020-08-25

#### Fixed

* fix format on simple product from product exporter
* log when attribute is not found in `metadata` in omnilogic scope instead of remove it

### [2.214.0] - 2020-08-20

#### Changed

* applying Fortify recommendation

#### Fixed

* change stock scope for notification in price consumer
* fix image url from product exporter

### [2.213.0] - 2020-08-18

#### Fixed

Remove product attributes when not found in `metadata` in omnilogic scope

#### Changed

* remove metadata verify notify from product consumer

### [2.212.1] - 2020-08-13

#### Added

* create tests to increase test coverage

#### Changed

* remove duplicate code

### [2.212.0] - 2020-08-12

#### Changed

* Add test to verify valid_ean with 14 digits
* Removed zfill from valid_ean
* Remove last two digit from product id on Enriched product endpoint

### [2.211.0] - 2020-08-12

#### Added

* Add last_updated_at info in the stock consumer
* Add attributes to pubsub on stock consumer

### [2.210.3] - 2020-08-11

#### Changed

* pricing log improvements
* inactive seller product log improvements
* remove script folder
* remove inactivate_seller_products cron
* remove duplicate block in score and update category

### [2.210.2] - 2020-08-11

#### Fixed

* fix call method by action on badge consumer

#### Changed

* Set master version in Fortify
* Increase test coverage for 90%

### [2.210.1] - 2020-08-10

#### Fixed

* Fix build removing duplicate test

### [2.210.0] - 2020-08-10

#### Changed

* Remove `amazon-kclpy` lib

### [2.209.0] - 2020-08-06

#### Added

* Add attributes to pubsub on product-exporter

#### Changed

* add price source from price and pricing consumers
* Force bytesIO to close if not being used

#### Fixed

* fix price and list price on product exporter

### [2.208.0] - 2020-08-04

#### Fixed

* Remove remove-sqlite from buildpacks url

#### Changed

* save stock magalu in price collection
* notify stock only when it is distribution center
* pubsub log improvements

### [2.207.0] - 2020-07-31

#### Fixed

* publish from pubsub to the poller expects an id, but not all pollers have this information

#### Changed

* Remove solr consumer

### [2.206.0] - 2020-07-29

#### Changed

* Get product id from raw_products instead of variation info in the integracommerce-product-callback consumer
* Remove old images consumer

### [2.205.0] - 2020-07-28

#### Changed

* change kinesis to pubsub from badge consumer

#### Added

* Add project id to notification

### [2.204.0] - 2020-07-28

#### Changed

* Modify matching consumer to notify SNS instead of SQS

### [2.203.0] - 2020-07-28

#### Fixed

* Add another condition to build image urls because of different values from media collection

### [2.202.0] - 2020-07-27

#### Fixed

* Fix build_images methods to reflect the true return of media collection
* Fix swagger endpoint

#### Added

* Add stock 3p notification to sns

#### Changed

* remove update notification to integracommerce

### [2.201.0] - 2020-07-23

#### Fixed

* Fix md5 update in the pricing consumer

#### Changed

* create category when returning 404 from update

### [2.200.0] - 2020-07-22

#### Added

* Add pubsub publisher to notification
* Add field offer_id to payload in simple_product

#### Fixed

* Fix pricing consumer name in main.py

#### Changed

* removing specification of CDs from inventory query

### [2.199.0] - 2020-07-21

#### Added

* Add pricing consumer to get dynamic prices of 1P products

### [2.198.0] - 2020-07-20

#### Changed

* rebuild log improvement
* remove retry from integracommerce consumer
* change kinesis to pubsub from category consumer
* add stock type on product exporter settings
* remove add day and increases execution time for metabooks cron
* force int worker in ic consumer

#### Fixed

* Fix stock data payload sent to datalake
* fix owner in authorization middleware

### [2.197.0] - 2020-07-17

#### Changed

* Change product consumer to use kinesis via boto
* Modify price consumer to disallow update price/list_price when product is 1P

### [2.196.0] - 2020-07-16

#### Fixed

* mock external dependency for cache unit tests
* fix product and factsheet endpoints on swagger

#### Changed

* Pinning specific google versions to solve pubsub consumer problems
* Refactoring stock helper

#### Added

* Add pollers for pricing context
* Add stock count in simple product from product exporter consumer
* Send stock information to Datalake

### [2.195.0] - 2020-07-13

#### Changed

* Set request created log as debug
* Set log level as debug for doory and linx-consumers
* Reduce IntegraCommerce consumer logs text size

### [2.194.0] - 2020-07-08

#### Added

* Selections `24454` for product poller query

### [2.193.0] - 2020-07-08

#### Added

* clean linx job from solr and arcoiro calls

### [2.192.0] - 2020-07-06

#### Fixed

* SQS mock unit tests
* IntegraCommerce consumer token mock unit tests

#### Changed

* update dependencies

### [2.191.0] - 2020-07-01

* add pollers in Procfile and Gitlab CI
* Include the symbol `&` in the allowed non alphanumeric characteres

### [2.190.0] - 2020-06-25

#### Changed

* lu content poller improvements

#### Added

* poller running in k8s
* aplly seller_id slugfy for get medias on product writer consumer

### [2.189.0] - 2020-06-24

#### Added

* create lu content poller

#### Fixed

* use product scores to sort media data and factsheet from matching consumer

### [2.188.0] - 2020-06-23

#### Changed

* Unify metadata extracted with normalized metada for descriptive payload

### [2.187.0] - 2020-06-19

#### Changed

* Change constants for notifications sent to Patolino

### [2.186.0] - 2020-06-18

#### Added

* Remove media validations

#### Changed

* marketpalce stock without stock details on stock consumer
* popular stock_details only with stock greater than zero

### [2.185.0] - 2020-06-17

#### Added

* endpoint to retrieve product from storage (raw) using `sku` and `seller_id`
* endpoint to retrieve product from storage (raw) using `navigation_id`

 ### [2.184.0] - 2020-06-17

#### Added

* Patolino notification when product is out of stock

### [2.183.0] - 2020-06-16

#### Added

* add seller_name on simple_product from product exporter

#### Changed

* add sns notification from stock consumer

### [2.182.2] - 2020-06-10

#### Added

* Selections `24450`, `24451`, `24452`, `24453` for product poller query

### [2.182.1] - 2020-06-09

#### Fixed

* remove duplicate notification in product removal rule let me know

### [2.182.0] - 2020-06-05

#### Added

* Add `url` and `name` for categories in simple_product scope on product-exporter
* Add `review_count` and `review_rating` in product-exporter

#### Changed

* Remove product attributes on metabooks scope

### [2.181.1] - 2020-06-04

#### Fixed

* add product notification in seller inactivation flow

### [2.181.0] - 2020-06-03

#### Added

* endpoint to retrieve product using `parent_sku`

### [2.180.0] - 2020-06-02

#### Fixed

* fix use var env for ENABLE_WAKKO_SCOPE
* fix use var env for PUBLISH_MARKETPLACE_STOCK_IN_PUBSUB
* fix stock type name

#### Changed

* remove notification for sqs product writer in the badge consumer
* notifying sns on the consumer badge
* add bagde in product exporter settings
* add badge in simple product on product exporter consumer
* add selections in simple product on product exporter consumer

### [2.179.0] - 2020-05-29

#### Changed

* notifying marketplace stock on pubsub
* set log level as debug on kinesis broker

#### Fixed

* fix stock type unmapped
* fix payload to send on niagara pubsub

### [2.178.0] - 2020-05-28

#### Changed

* consumer implementation of stock
* implementing stcok rules
* send product remove unpublished data to Lake
* add navigation_id to the payload for pubsub

#### Fixed

* do not make requests when there is no isbn or ean

### [2.177.0] - 2020-05-26

#### Changed

* set log level as debug

### [2.176.0] - 2020-05-25

#### Added

* send product unpublished data to Lake
* command to fix imports
* add codes of cashback selections in poller query

#### Fixed

* add escape special characters for brand
* add stock consumer to gitlab-ci
* add treatment when image resize error occurs

#### Changed

* ignore the timestamp to generate the md5

### [2.175.0] - 2020-05-22

### Fixed

* fix tests mocking kinesis
* raise error when pubsub cannot process the message

#### Added

* add pubsub broker for consumers

### [2.174.1] - 2020-05-20

#### Fixed

* Fix product-exporter to not create a list of lists

### [2.174.0] - 2020-05-19

#### Changed

* refactoring geoDelivery
* Retrieve geoDelivery from IndexerAPI

### [2.173.0] - 2020-05-16

#### Fixed

* fix merge on wakko scope

#### Changed

* Standardize mock call assert on product_exporter consumer tests

#### Added

* Add success and error notification to product consumer

### [2.172.0] - 2020-05-14

#### Added

* Send notification message to Patolino with process download media result

#### Changed

* Change grpcio version
* Send notification when publish on product_exporter internal feeds pubsub

### [2.171.0] - 2020-05-13

#### Added

* Add notification to patolino when factsheet failed or succeeded

#### Fixed

* convert values of the keys "descriptive" and "delivery" to list in the pubsub simple product scope
* fix to send navigation id with 9 digits when numeric

#### Changed

* production and sandbox deployment via CI

### [2.170.0] - 2020-05-11

#### Fixed

* remove raise exception from notification sender

#### Changed

* change media consumer for resize images

#### Added

* create script for resize product from storage

### [2.169.0] - 2020-05-11

#### Added

* Create wakko scope to process on merge

* merge refactoring


#### Changed

* Convert dict values to list in product-exporter consumer

### [2.168.0] - 2020-05-06

#### Added

* Create role on `taz-consumer-enriched-product` to skip message if it is already been processed

### [2.167.0] - 2020-05-06

#### Added

* Priorize wakko attributes on create_enriched_payload

#### Changed

* Add entity in payload from simple product

### [2.166.0] - 2020-04-30

#### Changed

* Add specific selections to the product query in the poller

#### Fixed

* Fix factsheet url in product exporter
* Fix factsheet url in complete product
* Remove query metric for matching quantity

#### Added

* Added `aroma` in product specification
* Add starting notification to product_write consumer

### [2.165.0] - 2020-04-23

#### Changed

* change get factsheet http to storage in product indexing consumer

### [2.164.0] - 2020-04-20

#### Fixed

* Remove ObjectId and serialize datetime objects to send unpublished product notification

#### Changed

* Set log level as debug
* Change method `.capitalize` to `.title` in create product processor

### [2.163.0] - 2020-04-16

#### Added

* Add endpoint to get seller information
* Settings for patolino in production

#### Changed

* ipdv postback log improvements

### [2.162.0] - 2020-04-15

#### Changed

* Accepting multiple tags html for breakline

### [2.161.0] - 2020-04-14

#### Changed

* Send task_id to rebuild queue based on seller id and scope

### [2.160.0] - 2020-04-14

#### Added

* Add persistence of sellers in SellersHandler

### [2.159.0] - 2020-04-10

#### Fixed

* Fix exception when integration is none on ipdv scope
* Not sending empty payload to pubsub
* Remove lowest price validation

#### Added

* Add MPEG to valid medias types

### [2.158.0] - 2020-04-09

#### Added

* Add notification to product_write consumer for unpublished products
* Create rebuild scope for register ipdv sellers

#### Fixed

* Fix order images from Metabooks books
* Fix duplicated products from Magazine Luiza in matching

### [2.157.0] - 2020-04-07

#### Added

* Endpoint to receive seller and call inactive seller rebuild to inactivate seller products
* Rebuild Scope for inactive products for seller

#### Changed

* Notify rebuild ipdv marvin seller on seller endpoint

### [2.156.0] - 2020-04-02

#### Added

* create class to send notification for Patolino
* create get factsheet endpoint

#### Changed

* adjustment for publishing the flow to display catalog data on pubsub
* raise exception when unable to download image
* returning workers' processing log as info
* adjustment in ipdv to log specific errors
* add metadata e filters metadata in simple product scope
* normalizing metabooks labels

### [2.155.0] - 2020-03-30

#### Added

* create product exporter consumer
* create `simple_product` scope from product exporter consumer
* create `product_features` scope from product exporter consumer
* create rebuid product exporter endpoint

#### Changed

* remove put queue from shipping consumer

### [2.154.0] - 2020-03-27

#### Fixed

* Correting when we update `disable_on_matching` now we update `md5` too

#### Changed

* Add verification on `taz-consumer-product` to not skip update when `disable_on_matching` is True

### [2.153.0] - 2020-03-26

#### Changed

* enable to set log level by env var
* if there is no ean, send the isbn to the consumer of the complete product
* add product_hash in update from product consumer
* change worker and max attempts in media poller

#### Fixed

* correction for not recording empty payload in the media collection for magalu products
* fix price none in out of stock rule
* correction for when it is not possible to extract skus from the product

#### Added

* create script to resend products to SNS

### [2.152.0] - 2020-03-23

#### Changed

* for book category send the data of the mongo instead of storage because of the enrichment by metabooks
* changing sort images by url
* send bundles payload as list to datalake

#### Fixed

* correcting message sent to queue through product consumer

### [2.151.0] - 2020-03-18

#### Changed

* changing description `Magazine Luiza` to `Magalu`
* Removing sort images by url

### [2.150.0] - 2020-03-17

#### Changed

* applying slugify to the attribute when it doesn't exist in our white list

#### Added

* enabling released entities for matching via omnilogic

### [2.149.0] - 2020-03-16

#### Changed

* Replace "-" for "_" keys to send enriched products to datalake
* invert order of search by product in `complete_product` consumer
* Sort sellers by prices without default seller at the top

### [2.148.0] - 2020-03-11

#### Changed

* remove old_images consumer command from Makefile
* change cron schedule from store pickup checker
* add try/except in metabooks ftp cron
* use sku_name in reference fields when matching from omnilogic

#### Added

* adds deploy command for search consumers

### [2.147.0] - 2020-03-05

#### Fixed

* Skip delete on poller when a error happens on product cursor
* Adding Redis Key to Poller process continue after fatal exceptions
* Changed the MONGODB_HOST port from 27019 to 27017 (MongoDB default port)
* Altered test_should_return_distinct_active_sellers assert to use sorted
* Changed the products in TestRebuildSellersCrontab Class
* Removed no_cursor_timeout from pymongo count in UpdateIdRawProduct Class

#### Added

* Added metric logs to download_media

#### Changed

* Changed the way to write bytes from response.content on media consumer and improved error logs
* Changed ALLOWED_HTML_TAGS to env variable and removed tags IMG and HR

### [2.146.0] - 2020-01-27

#### Fixed

* fix media download from media consumer

### [2.144.0] - 2020-01-22

#### Added

* Add new validations for images.

### [2.143.0] - 2020-01-15

#### Fixed

* Fix badge duplication when updating

#### Added

* adding shipping consumer from sqs

### [2.142.0] - 2020-01-10

#### Added

* changing log message for product not found in frajola
* adding original url images in media document

#### Changed

* sonar enhancements and bugfixes
* removing category import call from babel in category consumer
* changed `get_price` to always get the first price
* removing mandatory isbn field on product
* sending all product enrichments to datalake

### [2.141.1] - 2019-12-19

#### Added

* adding fortity on gitlab ci
* Create endpoint to get medias from product by seller and sku

### [2.141.0] - 2019-12-17

#### Added

* Create endpoint to get medias from product by seller and sku
* Create endpoint to get medias from product by navigation id

### [2.141.0] - 2019-12-17

#### Fixed

* Fix missing space in run_parallel_cron_deploys command
* Fix error when product enriched with none entity in payload

#### Changed

* Remove delete action in `ipdv_product_postback` consumer
* converting list to string from value in factsheet merger

### [2.140.0] - 2019-12-16

#### Changed

* Send `url` and `published` keys to iPDV on `ipdv_product_postback` consumer

### [2.139.0] - 2019-12-12

#### Changed

* Update requirements

### [2.138.0] - 2019-12-09

#### Fixed

* fix factsheet not found from enriched product consumer
* force omnilogic source in criteria from merge

#### Changed

* Add validation in `badge` endpoint for badge existence

### [2.137.0] - 2019-12-03

#### Added

* Command to run consumer, cron in parallel
* Metrics for products without stock
* Script to clean products without stock

#### Changed

* adding log to send payload from rebuild sellers
* Add zero stock rule that deletes out-of-stock products for more than certain days

### [2.136.1] - 2019-11-28

#### Fixed

* check if there is no `entity` in enriched data

### [2.136.0] - 2019-11-06

#### Changed

* adding product payload when skip product update
* reversing order to get product data for sent from Omnilogic
* changing notification class to sqs from rebuild seller cron

### [2.135.0] - 2019-11-04

#### Added

* Aggregation field in doory indexing
* toggle to disable doory product indexing

### [2.134.0] - 2019-10-30

#### Fixed

* fixing merge from omnilogic when metadata is none
* applying title to offer_title on metabooks
* changing matching notification to sqs notification

### [2.133.0] - 2019-10-23

#### Changed

* removing delete from medias
* removing ze (gis) cron
* removing ze implementation from product indexing

### [2.132.0] - 2019-10-18

#### Fixed

* add exception to fix bug in the flow of unpublish products

#### Changed

* using notification class in product rebuild
* removing iteration from stores to record at mongo

### [2.131.0] - 2019-10-16

#### Changed

* removed `smallfiles` from docker-compose
* add cache on bazaarvoice script
* bazaar voice script improvements
* normalize html script improvements
* improve query execution time on catalog score endpoint
* running queries on big query for metrics creation in metric cron

#### Fixed

* products with attributes and without attributes matching through Omnilogic
Omnilogic
* fixed `ean` validation of bazaarvoice product cron

### [2.130.0] - 2019-10-02

#### Changed

* Send BazaarVoice XML to a bucket on GCP
* set fallback categories when category not found in datalake consumer

### [2.129.0] - 2019-09-30

#### Added

* Add tests

#### Fixed

* fix omnilogic matching from books
* fix bazaarvoice xml parser to always return navigation id
* fix image not found in metadata verify consumer
* fix download image from metadata input

#### Changed

* removing `stamp`, `product_click` and `sold_product` pollers
* removing `solr_suggestion`, `customer_behavior` and `buybox_peding` consumers
* matching from products with different eans

### [2.128.0] - 2019-09-16

#### Added

* create tests to increase test coverage

#### Changed

* changes to display two-day delivery

#### Fixed

* update product from the catalog when badge is removed
* correction in sending product categories to datalake
* notifying product type sns when a product receives enrichment

### [2.127.0] - 2019-09-11

#### Fixed

* sending product without ean to bazaar voice

### [2.127.0] - 2019-09-11

#### Fixed

* fix metadata is empty from enriched products scope

#### Added

* created a new route to receive a list of products to delete them

### [2.126.0] - 2019-09-10

#### Changed

* forcing source `omnilogic` and `metabooks` to get enriched product
* increasing test coverage
* rebuild improvements
* forcing string into value field when sending to datalake
* removing overlap of cron execution

#### Fixed

* fix memory leak in old images consumer

#### Added

* created command to delete keys on Redis
* creating script to normalize HTML descriptions

### [2.125.0] - 2019-09-05

#### Added

* implement ipdv jwt token generator

### [2.124.1] - 2019-09-05

#### Changed

* Changed BazaarVoice full script to import products by seller

#### Fixed

* Fixed some xml validations of cron bazaarvoice
* Fixed `express_delivery_scrapping` method name and tests
* Fix update delivery days in collection

#### Added

* creating script to get 3p products without image

### [2.124.0] - 2019-09-03

#### Added

* create Google PubSub Subscriber
* creating method for html sanitizer

#### Fixed

* forcing entity and category when does not exist in enriched_products

### [2.123.0] - 2019-08-30

#### Changed

* remove sonar login from file

#### Added

* blocking and notifying overlap of cron execution
* script to score missing products

### [2.122.0] - 2019-08-29

#### Fixed

* sorting attributes on unit test
* fix cron name in makefile

#### Changed

* send datalake `navigation_id` with 9 digits when numeric
* changing cron `express-delivery-scrapper` execution to every two hours
* adding delivery and pickup store in product_writer consumer
* changing product query for check `strCodigo` in selection from product poller

#### Added

* add `stock_count` field on `complete_product` consumer

### [2.121.0] - 2019-08-27

#### Added

* adding delivery flags in doory search attributes
* create iPDV postback consumer
* creating BazaarVoice full script for product importation
* implement storepickup crontab

#### Changed

* saving `delivery_plus_1` or `delivery_plus_2` in unified object from matching
* saving `store_pickup_available` in unified object from matching
* express delivery scrapper cron improvements

#### Fixed

* fix pipeline failure
* fixed file extension and some mongodb queries for BazaarVoice crontab
* sending old images of the magazineluiza to GCS

### [2.120.0] - 2019-08-24

#### Added

* Add cron bazaarvoice calls implementation
* create storepickup checker crontab structure
* creating `api_luiza_pickupstore` merge scope
* create `APILuiza` pickup stores http client
* creating `express_delivery_scrapper` crontab

#### Fixed

* Mock arcoiro call in solr_indexing converter test
* forcing 3 decimal places in product dimensions

#### Changed

* set delivery plus 1 or delivery plus 2 in raw products from merge

### [2.119.0] - 2019-08-19

#### Added

* implement bazaar voice brands xml for crontab
* remove subtitle from metabooks merge
* creating file upload to BazaarVoice FTP
* creating XML creator for product for bazaarvoice crontab

#### Changed

* changing sqs settings from rebuild marvin

### [2.118.0] - 2019-08-15

#### Added

* creating XML creator for category for bazaarvoice crontab
* add crons in Makefile
* Allow simple quote `'` special character on product title

### [2.117.0] - 2019-08-14

#### Changed

* Allow `%` character in title
* notify catalog SNS on media consumer

#### Added

* added new scope from media on datalake
* Add endpoint for rebuild metabooks
* creating bazaar voice products crontab basic structure

### [2.116.1] - 2019-08-13

#### Changed

* changing mongodb host sandbox
* changing redis host and password sandbox
* change log level when request doory-indexer to get custom scores

### [2.116.0] - 2019-08-12

#### Fixed

* implement DELETE action for unpublish model

#### Added

* added more logs to the inactivate inactive seller products flow

#### Changed

* Updated scripts/resend_datalake.py to contemplate media
* send product to indexing stream with default category when missing

#### Fixed

* removing hash hyphen from metabooks

### [2.115.0] - 2019-08-06

#### Changed

* script resend datalake improvements
* removing consumer s3 calls from doory and linx consumers

#### Fixed

* Fixed inactive_seller_products to not inactive a seller when the method return an exception

### [2.114.1] - 2019-08-02

#### Changed

* apply slugify metadata to not send spaces and special characters
* Fix doory indexer env variable
* Remove value for sandbox and production

### [2.114.0] - 2019-08-01

#### Added

* Add verification to remove last two zeros from navigation_id when we will unpublish products
* create rebuild endpoint to send catalog notification

#### Changed

* Add navigation_id filter to unpublish product listing endpoint
* changing `rewind` to `list` in product writer consumer

### [2.113.1] - 2019-07-31

#### Fixed

* Fix on inactivate_seller_products/seller.py when we try to get helena token

#### Added

* Created .yaml file for inactive products of inactive sellers cron

### [2.113.0] - 2019-07-29

#### Changed

* change datalake product scope send schema

### [2.112.1] - 2019-07-25

#### Added

* Retrieve custom scores in product indexing

### [2.112.0] - 2019-07-24

#### Added

* Create crontab to inactivate products of inactive sellers
* Create new endpoint to rebuild marvin's sellers

### [2.111.0] - 2019-07-19

#### Added

* creating class request `seller` data on `Helena`

#### Fixed

* set default value if key does not exist

### [2.110.0] - 2019-07-15

#### Changed

* use categories from product when categories not found
* removing publish docs from gitlab ci
* returning only sku and seller id when score and enriched product does not exist

#### Fixed

* fix storage exception error in complete product consumer
* fix problem in uploading images to GCP

### [2.109.0] - 2019-07-10

#### Changed

* raising error exception when it is not possible to download image from metabooks
* removing old consumer from stamp
* removing s3 usage from consumers

#### Fixed

* fix product score scope from datalake consumer

### [2.108.0] - 2019-07-05

#### Changed

* Add `*` and `@` characters in title
* changing topic name from enriched product consumer
* notifying matching through consumer metabooks verification
* remove solr deploy command
* getting mongo product when it does not exist in storage
* limiting number of records returned by single matching query

### [2.107.0] - 2019-07-03

#### Changed

* getting products by isbn that should be notified to the metadata verify
* removing sending to sqs in consumer price
* looking only for products that have isbn in metadata verify
* datalake improvements
* notifying SNS when there is a product score

#### Added

* adding `price` datalake scope
* adding disable_cache_lock property in sqs broker
* getting attributes from ean products
* adding `task_id` in put sqs from product quarantine
* adding `product_average_rating` and `product_total_review_count` to datalake's product scope

### [2.106.0] - 2019-06-26

#### Added

* adding `product_score` datalake scope
* script to resend scopes to datalake SQS queue
* create product scope for datalake

#### Changing

* adding message attributes to send message from sns
* removing category restriction to update categories of db0
* adding category `LI` from metabooks flow

### [2.105.0] - 2019-06-24

#### Changed

* changing consumer from metaverify to check by sku and seller_id
* removing sending to sqs in consumer product
* removing sending to sqs in merge class
* adding inventory condition greater than zero in product query
* changing order of when the frajola is called
* removing product report by category
* removing solr commands from Makefile
* group products by attribute size
* removing canonicalIds before update/add

#### Added

* adding the task_id and origin fields in the sns notification
* creating consumer for update categories in db0 (by Frajola)
* creating Google PubSub Manager
* creating datalake consumer
* adding the word `livro` in title from metabooks
* adding `enriched_product` datalake scope
* adding book products metrics

### [2.104.0] - 2019-06-18

#### Changed

* update methods that remove or fix HTML tags

### Added

* notifying complete product queue on factsheet consumer
* creating taz-api swagger

### [2.103.0] - 2019-06-11

#### Changed

* changing report produtos from all sellers
* removed allowed categories from doory consumer
* Save dimensions from image on mongodb

#### Added

* create version 0.2.0 of score

### [2.102.1] - 2019-06-04

#### Changed

* changing doory elasticsearch document from `product` and `suggestion` to `_doc`
* updating elasticsearch sandbox URL
* enable report products for all categories
* adding log to doory product indexer

### [2.102.0] - 2019-06-04

#### Changed

* remove `rewind` e use `list` in prices returning
* get ibsn from metabooks with ean
* find products from ean and isbn fields
* enabling categories to send to the gis

#### Added

* adding distribution products by score version metric

### [2.101.0] - 2019-05-30

#### Added

* adding report products from crontab
* adding log for ze call
* implementing sentry
* creating media active poller
* adding report multimedia in cron
* add sku count on score handler
* Scoring products that have not being enriched

#### Fixed

* correction in the query to obtain md5 of the existing product score
* update product when active in delete method
* fix url product fron report products

#### Changed

* set CAFE subcategory for ze test
* remove check active categories from product quarantine
* remove temporary category from product quarantine

### [2.100.0] - 2019-05-21

#### Added

* adding gis call in doory

### [2.99.1] - 2019-05-15

#### Changed

* Removing lookup use and getting categories descriptions from the categories collection

### [2.99.0] - 2019-05-10

#### Fixed

* category aggregation for general and seller score

#### Added

* create seller score endpoint
* creating full catalog score endpoint
* create category score endpoint

#### Changed

* remove `mock` dependency
* mock stock http client for test
* notifying the product score through the merge class
* remove product score notification fron product consumer

#### Fixed

* fix filename images from metabooks
* fix skip notification from crontabs
* fix merge default entity and specific entity from product score
* fix md5 generation site for the product score

### [2.98.0] - 2019-05-06

#### Fixed

* applying slugfy on seller to upload images
* fix none in name criterias and value for reviews
* correcting the writing of criteria to score criteria
* update prometheus client dependency
* improvements in the metrics endpoint
* sending magazine products from category books to SQS of images
* changing payload sent to ze queue
* change `ProductScoreHandler` to only find score in collection

#### Added

* adding new metrics in cron to expose through prometheus
* creating "ze" (gis) crontab
* implementing cron property to not notify in slack
* publish documention from gitlab-ci

#### Changed

* correcting the writing of criteria to score criteria
* update prometheus client dependency
* improvements in the metrics endpoint
* sending magazine products from category books to SQS of images
* changing payload sent to ze queue
* changing `scores` to `score_points`
* refactoring score flow
* increasing expiration time in gitlab-ci

### [2.97.0] - 2019-04-15

#### Changed

* improve gitlab ci file
* changing update to update_many in product consumer

#### Added

* creation class to obtain weights of the criteria by entity
* create score weight endpoint

### [2.96.0] - 2019-04-11

#### Added

* entity list endpoint
* create product by ean endpoint
* created score class for save points in mongodb
* create criteria endpoints
* added sonarqube in project

#### Changed

* changing product score consumer to call calculate score

### [2.95.0] - 2019-04-05

##### Added

* creating `product_score` consumer

#### Changed

* removing deploy command from taz-consumer-product-review consumer
* creating notification of product score SQS on product consumer

#### Added

* create rebuild `product_score` by sku endpoint
* create rebuild `product_score` by sku
* create rebuild `product_score` by seller
* create rebuild `product_score` by seller endpoint

### [2.94.1] - 2019-03-29

#### Changed

* updated main_category in merge class

### [2.94.0] - 2019-03-25

#### Changed

* maintaining the value of ean even when isbn
* improvements in metabooks categorization flow

### [2.93.0] - 2019-03-20

#### Added

* creating script for importing csv from metabooks categories
* added metabooks categories endpoint from import categories

#### Fixed

* forcing the blank subtitle does not exist

#### Changed

* applying magazineluiza categorization in enrichment by metabooks

### [2.92.0] - 2019-03-15

#### Changed

* improvements in metabooks flow

#### Added

* sending raw_products payload to google storage
* created script to send from raw_products to storage
* frajola api implementation

### [2.91.0] - 2019-03-12

#### Changed

* remove logentries
* download and save images from metabooks in the bucket
* reading bucket images from metabooks images

#### Fixed

* correction in enrichment flow of metabooks
* fix name and value format in bazaar voice review cron

### [2.90.0] - 2019-03-06

#### Fixed

* fix on method call to mount payload

#### Added

* slack notification when crontab run
* creating cron for importing bazaar voice reviews

### [2.89.0] - 2019-02-28

#### Changed

* using original product information to sent in the complete product
* changing product poller for import temporary products
* to use omnilogic enrichment when there is no metabooks for books
* notify sqs when an image is processed
* on base_price poller retrieve bundle info if exists
* changing mongo connectionstring for use mongos in k8s
* on query of base_price poller, certify that the product is active

### [2.88.0] - 2019-02-22

#### Changed

* support saving different sources in the enriched product consumer
* merge refactoring creating partner scopes

#### Fixed

* ignoring message when there is no json file in the flow of metadata veriry

#### Added

* create metabooks scope for merge
* removing brand regex in query from matching
* sending factsheet to acme stream in factsheet merger

### [2.87.0] - 2019-02-18

#### Added

* create metabooks ftp crontab
* created script for initial import of metabooks
* create metadata verify consumer

#### Changed

* getting d-1 files in metabooks
* changed `/enriched_products` endpoint to return result in list
* changing path for save metabook payload

### [2.86.0] - 2019-02-07

#### Added

* create metabooks input consumer
* added validate isbn method
* added SQS notify to metadata verify queue on product consumer
* sending product enrichment to the SNS

#### Changed

* changed product consumer to write ISBN in correct field
* changing deploy-all-consumer command in Makefile

#### Fixed

* fixed int in chunk_size from media consumer

### [2.85.0] - 2019-02-04

#### Fixed

* correction on the display name of the factsheet

#### Changed

* sending factsheet to acme stream
* returning product activation from poller
* convert active product in disable_on_matching from product consumer
* allow gemco_id null as value 0 on query base_price poller
* remove `blnAtivo` from `tabSetor` in pollers

#### Added

* created script to send factsheet to acme

### [2.84.4] - 2019-01-21

#### Changed

* setting the number of workers to 8

### [2.84.3] - 2019-01-15

#### Fixed

* removing validity and activation of bundles in product query
* do not import temporary products in product query
* linx indexing for 7 digit products

#### Changed

* altering the amount of consumer workers not to get through instance cores
* dependencie version for bleach upgraded to 2.1.4
* remove `blnAtivo` from tabSetor in price campaign poller
* changing endpoint from medias

#### Added

* create cron for rebuild sellers

### [2.84.2] - 2018-12-18

#### Changed

* returning products and prices not active and without stock but that are in the period of registry of the last 90 days

### [2.84.1] - 2018-12-17

#### Fixed

* fixing linx product delete

### [2.84.0] - 2018-12-13

#### Changed

* removing unnecessary logs
* rounding dimension values to 3 decimal places
* changing endpoint from integracommerce
* update hamilton version
* changing factsheet_parser to use FACTSHEET_DOMAIN

#### Added

* added FACTSHEET_DOMAIN key in settings

### [2.83.0] - 2018-12-12

#### Fixed

* fix not to cut alphanumeric IDs
* removing code from lost category in code

#### Changed

* sending the same product information without image to the SNS
* get produto from navigation_id in complete product consumer
* change poller name from "pricing" to "base_price"
* increasing number of characters to custom attributes
* improvement in logging when you do not have the grouping of products with the same parent

### [2.82.2] - 2018-12-04

#### Changed

* changing log level from queue broker
* removing the lognit logs

#### Fixed

* start metrics only when api
* fixing linx product payload
* send default installment plans for product to linx when missing
* setting product doory info from available variation

### [2.82.1] - 2018-11-16

#### Fixed

* changing delete workflow on linx to send multiple deletes whenever a variation exists on current stream message

### [2.82.0] - 2018-11-12

#### Changed

* changing `price` and `price_campaign` to use preco_cache new

### [2.81.1] - 2018-11-07

#### Fixed

* delete method for linx indexing

#### Added

* added dependency file in project

#### Changed

* enabling new categories to use enrichment in the doory consumer

### [2.81.0] - 2018-11-06

#### Changed

* remove merge categories

### [2.80.0] - 2018-11-05

#### Changed

* doory consumer `enriched_parser` to use `navigation_filters` attributes in factsheet
* factsheet merger to use `technical_specification` attributes in factsheet

#### Added

* create `deploy-all-consumers` command in Makefile
* added settings file from solr master gcp 1

#### Fixed

* correction on the object used in the method to clear the title

### [2.79.0] - 2018-10-31

#### Changed

* update requirements

### [2.78.0] - 2018-10-31

#### Changed

* raising bad request exception when json error occurs in kinesis
* sending factsheet consumer data to google

#### Fixed

* `partner` poller query return ordened and batck_key should be a string on converter to be compared
* remove duplicated subcategories in category merger class
* set single seller strategy when product has no `product_hash`

### [2.77.2] - 2018-10-17

#### Added

* `custom_attributes` index to mongodb_indexes script

#### Fixed

* remove `unique_with` parameter from CustomAttributes model

### [2.77.1] - 2018-10-17

#### Changed

* change order parameters on get custom_attribute to respect collection index

### [2.77.0] - 2018-10-17

#### Added
* integration to add suggestions based on user typed terms

#### Fixed

* validating empty facts before building attributes

#### Changed

* adding absolute clicks and quantities values in product indexer
* adding and changing settings from gcp migration
* changing p52 hostname

### [2.76.0] - 2018-10-16

#### Changed

* sending SQS message in "Cartaz de Loja" save/update
* send `short_title` and `short_description` in variation to Stream


### [2.74.0] - 2018-10-09

#### Changed
* considering category and type of spec to group variation on doory indexer
* considering category and type of spec to group variation on linx indexer

### [2.73.0] - 2018-10-02

#### Added

* create storage class for google cloud
* create poller to `partner`

#### Changed

* sending media consumer data to google

### [2.72.0] - 2018-09-28

#### Changed

* enable categories ED, EP, IN, AU, MO, AR to use rich data

#### Fixed

* fix attribute name validation

### [2.71.3] - 2018-09-27

#### Fixed

* validating attributes before building indexable facts

### [2.71.2] - 2018-09-27

#### Fixed

* indexed url for linx processor
* skipping 7 digit products on product indexing list

#### Changed

* skipping image when it is not possible to download

### [2.71.1] - 2018-09-25

#### Fixed

* fix changelog
* dealing with versions conflicts of elasticsearch delete action
* consume review score from data instead self

### [2.71.0] - 2018-09-24

#### Added

* adding key to disabled price lock
* improvement in delete log in Doory

#### Changed

* removing category restriction from doory consumer
* changing values for voltage normalization
* revert of removing category restriction from doory consumer
* re-matching when product has no variations

### [2.70.1] - 2018-09-19

#### Changed

* enabling TE for filter normalization

### [2.70.0] - 2018-09-18

#### Added

* adding rules for generation of alphanumerical IDs

#### Changed

* set omnilogic source when source not exist

### [2.69.0] - 2018-09-17

#### Changed

* use categories and subcategories from product in solr converter
* use enriched_products in doory consumer

### [2.68.0] - 2018-09-14

#### Changed

* do not crop id to no specs products on linx indexer

### [2.67.0] - 2018-09-14

#### Fixed

* fix specs aggregation on linx indexer
* Mock arcoiro request in Solr Converter
* fix factsheet parser attribute/value id generator to use slug

#### Changed

* setting subcategory_path to linx indexer
* do not crop id to group skus on linx indexer

### [2.66.1] - 2018-09-13

#### Changed

* save category merge in raw_products

### [2.66.0] - 2018-09-12

#### Fixed

* refactoring solr_index to improve performance
* Mock external dependencies in unit tests

#### Added

* endpoint get for enriched products

#### Changed

* accepting merge with more than one category
* keep product in quarantine if category and subcategory are missing or inactive

### [2.65.0] - 2018-09-10

#### Fixed

* exception correction when value is a repeated list in get ranker

### [2.64.0] - 2018-09-07

#### Added

* implement custom scores

### [2.63.0] - 2018-09-05

#### Fixed

* linx product indexer apply correct sku info

### [2.62.1] - 2018-09-04

#### Fixed

* added try/except from get ranker in solr converter

### [2.62.0] - 2018-09-03

#### Changed

* linx product indexer assembles variations on by linx specs

#### Fixed

* exception correction when value is a list in get ranker

### [2.61.1] - 2018-08-28

#### Added

* adding new range of product IDs

### [2.61.0] - 2018-08-28

#### Fixed

* added wait_time for pricing poller in production settings

#### Added

* catalog integrations documentation
* parametrized solr boosts

### [2.60.4] - 2018-08-22

#### Changed

* allowing the `/metrics` access without a token
* adding app name in `/metrics` return

#### Fixed

* does not overwrite product `attributes` when there is no `sku_metadata`

### [2.60.2] - 2018-08-17

#### Changed

* changing display name and slug in factsheet merge
* remove convert log in price_campaign poller

#### Fixed

* changing location of instantiating prometheus in API

### [2.60.1] - 2018-08-16

#### Fixed

* fix delete action in linx product indexer

### [2.60.0] - 2018-08-15

#### Changed

* exception correction when review values is none
* endpoint to get catalog metrics

### [2.59.0] - 2018-08-13

#### Added

* script for export categories
* create metrics crontab

#### Changed

* changed pricing query for reducing records
* Remove request on apigee at pricing poller, and added gemco_id to stream
* Adding voltage and id withou crop in solr document
* send payload product with delete action to SNS

### [2.58.0] - 2018-08-09

#### Added

* product indexer to linx search

#### Changed

* adding `canonical_ids` by variation
* using navigation_id to find the product when it receives the enrichment

#### Fixed

* fix get badge detail

### [2.57.0] - 2018-08-07

#### Changed

* renew integracommerce token if receives unauthorized response
* Remove raise from pricing poller that shutdown the poller

### [2.56.0] - 2018-08-06

#### Changed

* Dont save price on mongo when price/stock are missing

### [2.55.1] - 2018-08-03

#### Changed

* disable price lock

#### Added

* added `show_all` querystring parameter from badge list

### [2.55.0] - 2018-08-02

#### Changed

* changed stream name from product_sold_quantity in production settings
* corrections to deploy the project on teresa
* using metadata and subcategory_ids information even when there is no product_hash
* Dont save price on mongo when price/stock are missing

#### Removed

* relevant terms and dependent algorithms

### [2.54.0] - 2018-08-02

#### Added

* sending message timestamp to acme kinesis stream
* sending image to acme kinesis stream

#### Changed

* Dont raise not found exceptions on pricing poller

### [2.53.0] - 2018-08-01

#### Added

* added pricing poller to retrieve list price from database, and cost price from apigee

### [2.52.1] - 2018-07-31

#### Changed

* fixing load metadata to factsheet

### [2.52.0] - 2018-07-31

#### Added

* Mysql connector

#### Changed

* customer behavior is used for 3p and 1p products (not only 3 as it was previously)
* polling sold amounts by product from p52

### [2.51.0] - 2018-07-26

#### Added

* enriching brands and attributes of products without product_hash

#### Changed

* general changes to deploy consumer

### [2.50.0] - 2018-07-25

#### Changed

* execute matcher on threadpool

### [2.49.0] - 2018-07-24

#### Changed

* changed mongodb for suport more hosts
* use product brand field from variation as a priority. If not, use facts
* update project dependencies

### [2.48.0] - 2018-07-18

#### Added

* call factsheet merger in product merger
* call factsheet merger in factsheet consumer

### [2.47.0] - 2018-07-12

#### Added

* added lock product by price update
* create script for remove duplicated unified_objects
* configuring taz-api to run on teresa

#### Changed

* product without image is not added to the items for recording on redis
* remove sleep from media download
* using inactive product information from magazineluiza to omnilogic

### [2.46.0] - 2018-07-11

#### Fixed

* correction on the return of the current badges

#### Changed

* save slug badge in cache from badge consumer
* improvement logs from product consumer

### [2.45.7] - 2018-07-04

#### Fixed

* fix sending product payload to merge notification

#### Changed

* removing multi parameter in update from product and price consumer
* sending all variations to be removed from solr

#### Added

* Added log info on Converter price_campaign scope poller

### [2.45.6] - 2018-07-02

#### Changed

* adding offer_title in update product

#### Fixed

* leave from run processor when shard is locked

### [2.45.5] - 2018-06-28

#### Changed

* include validation on payload to price lock
* adding sleep between attempts to get the images
* log payload of price when there is exception in the consumer of price

### [2.45.4] - 2018-06-26

#### Changed

* increase max clients for semaphore in babel and integra consumer
* adding logs for product identification without images
* REVERT - changing product query to verify that the parent product is active

### [2.45.3] - 2018-06-25

#### Changed

* changing product query to verify that the parent product is active

### [2.45.2] - 2018-06-19

#### Changed

* changing title merge rule to always keep title of magazineluiza
* changing single-seller query to consider subcategory rather than category

### [2.45.1] - 2018-06-19

#### Added

* added log with `product_hash` in merge class

#### Changed

* added `multi` parameter in update price and product consumer


### [2.45.0] - 2018-06-18

#### Fixed

* fix null title after passing through merge class

#### Added

* endpoint to create price locks by seller
* added more logs in media consumer

#### Fixed

* using 'get' method to access dict info about 'created' and 'updated' date
* fix validation of scopes allowed in rebuild

### [2.44.2] - 2018-06-13

#### Added

* added elastisearch host in production settings

#### Fixed

* fix exception when product_name is null)

#### Changed

* cleaning up search vendors that will not be used

### [2.44.1] - 2018-06-12

#### Changed

* adding sku and seller information in media log

### [2.44.0] - 2018-06-07

#### Changed

* bucket name rollback of settings

#### Added

* adding verification method to blacklist in product consumer

### [2.43.0] - 2018-06-06

#### Fixed

* correction in the name of the media and factsheet bucket

#### Added

* added `offer_title` e `product_hash` in raw_products

#### Changed

* sending `offer_title` and `product_hash` fields in complete product
* save `product_hash` in merger class

### [2.42.0] - 2018-06-04

#### Fixed

* fix api rebuild to send payload to sqs
* fixing poller tests
* correction in stream processing loop

#### Changed

* changed bucket name for media and factsheet consumer
* not applying rule of title size when already owning source
* changed arcoiro endpoint

### [2.41.0] - 2018-05-30

#### Changed

* pointing pollers straight to google analytics api instead of intelie live backend
* removing validation by ean in grouping with omnilogic

### [2.40.0] - 2018-05-28

#### Fixed

* considering the reference in the title rule for magazine

#### Changed

* increase max_clients for semaphore
* solr consumer improvements

#### Added

* seller list endpoint

### [2.39.1] - 2018-05-24

#### Fixed

* correction for when to use omnilogic title clear the reference
* applying title size rule only for magazineluiza

### [2.39.0] - 2018-05-23

#### Fixed

* checking for records to process in kinesis boto
* unlock shard after stream break

#### Added

* category merge from omnilogic

#### Changed

* remove USE_MERGE key from merger class
* setting strategy in query when matching for omnilogic
* changed `insert` and `remove` to `update` in enriched product save

### [2.38.0] - 2018-05-22

#### Changed

* activating merge and matching by omnilogic

#### Added

* create test matching from omnilogic with `product_hash` is null

### [2.37.0] - 2018-05-18

#### Changed

* refactoring in rebuild consumer
* remove category and product list scopes from rebuild consumer
* changed rebuild endpoint to use rebuild consumer

### [2.36.0] - 2018-05-16

#### Added

* create omnilogic strategy for product matching
* create rebuild endpoint for reprocess products

#### Changed

* saving only the fields that were received in the payload in the price collection

### [2.35.0] - 2018-05-16

#### Changed

* changed insert to update in mongo collections for product and price consumer
* remove threads from shards in boto stream
* update requirements

### [2.34.1] - 2018-05-15

#### Changed

* correction in the product bucket key

### [2.34.0] - 2018-05-15

#### Added

* create script copy raw_products to products
* create script to send raw_products to s3
* create blacklist endpoint to create, delete and list
* create rebuild endpoint for reprocess a seller products

#### Changed

* remove products collection and use raw_products in merger class
* save raw product in s3 bucket from product consumer

### [2.33.0] - 2018-05-04

#### Changed

* changed `delete_many` to `remove` in product, merger and enriched_products

#### Added

* create script to resend products to complete product queue
* add more logs in enriched_products consumer

#### Fixed

* fix raw_products not found in enriched_products consumer

### [2.32.0] - 2018-05-03

#### Added

* created script to populate `products` collection
* merge class to join enriched_product to raw_product
* add semaphore to control babel requests in babel callback consumer
* add semaphore to control integracommerce requests in integracommerce callback consumer
* created `enriched_product` consumer

#### Changed

* product consumer to notify merge class instead of matching
* remove active flag in badge list

#### Fixed

* shardIterator when records is empty

### [2.31.0] - 2018-04-24

#### Fixed

* fixing customer behaviour pollers
* discarding product because not subcategories in complete product consumer

#### Added

* validation to verify if product is unpublished via admin
* endpoint to unpublish products

### [2.30.1] - 2018-04-20

#### Fixed

* correction of payload encode inserted in the queue
* increasing worker from media and factsheet consumer

### [2.30.0] - 2018-04-19

#### Changed

* removing KCL config files from migrated consumers
* changing chunk size for consumers with boto
* changed `remove` for `delete_one` in product consumer
* remove retry decorator in `_get_records` in stream class
* reducing calls in the kinesis stream
* enabling the 5x range for product code
* remove delete price from product consumer

### [2.29.0] - 2018-04-17

#### Changed

* Category and Integracommerce consumers to use BotoKinesis
* changed log level for required non empty field exception
* changing amount of threads in consumers with boto

### [2.28.0] - 2018-04-12

#### Fixed

* correction in product desmatching

#### Changed

* adding product url in complete product payload
* babel callback and buybox pending consumers to use BotoKinesis

### [2.27.0] - 2018-04-09

#### Fixed

* Factsheet and Badge consumers to use BotoKinesis

### [2.26.0] - 2018-04-05

#### Added

* create notification endpoint

### [2.25.0] - 2018-04-04

#### Fixed

* correction in image url to send to sqs from media consumer
* correction in delete action of complete product consumer
* fix verification only by seller, causing product lock in product_writer
* BotoKinesis improvements ro run multi thread.

#### Changed

* added sku and seller in log for variations unavalilable in product writer
* added exception in log error from solr indexing consumer
* added more logs in matching and product_writer consumer
* added `last_updated_at` in product
* considering categories in the generation of md5 in product consumer

### [2.24.0] - 2018-03-28

#### Changed

* added solr url in solr general exception

#### Added

* adding notification in the image queue in media consumer

### [2.23.0] - 2018-03-27

#### Fixed

* correction in format type when attributes is empty

#### Changed

* adding error log in sending to sns
* changed sns topic value in sandbox e production settings

### [2.22.0] - 2018-03-26

#### Changed

* removing payload submission from the recommendation queue through the complete product
* sending complete product notifications for SNS topic
* ignore arcoiro extra field
* sending product and price notification with payload specific for SNS topic
* increasing arcoiro timeout from 5s to 15s

#### Fixed

* fix to remove products from a badge that was duplicating the badge

### [2.21.1] - 2018-03-19

#### Fixed

* correction on return of active badges campaigns

### [2.21.0] - 2018-03-14

#### Changed

* removing matching by non-parent variation
* specific `sku` and `seller_id` required fields for delete in buybox pending consumer

#### Added

* added config for new solr master for solr indexing consumer

### [2.20.0] - 2018-03-12

#### Changed

* extending the amount of IDs behavior pollers can fetch
* matching refactoring and fix single seller matching

### [2.19.0] - 2018-03-08

#### Changed

* ignore exception in strip attributes when attribute name is invalid
* applying capitalize only in the field that is in uppercase
* changing log level of download image failure
* sending complete product payload to recommmedation product info queue
* added `navigation_id`, `price` and `list_price` in complete product payload

#### Added

* script for resend products in product writer queue

### [2.18.0] - 2018-03-05

#### Fixed

* removing products not sent for solr
* checking if the name field exists in the badges listing
* fix matching for product with same ean, withou attributes and different titles

### [2.17.0] - 2018-03-01

#### Changed

* remove duplicated products from solr indexing consumer
* treatment for product not found in the product review consumer
* returning message to review queue when values already exist in mongo

### [2.16.0] - 2018-02-27

#### Changed

* returning rule of magazineluiza winning at buybox

### [2.15.0] - 2018-02-26

#### Added

* create script for find is_html attribute in factsheet
* added `order` field in seller list

#### Changed

* added disable_on_matching in get buybox products
* exception handling when product not found

#### Fixed

* single matching same titles, attributes and seller
* fix save in collection for product and price consumer

### [2.14.0] - 2018-02-23

#### Added

* create get product navigation id endpoint
* Endpoint for remove matching
* added log error for strip_attributes_from_title method

#### Fixed

* single matching different products with same title and attributes

#### Changed

* changing logging level for some unused messages

### [2.13.0] - 2018-02-21

#### Changed

* added matching strategy in unified_objects collection
* Adding support to teresa to consumer of media
* Adding support to teresa to consumer of product quarantine

#### Added

* Check vulnerabilities for dependencies on CI
* create endpoints for buybox list

#### Fixed

* Fixed ungroup products with differents attributes and same titles

### [2.12.1] - 2018-02-20

#### Fixed

* encoding product payload in buybox pending consumer
* get stream_name method on BotoKinesis

### [2.12.0] - 2018-02-20

#### Changed

* BotoConsumer to get stream_name according to scope
* added message success in queue broker
* adjustment in single matching to group products with different parents

#### Fixed

* fix on md5 generation of product for skip of update
* correction product buybox winning in detail but not exhibiting in the showcase

### [2.11.0] - 2018-02-15

#### changed

* customer_behavior and price consumer to use BotoKinesisBroker

### [2.10.0] - 2018-02-06

#### Changed

* adding score to magazine to win on price ordering when impacted
* product consumer notify complete product queue
* remove pending_products from product consumer
* discarding product when already exists in pending product

#### Added

* create buybox pending consumer
* create product complete consumer

### [2.10.0] - 2018-02-06

#### Changed

* disabling all sellers for buybox

#### Added

* new kinesis record processor to replace kcl lib

### [2.9.0] - 2018-01-29

#### Changed

* removing rule of magazineluiza always winning
* enabling all sellers for matching
* adding canonical_ids that belong to the same inactive product

### [2.8.2] - 2018-01-10

#### Changed

* hamilton version update
* review consumer log enhancements
* media consumer log enhancements
* save empty payload for product in redis for diff

### [2.8.1] - 2018-01-09

#### Changed

* remove force product in solr consumer when not found in solr read
* changed script for resend product by id
* fix not to cut batch_key in five digits when is_batch off
* removing inventory check in media query

### [2.8.0] - 2017-12-19

#### Added

* set brand in reference when it has the title
* create script for resend showcase imagens in SQS
* create script for resend products by id
* added solr-cloud properties in solr indexing consumer

#### Changed

* removing 404 treatment for product review
* added checkout_price in query of the price poller

### [2.7.3] - 2017-12-06

#### Fixed

* correction to consider correct timezone in badges listing
* fix exception for when there is no skus on price verification

#### Changed

* changed log level for subcategory in product_writer consumer

### [2.7.2] - 2017-11-27

#### Added

* adding log in method `_verify_all_skus_have_prices` for exception identification
* create script for resend products in product_writer queue

#### Fixed

* exception correction when using forced product flow in solr consumer

### [2.7.1] - 2017-11-24

#### Changed

* setting price value when discount_price_200_0 does not exist

### [2.7.0] - 2017-11-22

#### Changed

* remove the `complete_description` and `text` fields in solr consumer

### [2.6.1] - 2017-11-15

#### Fixed

* fix on product force log on solr consumer

### [2.6.0] - 2017-11-15

#### Added

* validation to remove broken tags and normalize uppercase tags

#### Changed

* when the product does not exist in the solr read use payload information

#### Fixed

* removing product variations when it is voltage in solr consume

### [2.5.3] - 2017-11-14

#### Changed

* log enhancements for solr reading
* setting price value when cash_price_200_0 does not exist

### [2.5.2] - 2017-11-14

#### Changed

* changed log level for message in solr writer

### [2.5.1] - 2017-11-13

#### Fixed

* treatment for when cash_price does not exist in read solr

#### Added

* adding sku and product_id information in the log of the arcoiro

### [2.5.0] - 2017-11-07

#### Fixed

* correction in the type of action for notification of badges
* fields containing html tag

#### Added

* adding solr suggestion in production settings

### [2.4.1] - 2017-11-03

#### Fixed

* returning production log path configuration

### [2.4.0] - 2017-11-03

#### Fixed

* fix grouping by variation when products have the same parent with the attributes

#### Added

* create new consumer solr suggestion
* adding ids range starting with 6

### [2.3.0] - 2017-10-31

#### Fixed

* remove a product only when there are no variations and is inactive

#### Changed

* changing media query to consider unavailable products
* update readme with deploy instructions

### [2.2.5] - 2017-10-25

#### Added

* adding log information for product debug traceability

### [2.2.4] - 2017-10-24

#### Added

* redis with singleton pattern

#### Changed

* deleting only the different ids of variation and canonicals
* do not clean directories in old images consumer
* changed application name in old images stream properties
* changing log level to error 404 for integracommerce consumer

### [2.2.3] - 2017-10-24

#### Fixed

* customer behavior clicks quantity
* query correction for voltage products
* image_url update in badge API
* correcting product color with factsheet value and having no voltage

#### Added

* `Integra Commerce` product callback consumer implementation

#### Changed

* adding product_id in the mongo query to get reviews
* changing image script to read from a list of sellers
* added active querystring in badge poller
* removing validation to not add badge to product out of stock
* changes to save marketplace images directly on s3

### [2.2.2] - 2017-10-19

#### Fixed

* do not send delete notification for products with old_products that are single seller
* forcing `stores` attribute on all products in solr consumer
* duplicity of attributes in product poller
* modifying urls of images for lower case on solr consumer

### [2.2.1] - 2017-10-16

#### Added

* `Integra Commerce` product callback consumer implementation
* `Integra Commerce` refresh token implementation

#### Fixed

* fix `id_correlations` when there is ungrouping products
* fix `local variable 'req' referenced before assignment` in solr consumer
* correction in the log message on the badge consumer

#### Changed

* enabling to send produtos for kinesis stream
* adjustments in media and factsheet query to return products to store
* remove expires for badge consumer

#### Added

* script for image resending by seller
* method on category consumer to update babel categories

### [2.2.0] - 2017-10-09

#### Changed

* solr multi master indexing capabilities/mechanics (now it can only index one master per process, but the write url can be specified via env var)

#### Added

* badges and sellers info on Solr consumer
* added `priority` field in badges

#### Fixed

* correction in writing the word tooltip that was with _
* correction in the product query to obtain color information
* sorting `badges` by `priority` instead of `position`
* add field `origin` with module name to `product_writer` queue

### [2.1.0] - 2017-10-04

#### Changed

* changing product query to return color of factsheet
* removing perfume pollers
* removing product posting block for perfume

#### Added

* adding price values in the skip log

#### Fixed

* fix payload sent to product writer

### [2.0.1] - 2017-10-03

#### Fixed

* small adjustments in the publication of badges

#### Changed

* changes in badges endpoint

#### Added

* adding key to kinesis in production
* adding key to change publication flow

### [2.0.0] - 2017-09-27

#### Fixed

* minor fixes in fry

#### Added

* added `message_timestamp` to kinesis message
* send product to stream by product writer consumer

### [1.15.0] - 2017-09-26

#### Added

* get fry prices for all products

### [1.14.0] - 2017-09-25

#### Fixed

* do not send notification to kinesis when not downloading
* fix badge consumer and poller

#### Changed

* changing log level for consumer product

#### Added

* badge poller implementation
* adding badges on payload mounted on product writer
* get, delete, update and insert badge implementation
* added `release_date` in md5 method
* badge consumer implementation
* script to check if product exists in id_correlation collection
* added log in badge notify

### [1.13.22] - 2017-09-21

#### Changed

* increasing quantity of workers in solr consumer
* skip product and price update when payload already exists in mongo

#### Added

* script for updating review of marketplace
* created badges list endpoint

### [1.13.21] - 2017-09-19

#### Added

* force parameter to skip sqs delay
* adding request log in product consumer

#### Changed

* searching correlations through product and variation

### [1.13.20] - 2017-09-18

#### Changed

* changing title proximity weights to matching

### [1.13.19] - 2017-09-15

#### Fixed

* fix to remove from solr products through canonical ids

#### Changed

* adding sku and seller in the log to delete old_product_ids
* adding isnull to campaign code in price query

### [1.13.18] - 2017-09-13

#### Fixed

* not sending product delete for variations that start with the same product_id

#### Changed

* removing mongo remove call in product and price consumer
* add log when any exception is raised

#### Added

* adding log for when a product is unpublished on product_writer

### [1.13.17] - 2017-09-11

#### Changed

* not adding main product code in solr to delete
* increasing ngram in matching for buybox

#### Added

* attribute amount to product_scores collection
* script for remove matching for products

### [1.13.16] - 2017-09-04

#### Fixed

* fix matching for products without attributes
* correction in submitting review information to solr
* fix null sentences on matcher
* fix reviews on solr converter

#### Added

* saving info about image count on collection
* sending review information to solr
* adding quantity of product seller in solr
* increasing number of ranges 70, 71, 72 and 73
* adding allowed sellers for matching

#### Changed

* remove unused parameter for `_save_pending` function

### [1.13.15] - 2017-08-27

#### Fixed

* validating message and settings for product review

#### Added

* adding the main_media in each variation to get images
* script creation for media json rewriting

#### Changed

* capitalize product `title` and `reference` when is uppercase and marketplace
* create unit tests for capitalize product `title` and `reference` on update

### [1.13.14] - 2017-08-23

#### Fixed

* fix in review consumer

#### Added

* script to submit products to review queue

#### Changed

* use review data from `customer_behaviors` (from bazaar voice) collection
* creating collection to store data for scoring

### [1.13.13] - 2017-08-22

#### Added

* created endpoint to write review in sqs
* is_html attribute on factsheet consumer

#### Fixed

* skipping sold quantity attribution from customer behaviour whenever a product is from Magalu

#### Changed

* removing invalid characters `<` and `>`
* saving full payload of medias in json

### [1.13.12] - 2017-08-21

#### Added

* `customer behavior` clicks and sold quantities on Solr index file

#### Fixed

* correction to assemble variation categories in matching

#### Changed

* changing url from static content to not passing through cdn

### [1.13.11] - 2017-08-18

#### Fixed

* increasing datasheet query field to not truncate values

#### Changed

* assigning the main product variation
* limiting description field size allowed in solr

### [1.13.10] - 2017-08-14

#### Fixed

* fix on product type with attributes for marketplace
* buy-box match now have the same behavior indepedent of variation comparison sequence

### [1.13.9] - 2017-08-09

#### Changed

* changing payload sent to price campaign kinesis
* voltage group variations in solr convert

### [1.13.8] - 2017-08-08

#### Added

* validating video url on consumer product

### [1.13.7] - 2017-08-04

#### Changed

* removing invalidation from cloudfront for factsheet and media
* optimizing campaign price query

### [1.13.6] - 2017-08-02

#### Changed

* increasing product sold poller wating time
* changing grouping of selections for main product
* added cloudfront invalidate in factsheet consumer
* improvement in solr testing
* changing campaign price poller recording key

### [1.13.5] - 2017-07-27

### Changed

* increasing product click poller wating time
* removing writing in old solr
* changed solr master endpoint in sandbox

### [1.13.4] - 2017-07-26

#### Changed

* increasing endpoint max results
* removing aws credentials from settings

#### Fixed

* fix log file path in production settings

### [1.13.3] - 2017-07-21

#### Fixed

* fix does not group products with same parent and different attributes

#### Changed

* changed campaign price payload sent to stream
* added cloudfront invalidate in media consumer
* added console appender in production settings
* returning code to not send products without price

### [1.13.2] - 2017-07-20

#### Fixed

* correction in the factsheet query that did not return all information
* correction in exception missing message

#### Changed

* changed logging appender
* treatment to accept empty sellers in babel and elasticache consumer

### [1.13.1] - 2017-07-18

#### Changed

* fixing new solr master public address

#### Fixed

* remove invalidate cloudfront in factsheet consumer

### [1.13.0] - 2017-07-18

#### Added

* new solr master to taz solr indexing consumer
* create ngram algorithm for title/reference proximity for matching

### [1.12.1] - 2017-07-17

#### Fixed

* force float in log_processing_status method

#### Changed

* refactor `buybox` and `single seller` product matcher
* notify matching in product review consumer

### [1.12.0] - 2017-07-17

#### Added

* publication time logs to measure overall product publishing lead time
* create cloud front manager with invalidation method
* Log on stream process_record to apply on Intelie
* create cloudfront manager with invalidation method

#### Changed

* update requirements
* added cloudfront invalidate in factsheet consumer
* save json file with list of images in media consumer
* applying slug in sku to save media
* changing the price save from update_one to update

#### Fixed

* correction in the query to set the main variation
* correction to publish product that does not have a price record
* correction not to record different media of status code 200
* fix exception in media consumer

### [1.11.3] - 2017-07-07

#### Added

* sending notification to `price-monitor` on price updates
* adding script that fixes/forces a matching strategy to all related skus

#### Fixed

* fixing matching bug for non exclusive strategy

### [1.11.2] - 2017-07-05

#### Added

* creating consumer for customer behavior data

#### Changed

* changed flow of price deletion
* changed endpoint for count in api
* added wait_time in settings for new pollers

#### Added

* adding log for when you can not find any id to get product in unified_objects

#### Added

* adding script that forces/fixes a matching strategy on a product and all its related skus

### [1.11.1] - 2017-06-28

#### Changed

* upgraded pymongo to 3.4.0
* upgraded mongoengine to 0.13.0
* increased batch from 100 to 500 (to fit expected capacity on kinesis consumed bytes metric)
* decreased idle time between messages to throttle up consumer capacity
* removed new solr master to avoid log misinterpretation

### [1.11.0] - 2017-06-26

#### Fixed

* Fix `Product Clicks Poller` missing implementations

#### Added

* sending callback to babel even in delete actions
* retries on solr indexing process
* created endpoint to return product counts
* adding ranges 74, 75, 76 and 77 to our ID ranges

#### Changed

* change of name in consumer and settings
* decreasing kinesis batches length in order to ease total consumed bytes metrics (product indexing)

### [1.10.0] - 2017-06-20

#### Added

* create poller for product clicks quantity
* unit tests for API Poller
* unit tests for `MsSqlDataStorage`
* unit tests for `APIDataStorage`
* review consumer implementation
* creating fixture to clear redis cache
* adding image unavailable for variations when it does not have media
* create poller for product sold quantity

#### Changed

* changing message log level for image download attempts
* changing log level for error in logentries
* specifying payment method for request in arcoiro
* importing only temporary active products

### [1.9.2] - 2017-06-13

#### Fixed

* fix on writing ids in id_correlations by writing the id of the product itself

#### Added

* adding categories and selections in variation
* added log processing time in arcoiro request

#### Changed

* removing pending flow on updates after product is approved on matching

### [1.9.1] - 2017-06-12

#### Added

* new solr master to settings file (production)

#### Fixed

* fix of a bug that happened when a disabled product was being processed

### [1.9.0] - 2017-06-08

#### Fixed

* fix missing poller exception message from `KinesisBroker`

#### Added

* created new poller for campaign prices
* created tests for stream broker inside poller context
* adding import of images and factsheet for temporary products
* adding log on consumer price
* adding error in sqlserver log

#### Changed

* disabling matching sellers
* discarding consumer of prices with campaign code
* changing log level on consumer solr
* increasing price difference tolerance to 50% for buybox product cut rules

### [1.8.3] - 2017-06-06

#### Changed

* removing default campaign verification
* removed query for partner pricing
* consumer queue log improvement
* changing order actions in solr consumer

#### Added

* campaign price validation for magazineluiza products

#### Fixed

* Correction of the `disable_on_matching field loss after matching approval

### [1.8.2] - 2017-06-01

#### Added

* create http status constants
* added `fragrance` in product specification
* timeout tolerance to rebuild queries/cursors

#### Fixed

* correction in the query that returned two records but only 1 was expected
* fix default campaign code in price consumer

#### Changed

* log improvements in product model for api
* returning attributes in matching endpoint

### [1.8.1] - 2017-05-31

#### Added

* create function to format `id`(product, variation) to `solr_id`
* added ranges 78, 79, 80 and 81 for product ids

#### Changed

* save only prices campaign prices
* move sort operations from `Poller` to mixin
* move diff operations from `Poller` to mixin
* change in the order of verification of the stock type in the poller

#### Fixed

* move sort operations from `Poller` to mixin

### [1.8.0] - 2017-05-30

* changed price consumer and poller
* changing poller inheritance
* refactor `_transform_subcategory` function
* ordering the elements of the factsheet

### [1.7.26] - 2017-05-29

#### Added

* adding poller for epoca cosmeticos
* enabling whirlpool for buybox

### [1.7.25] - 2017-05-25

#### Added

* added log for product consumer
* decoupling sqlserver strict logics to a specialized package/module

#### Fixed

* fix lint and added link in circle ci
* fix save category inactive

### [1.7.24] - 2017-05-16

#### Fixed

* fix for products that have only one category

### [1.7.23] - 2017-05-16

#### Added

* adding main_category for correct category ordering

#### Changed

* added assert in test expression
* improve search_facets match

#### Fixed

* fix product query for gift

### [1.7.22] - 2017-05-10

#### Added

* enabling matching for `epocacosmeticos` and `casaamerica`

### [1.7.21] - 2017-05-03

#### Added

* keeping local cache of s3 files

#### Changed

* forcing EAN as string to check digits
* remove item of search_facets using sherlock configs
* deleting old product when matching assembles a buybox one

#### Fixed

* compatibility in media payloads

### [1.7.20] - 2017-04-25

#### Added

* 82 and 83 new ranges

#### Changed

* crowdflower improvements
* scripting easier ways to run consumers/pollers
* refactoring way to get ean code
* changing redis endpoint

### [1.7.19] - 2017-04-12

#### Changed

* fix empty url image for media consumer

### [1.7.18] - 2017-04-11

#### Fixed

* fix access denied in s3 for docs

#### Changed

* relevant terms extraction
* adding new range for product id and more logs

### [1.7.17] - 2017-04-07

#### Fixed

* fix clowdflower script

#### Changed

* circle ci s3 upload
* remove skip md5 in media consumer

#### Created

* create script for clean unified objects

### [1.7.16] - 2017-03-31

#### Fixed

* fix title, reference and brand in elastic search

#### Changed

* change blnAtivo for blnAvise_me in querys

### [1.7.15] - 2017-03-30

#### Changed

* Smaller search facets (checking attribute value length and denying facetability in negative cases)
* added and fix isort in project
* adding title, reference, brand and descripton in variation

#### Added

* adding circle and remove travis

### [1.7.14] - 2017-03-28

#### Added

* adding bundles and gift in matching product

#### Changed

* returning information from bundle and gift in poller
* refactoring save_pending in product consumer  and pending handler

### [1.7.13] - 2017-03-23

#### Fixed

* fixing fact checks

#### Changed

* save relevant information for product when pending moderation

### [1.7.12] - 2017-03-23

#### Fixed

* validating fact attributes

### [1.7.11] - 2017-03-23

#### Fixed

* fix save product

### [1.7.10] - 2017-03-23

#### Added

* adding log for send images to ftp
* create script clowdflower
* populate canonical_ids in solr

#### Changed

* changing log level from logentries to warning

#### Fixed

* fix ordering product variation by availability
* fix to save moderation products that are not on the whitelist
* fixing factsheet grouping and exhibition

### [1.7.9] - 2017-03-21

#### Added

* added sns manager

#### Changed

* remove product in quarantine when disable on matching is true

### [1.7.8] - 2017-03-17

#### Fixed

* minor fixes in product_writer and match_product

### [1.7.7] - 2017-03-17

#### Changed

* remove canonicals for marketplace products
* ordering product variation by availability
* remove skip save in price

#### Fixed

* fixing product_id bug on product_writer

#### Added

* adding seller_composite_name for sending es payload

### [1.7.6] - 2017-03-15

#### Fixed

* fix last_updated_at in price consumer

#### Changed

* remove has_product_change validate

### [1.7.5] - 2017-03-15

#### Changed

* added nolock querys in price and stamp
* added disable_on_matching in product change validate

#### Fixed

* fix script for adding pending products

### [1.7.4] - 2017-03-13

#### Fixed

* fix detail ids append canonicals in solr
* checking id existence before updating
* fix exception in elegible products
* fix sold count

#### Changed

* update readme

### [1.7.3] - 2017-03-10

#### Fixed

* fix approve pending products

### [1.7.2] - 2017-03-10

#### Fixed

* minor general fixes

#### Changed

* change in time between poller and sqs runs
* increasing time to obtain best sellers information

### [1.7.1] - 2017-03-09

#### Fixed

* fixing none ean bug

### [1.7.0] - 2017-03-09

#### Added

* script to add pending products as eligible buybox

#### Changed

* new id attribution mechanics

### [1.6.10] - 2017-03-09

#### Changed

* remove raise exception in delete pending product
* returning price and media in product api
* notify matcher when approve pending product
* returning media information in the matching api

#### Added

* added navigation_id when not found in id_correlations

### [1.6.9] - 2017-03-03

#### Added

* added origin in rebuild scopes
* added seller_slug in solr

### [1.6.8] - 2017-03-02

#### Fixed

* fix product consumer when rebuild product

### [1.6.7] - 2017-03-02

#### Added

* script for update navigation_id in raw_products
* script for clean unified objects

#### Changed

* update simple_settings (necessary to install requirements)
* sending to matching only when product change is relevant

### [1.6.6] - 2017-02-22

#### Changed

* limiting id generation retries and enabling logentries

### [1.6.5] - 2017-02-22

#### Fixed

* fix delete product in es

#### Changed

* added ids in production settings

### [1.6.4] - 2017-02-21

#### Fixed

* fix sells to company in product writer

### [1.6.3] - 2017-02-21

#### Changed

* changing image validation and adding id 88 and 89
* generation id when matching test

#### Added

* validating if there is change in the product that influences the matching
* added sells_to_company in product_writer

### [1.6.2] - 2017-02-20

#### Changed

* added 90 new range for matching

### [1.6.1] - 2017-02-20

#### Fixed

* fix error unified_object reference before assignment
* correction on return of product selections

#### Changed

* refactoring pending products and delete pending product after approval
* check md5 for media payload
* product pending handler refactoring

#### Added

* implementing multi master writing capabilities on solr_index consumer
* added new index create in doc

### [1.6.0] - 2017-02-15

#### Added

* implementing pending products workflow
* pending products list implementation
* added get and list methods for product handler
* added get pending product
* apply matching strategy implementation
* added pending sellers endpoint
* adding api documentation
* adding product information on matching return
* create token command
* moderating all products on sandbox env
* added new fields in models
* parametrizing strategies

#### Changed

* moving matching strategy decision (from matcher to product consumer) amongst other minor changes
* added data in response
* changing inheritance of models to dynamic

#### Fixed

* fix test consumer
* removing useless code
* moving matching strategy decision (from matcher to product consumer) amongst other minor changes
* validating that a ID is not None before adding it to canonicals
* fix messages and added test for pending products

### [1.5.17] - 2017-02-07

#### Added

* added gunicorn in base requirements

#### Fixed

* fix get strategy

### [1.5.16] - 2017-02-07

#### Fixed

* fix sells_to_company in auto buybox strategy

### [1.5.15] - 2017-02-07

#### Fixed

* fixed log message and fix exception on sells_to_company

#### Changed

* write empty when product has no description

#### Added

* added test matching endpoint

### [1.5.14] - 2017-02-07

#### Changed

* restructuring matching
* save sells_to_company in unified_ojects
* changed healthcheck for added version and host

#### Added

* added script for update disabled on matching in raw_products
* access log middleware implementation
* added sell_to_company in product consumer
* added version middleware

### [1.5.13] - 2017-02-02

#### Fixed

* fix on availability status

#### Changed

* standardizing assembler implementations

#### Added

* added authorization middleware

### [1.5.12] - 2017-02-01

#### Fixed

* fix to standardize error log

#### Added

* added api implementation
* exposing matching without saving it
* token implementation
* added base handler
* logging out of stock items

#### Changed

* rename apis for api
* equal to where the product query and price

### [1.5.11] - 2017-01-24

#### Changed

* changing consumer solr to read by variation

### [1.5.10] - 2017-01-19

#### Changed

* changing how IDs and deduplications are handled so they won't happen again

### [1.5.9] - 2017-01-19

#### Fixed

* deduplicating sellers on assembler

### [1.5.8] - 2017-01-18

#### Changed

* changing query to fetch products in Solr

### [1.5.7] - 2017-01-18

#### Changed

* assuring that one variation has only one price per item

### [1.5.6] - 2017-01-17

#### Changed

* sorting images only for magazineluiza
* using upsert to save the price

### [1.5.5] - 2017-01-17

#### Added

* added log in solr consumer

#### Fixed

* fixing single product bug for duplicated variation on same seller items

### [1.5.4] - 2017-01-17

#### Fixed

* fixing same seller repetition bug (on buybox)
* fix ordering images
* fixing id bug

#### Changed

* disabled stamp in production
* clearing logs sent to logentries
* remove variations for mkp products

### [1.5.3] - 2017-01-12

#### Changed

* changed elastic search settings

### [1.5.2] - 2017-01-12

#### Fixed

* remove variations delete in solr consumer

### [1.5.1] - 2017-01-12

#### Fixed

* fix generate canonical method in solr consumer

### [1.5.0] - 2017-01-12

#### Addded

* added `sellers_count` in elastic search
* buybox implementation

#### Changed

* improving docstring over buybox composition
* changed maxrecords for 600 in indexing processing stream

### [1.4.18] - 2017-01-05

#### Changed

* revert "remove sqs start delay"

### [1.4.17] - 2017-01-05

#### Changed

* remove sqs start delay
* enable stamp

### [1.4.16] - 2016-12-23

#### Changed

* remove lower the seller in solr consumer

### [1.4.15] - 2016-12-21

#### Fixed

* fix mongo duplicate key in product consumer
* fix factsheet convert

### [1.4.14] - 2016-12-19

#### Fixed

* fix media query
* fix attributes for factsheet query

#### Added

* added slug in attributes from factsheet

#### Changed

* price consumer refactoring
* invalid characters and html for mkp products and enable multiprocess

### [1.4.13] - 2016-12-14

#### Changed

* change structure from factsheet payload

### [1.4.12] - 2016-12-12

#### Changed

* enable send images for ftp in sandbox
* disable logentries em sandbox
* changed log level for warning in production

#### Fixed

* fix delivery availability in variations

### [1.4.11] - 2016-12-12

#### Changed

* changed logentries token in sandbox settings

#### Fixed

* fix to remove marketplace product

### [1.4.10] - 2016-12-08

#### Changed

* removing stock validation for one
* copy object for remove fields

### [1.4.9] - 2016-12-08

#### Added

* added dns for sql server
* enable task backoff time millis in stream properties

#### Changed

* remove updated_at and created_at in md5 hash
* changed stamp for redis

### [1.4.8] - 2016-12-06

#### Fixed

* fix md5 json not serializable

#### Changed

* forcing value 1 in stock when greater than zero
* skip md5 verification when rebuild

### [1.4.7] - 2016-12-05

#### Fixed

* fixing product save on raw_products
* treatment to verify that the product exists in rebuild product list

#### Added

* enabled kinesis multiprocess and changed stream properties
* added and check md5 for product and price

#### Changed

* send delete when product does not exist in solr reader

### [1.4.6] - 2016-11-28

#### Changed

* added nolock in product query
* remove delete in save product
* changed log type and added expires in lock cache

#### Added

* parallel record processors

### [1.4.5] - 2016-11-26

#### Added

* adding information in the consumer log

#### Changed

* changed log type for media success in poller
* fix url variation
* forcing seller id to be lowercase on solr document
* remove get stamp in mongo

#### Fixed

* fixed stock count price poller

### [1.4.4] - 2016-11-17

#### Changed

* adjusting the ratio of stamp
* remove multiprocess stamp

### [1.4.3] - 2016-11-16

#### Changed

* changing ids sent to elasticsearch
* changes consumer and poller stamp
* added created_at and removed is_new_product
* changed stamp flow

#### Added

* escaping character

### [1.4.2] - 2016-11-10

#### Changed

* sorted atributes for products
* changed stream name and s3 bucket for stamp consumer

### [1.4.1] - 2016-11-08

#### Added

* added is_devilery_available in variations
* added allowed html tags
* added exception in delete record es

#### Changed

* remove solr reader exception
* changing nationwide stock criteria

### [1.4.0] - 2016-11-04

#### Added

* create stamp consumer

#### Changed

* changed selection id in stamp query
* returning exception when not find record in solr

#### Fixed

* fix and refactoring in rebuild

### [1.3.1] - 2016-11-01

#### Fix

* fix exception in item of the factsheet in the solr

#### Changed

* changed sandbox and production kinesis properties

### [1.3.0] - 2016-11-01

#### Added

* added url in variation
* adding new allowed characters
* create stamp poller

#### Fixed

* changing the ES payload to avoid duplications
* correction to generate different ids in elements of the factsheet
* fix consumer old images
* fix clean documents in solr exception

#### Changed

* changed warning for debug in cache locks
* refactoring scopes in rebuild

### [1.2.0] - 2016-10-26

#### Added

* added bumpversion and changelog in project
* Old Magazine Luiza Images consumer
* added https in arcoiro settings
* add scope `product_by_list` in rebuild scopes

#### Changed

* add `price` and `list_price` as "Required non empty field" in price consumer

### [1.1.1] - 2016-10-21

#### Added

* added delay queue in product_writer SQS

#### Fixed

* sold out and specification in solr consumer

### [1.1.0] - 2016-10-20

#### Changed

* specifying fields to delete product
* allowing new characteres to no break html
* change ID from babel callback

#### Fixed

* sorted attributes in root products
* duplicated magazineluiza products


### [1.0.0] - 2016-10-19

* First release
