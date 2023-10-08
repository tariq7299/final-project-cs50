

## A Note about `location / {}` in NGINX

location / {}
- NGINX forwards any request that has the same URL as origin URL and ends with \ to what ever to define above in `upstream {}`

*so for example*
```
http {
    upstream flask-backend {
        server 192.168.2.10:8080;
    }
    server {

        listen 80;
        server_name  197.57.100.1;
        location /api {        
            proxy_pass http://flask-backend;
        }
    }
}

# so any request comining from 197.57.100.1/api will be forwarded to 192.168.2.10:8080
```
## A note about docker-compose
- WHen you exec docker-compose up
*Watch the terninal closly and you can see eny errors with some really usefull messages*