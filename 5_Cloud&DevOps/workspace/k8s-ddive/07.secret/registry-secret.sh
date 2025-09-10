#!/bin/bash

DOCKER_REGISTRY="https://amdp-registry.skala-ai.com/skala25a"
DOCKER_REGISTRY_USER="robot\$skala25a"
DOCKER_REGISTRY_PASSWORD="1qB9cyusbNComZPHAdjNIFWinf52xaBJ"

kubectl create secret docker-registry harbor-registry-secret \
  --docker-server=${DOCKER_REGISTRY} \
  --docker-username=${DOCKER_REGISTRY_USER} \
  --docker-password=${DOCKER_REGISTRY_PASSWORD}

