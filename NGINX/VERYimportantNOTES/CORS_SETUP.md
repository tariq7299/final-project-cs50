# YOu can setup CORS, by two methods

## 2- Using NGINX
```
server {

    listen 80;
    server_name  197.57.100.1;

    location /api {

        add_header Access-Control-Allow-Origin "$http_origin";
        add_header Access-Control-Allow-Methods "OPTIONS, POST, GET";
        add_header Access-Control-Max-Age "3600";
        add_header Access-Control-Allow-Credentials "true";
        add_header Access-Control-Allow-Headers "Content-Type";
        set $test  "A";

        if ($request_method = 'OPTIONS') {
            set $test  "${test}B";
        }

        if ($test = "AB") {
            add_header Access-Control-Allow-Origin "$http_origin";
            add_header Access-Control-Allow-Methods "OPTIONS, DELETE, POST, GET, PATCH, PUT";
            add_header Access-Control-Max-Age "3600";
            add_header Access-Control-Allow-Credentials "true";
            add_header Access-Control-Allow-Headers "Content-Type";
            return 204;
        }
        if ($test = "B") {
            return 403;
        }

        proxy_pass http://flask-backend;
        proxy_http_version  1.1;
        proxy_cache_bypass  $http_upgrade;
        proxy_set_header Upgrade           $http_upgrade;
        proxy_set_header Connection        "upgrade";
        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host  $host;
        proxy_set_header X-Forwarded-Port  $server_port;
    }
}
```

## 1- Using FLASK_CORS

```
from flask_cors import CORS
CORS(app, resources={r'/api/*': {"origins": "*"}}, supports_credentials=True)
# Also it is better to speciy the actuall origin IP like this 
    # CORS(app, resources={r'/api/*': {'origins': 'http://197.57.100.1:80'}}, supports_credentials=True)

```



## When you change the IP of server
So lets say you have want to run your app on a public IP address instead of your local IP address
So you have to change these:

### 1
*In nginx.conf*

`server_name <Public IPWithout "http://">`

- Also don't forget to add the CORS headers, and you can do this by two ways 
1- Specifying the origin IP address, and add headers to it only

        ```
            location /api {

                if ($http_origin ~* "^http://197.57.100.1$") {
                    add_header Access-Control-Allow-Origin "$http_origin";
                    add_header Access-Control-Allow-Methods "OPTIONS, POST, GET";
                    add_header Access-Control-Max-Age "3600";
                    add_header Access-Control-Allow-Credentials "true";
                    add_header Access-Control-Allow-Headers "Content-Type";
                    set $test  "A";
                }
                if ($request_method = 'OPTIONS') {
                    set $test  "${test}B";
                }

                if ($test = "AB") {
                    add_header Access-Control-Allow-Origin "$http_origin";
                    add_header Access-Control-Allow-Methods "OPTIONS, DELETE, POST, GET, PATCH, PUT";
                    add_header Access-Control-Max-Age "3600";
                    add_header Access-Control-Allow-Credentials "true";
                    add_header Access-Control-Allow-Headers "Content-Type";
                    return 204;
                }
                if ($test = "B") {
                    return 403;
                }
                proxy_pass http://flask-backend;
                proxy_http_version  1.1;
                proxy_cache_bypass  $http_upgrade;
                proxy_set_header Upgrade           $http_upgrade;
                proxy_set_header Connection        "upgrade";
                proxy_set_header Host              $host;
                proxy_set_header X-Real-IP         $remote_addr;
                proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
                proxy_set_header X-Forwarded-Proto $scheme;
                proxy_set_header X-Forwarded-Host  $host;
                proxy_set_header X-Forwarded-Port  $server_port;
            }
        ```

**OR**

2- Add headers to any oringin

        ```
            location /api {
                add_header Access-Control-Allow-Origin "$http_origin";
                add_header Access-Control-Allow-Methods "OPTIONS, POST, GET";
                add_header Access-Control-Max-Age "3600";
                add_header Access-Control-Allow-Credentials "true";
                add_header Access-Control-Allow-Headers "Content-Type";
                set $test  "A";
                if ($request_method = 'OPTIONS') {
                    set $test  "${test}B";
                }

                if ($test = "AB") {
                    add_header Access-Control-Allow-Origin "$http_origin";
                    add_header Access-Control-Allow-Methods "OPTIONS, DELETE, POST, GET, PATCH, PUT";
                    add_header Access-Control-Max-Age "3600";
                    add_header Access-Control-Allow-Credentials "true";
                    add_header Access-Control-Allow-Headers "Content-Type";
                    return 204;
                }
                if ($test = "B") {
                    return 403;
                }
                proxy_pass http://flask-backend;
                proxy_http_version  1.1;
                proxy_cache_bypass  $http_upgrade;
                proxy_set_header Upgrade           $http_upgrade;
                proxy_set_header Connection        "upgrade";
                proxy_set_header Host              $host;
                proxy_set_header X-Real-IP         $remote_addr;
                proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
                proxy_set_header X-Forwarded-Proto $scheme;
                proxy_set_header X-Forwarded-Host  $host;
                proxy_set_header X-Forwarded-Port  $server_port;
            }
        ```

### 2
*The AJAX request from frontend to api*
Make the requests point to the same Public IP as the Frontend
`VUE_APP_API_BASE_URL=http://197.57.100.1/api`