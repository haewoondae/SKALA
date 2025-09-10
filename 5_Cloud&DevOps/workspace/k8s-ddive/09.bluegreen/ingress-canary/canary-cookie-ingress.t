apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/canary: "true"
    nginx.ingress.kubernetes.io/canary-by-cookie: "canary-session"
  name: ${USER_NAME}-cm-tls-canary-ingress
  namespace: ${NAMESPACE}
spec:
  ingressClassName: public-nginx
  rules:
  - host: ${USER_NAME}-tls.skala25a.project.skala-ai.com
    http:
      paths:
      - backend:
          service:
            name: ${USER_NAME}-green
            port:
              number: 8080
        path: /
        pathType: Prefix
  tls:
  - hosts:
    - ${USER_NAME}-tls.skala25a.project.skala-ai.com
    secretName: ${USER_NAME}-cm-auto-tls-secret
