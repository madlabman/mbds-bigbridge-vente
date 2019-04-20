from cassandra.cluster import Cluster

cluster = Cluster(['column'], port=9042)
session = cluster.connect()

print('Connected')
