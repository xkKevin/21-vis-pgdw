{{/*
the name of configmap
*/}}
{{- define "pgdw-app.configmap.name" -}}
{{ include "pgdw-app.fullname" . }}-config
{{- end }}