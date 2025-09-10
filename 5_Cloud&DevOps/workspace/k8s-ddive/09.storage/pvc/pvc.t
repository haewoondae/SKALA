apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: efs-${SERVICE_NAME}
  namespace: ${NAMESPACE}
spec:
  accessModes:
    - ReadWriteMany
  volumeMode: Filesystem
  resources:
    requests:
      storage: 100Mi
  volumeName: efs-${SERVICE_NAME}

