FROM nginx:1.17.10-alpine

ADD dist/ /usr/share/nginx/html/
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
