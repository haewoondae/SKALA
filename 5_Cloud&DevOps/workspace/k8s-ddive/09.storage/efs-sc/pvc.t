apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: ${USER_NAME}-efs-sc-${SERVICE_NAME}
  namespace: ${NAMESPACE}
spec:
  accessModes:
    - ReadWriteMany
  volumeMode: Filesystem
  resources:
    requests:
      storage: 100Mi
  storageClassName: efs-sc-shared

