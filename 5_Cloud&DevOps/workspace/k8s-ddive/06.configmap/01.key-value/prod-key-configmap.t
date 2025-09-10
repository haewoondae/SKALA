# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: prod-db-config
data:
  database.url: jdbc:mysql://localhost:3306/production-db
  database.user: productor
  database.password: productor

