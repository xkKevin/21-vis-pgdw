{{- define "pgdw-app.config.nginx.conf" -}}
server {
    listen       80;
    server_name  localhost;
    client_max_body_size 1000m;

    location ~ ^/api {
        proxy_set_header HOST $host;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_connect_timeout 600;
        proxy_read_timeout 600;
        proxy_send_timeout 600;
        send_timeout 600;
        client_body_timeout 300;
        rewrite ^/api/(.*) /$1 break;
        proxy_pass https://{{ $.Values.backend.host }}:{{ $.Values.backend.port }};
    }

    location /socket.io/ {
        proxy_pass http://{{ $.Values.websocket.host }}:{{ $.Values.websocket.port }}{{ $.Values.websocket.path }};

        proxy_http_version 1.1;
        proxy_read_timeout 600s;
        proxy_redirect off;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host:$server_port;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header REMOTE-HOST $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /version {
        return 200 '{{ $.Chart.AppVersion }}';
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
