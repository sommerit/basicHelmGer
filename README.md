# Basic Deployment Helm Chart

## Einleitung

Dieses Helm Chart dient als Beispiel für den Deployment einer grundlegenden Anwendung in Kubernetes. Das Chart bietet folgende Funktionen:

- **Vault-Integration als Sidecar:** Ermöglicht das Abrufen von Secrets via HashiCorp Vault.
- **Optionale ConfigMap:** Kann bei Bedarf konfiguriert werden.
- **Optionaler Ingress:** Ermöglicht den externen Zugriff auf die Anwendung.
- **Einfache Konfiguration:** Einige Parameter, wie `nodeSelector` und `tolerations`, sind fest vorgegeben und nicht konfigurierbar, um die Komplexität zu reduzieren.
