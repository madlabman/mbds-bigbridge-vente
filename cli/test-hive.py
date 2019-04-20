from pyhive import hive

cursor = hive.connect(host='hive-server', port=10000).cursor()
cursor.execute('SELECT * FROM pokes LIMIT 10')

print(cursor.fetchall())
