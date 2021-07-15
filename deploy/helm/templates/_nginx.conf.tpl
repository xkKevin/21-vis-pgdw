{{- define "somnus-app.config.nginx.conf" -}}
server {
    listen       80;
    server_name  localhost;
    client_max_body_size 1000m;

    location ~ ^/backend {
        proxy_set_header HOST $host;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_connect_timeout 600;
        proxy_read_timeout 600;
        proxy_send_timeout 600;
        send_timeout 600;
        client_body_timeout 300;
        rewrite ^/backend/(.*) /$1 break;
        proxy_pass http://{{ include "somnus-app.service.backend" . }}:{{ $.Values.backend.port }};
    }

    location ~ ^/morpheus {
        proxy_set_header HOST $host;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_connect_timeout 600;
        proxy_read_timeout 600;
        proxy_send_timeout 600;
        send_timeout 600;
        client_body_timeout 300;
        rewrite ^/morpheus/(.*) /$1 break;
        proxy_pass http://{{ include "somnus-app.service.morpheus" . }}:{{ $.Values.backend.port }};
    }

    location /version {
        return 200 '{{ $.Values.deploy.version}}';
    }

    location /deploy/timestamp {
        return 200 '{{ $.Values.deploy.timestamp }}';
    }

    location / {
        root   /usr/share/nginx/html;
        try_files $uri $uri/ /index.html;
    }
}
{{- end }}
