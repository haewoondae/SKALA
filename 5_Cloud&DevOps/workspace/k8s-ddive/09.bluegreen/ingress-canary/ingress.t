apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
  name: ${USER_NAME}-cm-tls-ingress
  namespace: ${NAMESPACE}
spec:
  ingressClassName: public-nginx
  rules:
  - host: ${USER_NAME}-tls.skala25a.project.skala-ai.com
    http:
      paths:
      - backend:
          service:
            name: ${USER_NAME}-blue
            port:
              number: 8080
        path: /
        pathType: Prefix
  tls:
  - hosts:
    - ${USER_NAME}-tls.skala25a.project.skala-ai.com
    secretName: ${USER_NAME}-cm-auto-tls-secret
