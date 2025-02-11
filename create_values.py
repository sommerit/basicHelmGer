#!/usr/bin/env python3
import os

def ask(question, default=None):
    """
    Stellt eine Frage und gibt den Standardwert zurück, wenn keine Eingabe erfolgt.
    """
    if default is not None:
        prompt = f"{question} [{default}]: "
    else:
        prompt = f"{question}: "
    answer = input(prompt)
    if answer.strip() == "" and default is not None:
        return default
    return answer

def main():
    print("Dieses Tool erstellt interaktiv eine 'values.yaml'-Datei für dein Helm Chart.\n")
    
    # Grundlegende Parameter
    replicaCount = ask("Anzahl der Replikate", "3")
    image_repository = ask("Docker-Image Repository", "nginx")
    image_pullPolicy = ask("Image Pull Policy (Always, IfNotPresent, Never)", "IfNotPresent")
    image_tag = ask("Docker-Image Tag", "latest")
    service_type = ask("Service Typ (ClusterIP, NodePort, LoadBalancer)", "ClusterIP")
    service_port = ask("Service Port", "80")
    
    # Vault Integration
    vault_enabled_input = ask("Vault Integration aktivieren? (ja/nein)", "nein")
    vault_enabled = vault_enabled_input.strip().lower() in ["ja", "y", "yes"]
    if vault_enabled:
        vault_role = ask("Vault Rolle", "my-vault-role")
        vault_secretPath = ask("Vault secretPath", "secret/data/myapp/config")
        print("Für das Vault Template kannst du eine Standardvorlage verwenden.")
        vault_template = ask("Vault Template (optional)", '{{- with secret "secret/data/myapp/config" -}}\n{{ .Data.data | toJSON }}\n{{- end }}')
    else:
        vault_role = ""
        vault_secretPath = ""
        vault_template = ""
    
    # Formatiere das Vault Template außerhalb des f-Strings
    vault_template_formatted = vault_template.replace("\n", "\n    ") if vault_enabled else ""
    
    # ConfigMap
    configmap_enabled_input = ask("Soll eine ConfigMap erstellt werden? (ja/nein)", "nein")
    configmap_enabled = configmap_enabled_input.strip().lower() in ["ja", "y", "yes"]
    configmap_data = {}
    if configmap_enabled:
        print("Gib Key-Value-Paare für die ConfigMap ein. Drücke ENTER (ohne Eingabe), um zu beenden.")
        while True:
            key = input("ConfigMap Schlüssel (ENTER zum Beenden): ")
            if key.strip() == "":
                break
            value = input(f"Wert für '{key}': ")
            configmap_data[key] = value
    
    # Ingress
    ingress_enabled_input = ask("Ingress konfigurieren? (ja/nein)", "nein")
    ingress_enabled = ingress_enabled_input.strip().lower() in ["ja", "y", "yes"]
    if ingress_enabled:
        ingress_className = ask("Ingress Class Name (optional)", "")
        print("Definiere Ingress Hosts. Drücke ENTER, um das Hinzufügen zu beenden.")
        ingress_hosts = []
        while True:
            host = input("Ingress Host (z.B. example.com) (ENTER zum Beenden): ")
            if host.strip() == "":
                break
            path = ask("Pfad für diesen Host", "/")
            pathType = ask("Path Type (z.B. Prefix, ImplementationSpecific)", "ImplementationSpecific")
            ingress_hosts.append({
                "host": host,
                "paths": [
                    {
                        "path": path,
                        "pathType": pathType
                    }
                ]
            })
        ingress_tls = []  # TLS-Konfiguration kann hier ergänzt werden
    else:
        ingress_className = ""
        ingress_hosts = []
        ingress_tls = []
    
    # Erstelle den Inhalt für values.yaml in mehreren Schritten
    values_yaml = f"""# Auto-generiertes values.yaml

replicaCount: {replicaCount}

image:
  repository: {image_repository}
  pullPolicy: {image_pullPolicy}
  tag: {image_tag}

service:
  type: {service_type}
  port: {service_port}

resources: {{}}

vault:
  enabled: {str(vault_enabled).lower()}
  role: "{vault_role}"
  secretPath: "{vault_secretPath}"
  template: |
    {vault_template_formatted}
"""
    # Konfiguriere den ConfigMap-Block
    values_yaml += "\nconfigmap:\n  enabled: " + str(configmap_enabled).lower() + "\n  data:"
    if configmap_enabled and configmap_data:
        for key, value in configmap_data.items():
            replaced_value = value.replace("\n", "\n    ")
            values_yaml += f"\n  {key}: |-\n    {replaced_value}"
    else:
        values_yaml += " {}"
    
    # Konfiguriere den Ingress-Block
    values_yaml += f"""\n
ingress:
  enabled: {str(ingress_enabled).lower()}
  className: "{ingress_className}"
  annotations: {{}}
  hosts:"""
    if ingress_enabled and ingress_hosts:
        for host in ingress_hosts:
            values_yaml += f"\n    - host: {host['host']}\n      paths:"
            for path in host["paths"]:
                values_yaml += f"\n        - path: {path['path']}\n          pathType: {path['pathType']}"
    else:
        values_yaml += "\n    []"
    values_yaml += "\n  tls: []\n"
    
    # Schreibe die Datei
    with open("values.yaml", "w", encoding="utf-8") as f:
        f.write(values_yaml)
    
    print("\nDie Datei 'values.yaml' wurde erfolgreich erstellt.")

if __name__ == "__main__":
    main()
