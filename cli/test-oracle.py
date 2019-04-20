import cx_Oracle

con = cx_Oracle.connect(dsn='oracle:1521/orclcdb', user='sys', mode=cx_Oracle.SYSDBA, password='orclpa55')

print(con.version)

con.close()
