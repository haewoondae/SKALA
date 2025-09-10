apiVersion: v1
kind: Service
metadata:
  name: ${USER_NAME}-my-app-service-proxy
  namespace: gateway
spec:
  type: ExternalName
  externalName: skala-stock-ui.skala-edu.svc.cluster.local
  ports:
    - port: 8080

