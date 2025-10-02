#!/bin/bash

USER_NAME="sk000"

kubectl create configmap ${USER_NAME}-myfirst-configmap \
  --from-file=application-prod.yaml \
  --namespace=skala-practice

