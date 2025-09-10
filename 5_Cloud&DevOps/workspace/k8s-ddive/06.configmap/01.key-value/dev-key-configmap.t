apiVersion: v1
kind: ConfigMap
metadata:
  name: dev-db-config
data:
  database.url: jdbc:mysql://localhost:3306/develop-db
  database.user: developer
  database.password: developer

