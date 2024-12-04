STATEMENT = """
select SUBSTRING(CONVERT(varchar(10), id), 1, 2)  as batch_key, id, strdescricao from tabparceiro order by 1, 2
"""
