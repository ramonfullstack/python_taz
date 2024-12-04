## Métricas de Catálogo

### Obter métricas de catálogo

Retorna métricas coletadas do catálogo para serem utilizadas
pelo Prometheus

    GET /metrics
    

**Exemplo de requisição**

```
curl http://localhost:5000/metrics/?token=TOKEN \
-X GET
```

**Exemplo de resposta**

```
    # HELP process_virtual_memory_bytes Virtual memory size in bytes.
    # TYPE process_virtual_memory_bytes gauge
    process_virtual_memory_bytes 472629248.0
    # HELP process_resident_memory_bytes Resident memory size in bytes.
    # TYPE process_resident_memory_bytes gauge
    process_resident_memory_bytes 42065920.0
    # HELP process_start_time_seconds Start time of the process since unix epoch in seconds.
    # TYPE process_start_time_seconds gauge
    process_start_time_seconds 1534193317.26
    # HELP process_cpu_seconds_total Total user and system CPU time spent in seconds.
    # TYPE process_cpu_seconds_total counter
    process_cpu_seconds_total 0.73
    # HELP process_open_fds Number of open file descriptors.
    # TYPE process_open_fds gauge
    process_open_fds 15.0
    # HELP process_max_fds Maximum number of open file descriptors.
    # TYPE process_max_fds gauge
    process_max_fds 1048576.0
    # HELP python_info Python platform information
    # TYPE python_info gauge
    python_info{implementation="CPython",major="3",minor="6",patchlevel="4",version="3.6.4"} 1.0
    # HELP Total Entities Total Entities
    # TYPE Total Entities summary
    total_entities 1.0
    # HELP Total Sellers Total Sellers
    # TYPE Total Sellers summary
    total_sellers 123.0
    # HELP Inactive Sellers Inactive Sellers
    # TYPE Inactive Sellers summary
    inactive_sellers 25.0
    # HELP Active Sellers Active Sellers
    # TYPE Active Sellers summary
    active_sellers 98.0
```

**Códigos de retorno**

| Código | Descrição |
|---|---|
| 200 | Sucesso |
| 401 | Não autorizado |

