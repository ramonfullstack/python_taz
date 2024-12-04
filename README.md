# Taz  
![](https://s-media-cache-ak0.pinimg.com/736x/90/b3/41/90b341d801706c3d998e4265c87d6c57.jpg)

O Taz é responsável por pré-processar e publicar produtos no [ACME](https://github.com/luizalabs/acme). Ele é composto por uma série de workers assíncronos especializados por escopo de informação (produto, mídias, precificação e ficha técnica).

Especificamente, as premissas do Taz são:  

* Ingestão, análise, classificação e unificação de produtos de múltiplos lojistas  
* Processamento de imagens e ficha técnica  
* Ingestão de produtos legado do Magazine Luiza

## Documentação

URL: [http://luizalabs-docs.s3-website-us-east-1.amazonaws.com/taz/](http://luizalabs-docs.s3-website-us-east-1.amazonaws.com/taz/)
[draw.io](https://app.diagrams.net/#G1i6cUbBak8pjXJ4BL8FWe2w805Z_NYIAw)
[swagger](http://taz-api.magazineluiza.com.br/docs/)
[confluence](https://magazine.atlassian.net/wiki/spaces/CAT/pages/2327740542/Aplica+o+do+Taz)


## Instalação

1.  Instalação das dependências:

- Mac OSX

```
brew install mongodb python3 redis-server memcached tmux
```

- Ubuntu

```
apt-get install mongodb python3-dev redis-server memcached openjdk-8-jdk
```

2.  Criar um virtualenv:

        virtualenv taz -p python3

3.  Instalar dependências do Python, via `pip`:

        make requirements

### Observação Importante:
Caso utilize Mac e tenha problemas para instalar o `pymssql`, execute os seguintes passos:

    1.`brew unlink freetds`
    2.`brew install freetds@0.91`
    3.`brew link --force freetds@0.91`
    
No caso de usar Linux e ter problemas para instalar o `pymssql`, exporte a seguinte variável de ambiente:

    1.`export PYMSSQL_BUILD_WITH_BUNDLED_FREETDS=1`

Caso você tenha algum problema similar a esse `[Permission denied]: listdir('/path/taz/data/db/diagnostic.data',)` ao executar testes ou algo que utilize o mongo em seu projeto, de permissão de leitura, escrita e execução para a pasta `data`:

    1.`sudo chmod -R 777 data`

Caso ocorra o seguinte erro ao instalar as dependências (`make requirements`): `AttributeError: '_NamespacePath' object has no attribute 'sort'` , o problema está com a versão do seu `pip`/`setuptools` do Python. Para atualizá-los, basta executar os comandos abaixo:

`pip install --upgrade pip & pip install --upgrade setuptools`

Caso tenha o seguinte problema: `error in mongoengine setup command: use_2to3 is invalid.`

`pip install setuptools==56.0.0`

4.  Executar o projeto:

    3.1 Poller / Consumer

        make run
        
    3.2 API
    
        make run-api

Seguir o [padrão de commits](https://gitlab.luizalabs.com/luizalabs/ci-knife#commit-sem%C3%A2ntico)
        
## Executando os Testes

Para executar os testes do projeto:

    make test

Para executar testes especifícos do projeto:

    make test-matching Q=[alguma palavara ou nome de método ou classe]


Para executar a cobertura de testes no código:

    make coverage

## Execução

O Taz é dividido em três tipos de função:  

1. Pollers (coletam dados de uma fonte pré-definida)
2. Consumers (consome dados de um _stream_ ou de uma fila)
3. API (gerenciamento de informações do database)

### Poller e Consumer

Execute o comando:  

```
make run environment=ENVIRONMENT scope=SCOPE jobtype=JOB_TYPE
```

Onde:  

* **ENVIRONMENT** define qual configuração de ambiente será utilizada. Os valores suportados são `development`, `sandbox` e `production`;  

* **SCOPE** define qual escopo de informação o job cuidará. Os valores suportados são: `babel_product_callback`, `integracommerce_product_callback`, `elasticsearch_indexing`, `old_images`, `product`, `product_clicks_quantity`, `product_quarantine`, `product_review`, `product_sold_quantity`, `product_writer`, `rebuild`, `solr_indexing`, `solr_suggestion`, `factsheet`, `media`, `category`, `price`, `price_campaign`, `pricing`, `stamp`, `customer_behavior`, `partner`, `matching`, `badge` e `ipdv_product_postback`;

* **JOB_TYPE** define qual tipo de trabalho será executado. Os valores suportados são`poller` ou `consumer`  

Para verificar quais variáveis estão definidas em cada ambiente, dê uma olhada nos respectivos arquivos dentro do diretório `taz/settings`.

#### Executar todos os pollers em ambiente local

Para executar todos os pollers em ambiente local é necessário ter o `tmux` instalado.  
Após ter ele instalado, execute o comando:

```
make run-pollers-dev
```

Com isso, uma sessão do tmux será iniciada com o id `taz_consumers`;  

* Para conectar nesta sessão execute `tmux attach taz_consumers`.
* Para navegar entre as janelas dessa sessão pressione `ctrl b` e utilize as setas do seu teclado
* Para desconectar desta sessão e mantê-la rodando em background, pressione `ctrl b` e em seguida `d`
* Para desconectar desta sessão e interromper sua execução, interrompa os processos e dê `quit` em cada janela

#### Executar todos os consumers em ambiente local

Para executar todos os consumers em ambiente local é necessário ter o `tmux` instalado.  
Após ter ele instalado, execute o comando:

```
make run-consumers-dev
```

Com isso, uma sessão do tmux será iniciada com o id `taz_consumers`;  

* Para conectar nesta sessão execute `tmux attach taz_consumers`.
* Para navegar entre as janelas dessa sessão pressione `ctrl b` e utilize as setas do seu teclado
* Para desconectar desta sessão e mantê-la rodando em background, pressione `ctrl b` e em seguida `d`
* Para desconectar desta sessão e interromper sua execução, interrompa os processos e dê `quit` em cada janela


### API

Execute o comando: 

```
make run-api
```

## Deploy

Para efetuar o deploy do Taz (Consumers), utilizar o comando abaixo para deploy no Teresa

    make deploy-consumer scope=[scope] cluster=[cluster]

Para efetuar o deploy do Taz (API), utilizar o comando abaixo para deploy no Teresa

    make deploy-api cluster=[cluster]

Onde:

* **SCOPE** define qual escopo que será feito o deploy.
 
* **CLUSTER** define qual o ambiente que deseja publicar.  

Variavéis de ambiente:

* AWS\_ACCESS\_KEY\_ID 
* AWS\_SECRET\_ACCESS\_KEY
* JOB\_TYPE
* SCOPE

### Deploy Consumers e Cron em paralelo:

É possível rodar os deploys da cron/consumer em paralelo. Para isso, será necessário instalar o tmux:

Linux:
    `apt-get install tmux`

MacOS:
   `brew install tmux`

Executar os passos abaixo:

1. Colocar permissão de execução nos scripts para rodar os deploys das `crons` e `consumers` em paralelo.

```bash
      chmod +x run_parallel_consumer_deploys.sh
      chmod +x run_parallel_cron_deploys.sh
```

2. Rodar o tmux

```bash
tmux
```

3. Rodar o script

```bash
make deploy-all-consumer-parallel
```

```bash
make deploy-all-crons-parallel
```

4. Para acompanhar, será necessário conhecer alguns shortcuts do tmux:

O tmux trabalha com janelas e paineis. Como o deploy são em vários apps, precisou quebrar em janelas (windows). Cada janela equivale à um terminal.

Cada janela terá 4 painéis, ou seja, cada painel terá o deploy de uma aplicação. Um painel é um terminal quebrado em partes.

O número de janelas pode ser verificado na parte inferior do terminal.

Para trocar de janela:

CTRL + b + <nº janela> : Vai para o número de janela especificado.

Por exemplo, se quiser ir para a janela 0, bastar utilizar o atalho: Ctrl + b + 0

Para trocar de painel:

CTRL + b + ->  : Vai para o painel à direita;
CTRL + b + <-  : Vai para o painel à esquerda;

Para fechar um painel e o tmux:

CTRL + d


### Ambiente de homologação (Pollers)
Para atualizar o ambiente de homologação é necessário acesso via SSH, nas instâncias:
    172.19.90.46 (Poller)

### Instruções para deploys em produção

1. Certificar-se de que o branch master esteja atualizado (`git pull`).

2. Verificar se o CHANGELOG está correto.

3. Criar uma release nova: `make release-minor`, `make release-patch`, ou `make release-major`

4. Enviar as tags que foram criadas no processo acima para o Gitlab: `git push && git push --tag`

5. Criar solicitação de GMUD e esperar aprovação da mesma.

6. Quando a GMUD estiver aprovada, avisar no canal #producao sobre o deploy a ser realizado, colocando o link da GMUD e marcando o @squad-catalogo / @squad-pricing.

7. Rodar por meio dos comandos: 

* `make deploy-all-consumer cluster=[nome do cluster]` para os consumers;
* `make deploy-api cluster=[nome do cluster]` para a API.

8. Avisar na Thread (no aviso do passo 6) se o deploy foi sucedido ou teve rollback

9. Fechar a GMUD e adicionar a label `Deployed` se o deploy teve sucesso. Caso contrário, fechar e adicionar a label `Rollback`

## Monitoração

- Stackdriver (escolher o filtro do consumer no filtro `resource.labels.namespace_id`) - [https://console.cloud.google.com/logs/viewer?project=magalu-digital-project&organizationId=614831433169&minLogLevel=0&expandAll=false&timestamp=2019-08-12T17:59:21.303000000Z&customFacets=&limitCustomFacetWidth=true&dateRangeStart=2019-08-12T16:59:21.554Z&dateRangeEnd=2019-08-12T17:59:21.554Z&interval=PT1H&resource=container%2Fcluster_name%2Fgke-digital-navigation%2Fnamespace_id%2Fhotdogui-builder&scrollTimestamp=2019-07-29T14:11:39.525934959Z&advancedFilter=resource.type%3D%22container%22%0Aresource.labels.cluster_name%3D%22gke-digital-worker%22%0Aresource.labels.namespace_id%3D%22taz-consumer-product%22%0A](https://console.cloud.google.com/logs/viewer?project=magalu-digital-project&organizationId=614831433169&minLogLevel=0&expandAll=false&timestamp=2019-08-12T17:59:21.303000000Z&customFacets=&limitCustomFacetWidth=true&dateRangeStart=2019-08-12T16:59:21.554Z&dateRangeEnd=2019-08-12T17:59:21.554Z&interval=PT1H&resource=container%2Fcluster_name%2Fgke-digital-navigation%2Fnamespace_id%2Fhotdogui-builder&scrollTimestamp=2019-07-29T14:11:39.525934959Z&advancedFilter=resource.type%3D%22container%22%0Aresource.labels.cluster_name%3D%22gke-digital-worker%22%0Aresource.labels.namespace_id%3D%22taz-consumer-product%22%0A)

- [Grafana](https://grafana-catalogo.magazineluiza.com.br/dashboards/f/GZddw1TGz/catalogo?query=taz)
