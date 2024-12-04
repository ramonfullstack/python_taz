# Produtos de seller sem imagem

## Problema

Produto publicado não está exibindo imagem no site (aparece a imagem indisponível).

## Passos para identificação/depuração do problema

1. Obter o sku de um produto pelo external_id (external id pode ser obtido na página de detalhe do produto).

2. Buscar no banco do Babel na tabela product_variations pelo external_id e pegar o campo sku.

3. Acessar o logentries (no app babel-worker) para buscar por seller e sku da seguinte forma: sku & seller 

4. Verificar no logentries se os dados foram enviados para o Kinesis Stream (taz-media) 

5. Em último caso, acesse o painel da integra e verifique como a imagem está.

**Observação:** 

P/acessar o seller no painel da integra, é necessário o nome do seller e uma senha que algumas vezes é padrão:

Usuário Integra: nome do seller
senha: (solicitar à alguém do @squad-catalogo)

Para acesso à réplica do banco de dados Babel, peça no canal #firefighting