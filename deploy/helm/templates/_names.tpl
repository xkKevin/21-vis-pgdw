{{/*
the name of configmap
*/}}
{{- define "somnus-app.configmap.name" -}}
{{ include "somnus-app.fullname" . }}-config
{{- end }}

{{/*
the name of frontend.deployment
*/}}
{{- define "somnus-app.frontend.deployment.name" -}}
{{ include "somnus-app.fullname" . }}-frontend
{{- end }}

{{/*
the name of backend.deployment
*/}}
{{- define "somnus-app.backend.deployment.name" -}}
{{ include "somnus-app.fullname" . }}-backend
{{- end }}

{{/*
the name of morpheus.deployment
*/}}
{{- define "somnus-app.morpheus.deployment.name" -}}
{{ include "somnus-app.fullname" . }}-morpheus
{{- end }}

{{/*
frontend labels
*/}}
{{- define "somnus-app.frontend.labels" -}}
{{ include "somnus-app.labels" . }}
app.part: frontend
{{- end }}

{{/*
backend labels
*/}}
{{- define "somnus-app.backend.labels" -}}
{{ include "somnus-app.labels" . }}
app.part: backend
{{- end }}

{{/*
morpheus labels
*/}}
{{- define "somnus-app.morpheus.labels" -}}
{{ include "somnus-app.labels" . }}
app.part: morpheus
{{- end }}

{{/*
frontend selector labels
*/}}
{{- define "somnus-app.frontend.selectorLabels" -}}
{{ include "somnus-app.selectorLabels" . }}
app.part: frontend
{{- end }}

{{/*
backend selector labels
*/}}
{{- define "somnus-app.backend.selectorLabels" -}}
{{ include "somnus-app.selectorLabels" . }}
app.part: backend
{{- end }}

{{/*
morpheus selector labels
*/}}
{{- define "somnus-app.morpheus.selectorLabels" -}}
{{ include "somnus-app.selectorLabels" . }}
app.part: morpheus
{{- end }}

{{/*
backend service name
*/}}
{{- define "somnus-app.service.backend" -}}
{{ include "somnus-app.fullname" . }}-backend
{{- end }}

{{/*
morpheus service name
*/}}
{{- define "somnus-app.service.morpheus" -}}
{{ include "somnus-app.fullname" . }}-morpheus
{{- end }}
