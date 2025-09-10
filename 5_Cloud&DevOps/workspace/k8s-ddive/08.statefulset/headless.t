apiVersion: v1
kind: Service
metadata:
  name: ${USER_NAME}-${SERVICE_NAME}-headless
  namespace: ${NAMESPACE}
spec:
  clusterIP: None
  selector:
    app: ${USER_NAME}-${SERVICE_NAME}
  ports:
    - name: http
      protocol: TCP
      port: ${CONTAINER_PORT}
      targetPort: ${CONTAINER_PORT}
    - name: mgmt
      protocol: TCP
      port: 8081
      targetPort: 8081

