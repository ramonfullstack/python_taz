# V1 não está retornando nenhum produto

Threads: https://luizalabs.slack.com/archives/G1K7JJQL9/p1533734434000375
https://luizalabs.slack.com/archives/C1Y0WBTH8/p1533732769000225

## Passos para identificação do problema

1. Ao tentar consultar um produto na V1, confirmou-se que não estava retornando produtos;
2. O próximo passo foi verificar se os produtos existem no `Solr`;
3. Em um primeiro momento, imaginou-se que foi por conta de uma configuração no `xml` no campo `original_id`, pois o mesmo deveria ser `required` `False` do Solr:

    Antes:
```xml
        <field name="original_id" type="string" indexed="true" required="true" stored="true"/>
```
   Depois:
```xml
       <field name="original_id" type="string" indexed="true" required="false" stored="true"/>
```

4. Porém, mesmo ao realizar essa configuração, o problema ainda persistia.

5. Por fim, foi necessário reiniciar a máquina que roda a `v1` (172.19.90.53) em sandbox.

## Solução

Foi necessário dar um restart na V1 em sandbox (máquina `172.19.90.53`) acessando via SSH e executando o comando `sudo service tomcat7 restart`.

Porém, também seria possível fazer um `restart` da máquina no console da AWS utilizando a conta `mlresearch`.