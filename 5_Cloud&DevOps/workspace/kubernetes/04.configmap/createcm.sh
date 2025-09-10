#!/bin/bash

USER_NAME="sk003"

kubectl create configmap ${USER_NAME}-myfirst-configmap \
  --from-file=application-prod.yaml \d
  --namespace=skala-practice

