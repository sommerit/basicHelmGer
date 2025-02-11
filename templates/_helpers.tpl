{{/*
Helper-Templates für das Helm Chart.
Diese definieren wiederverwendbare Namen und Labels für die Ressourcen.
*/}}

{{- define "basic-deployment.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "basic-deployment.fullname" -}}
{{- if .Values.fullnameOverride -}}
  {{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- else -}}
  {{- $name := default .Chart.Name .Values.nameOverride -}}
  {{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}

{{- define "basic-deployment.labels" -}}
helm.sh/chart: {{ include "basic-deployment.chart" . }}
{{ include "basic-deployment.selectorLabels" . }}
{{- with .Chart.AppVersion }}
app.kubernetes.io/version: {{ . | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end -}}

{{- define "basic-deployment.selectorLabels" -}}
app.kubernetes.io/name: {{ include "basic-deployment.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}

{{- define "basic-deployment.chart" -}}
{{ .Chart.Name }}-{{ .Chart.Version }}
{{- end -}}
