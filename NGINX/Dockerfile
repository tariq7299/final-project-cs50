# production stage for NGINX
# FROM nginx:stable-alpine as production-stage
# COPY --from=build-stage /app/dist /usr/share/nginx/html
# COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf
# EXPOSE 80
# CMD ["nginx", "-g", "daemon off;"]

# FROM nginx

# RUN apt-get update

# # Install the iputils-ping package
# RUN apt-get install -y iputils-ping

# # Install the inetutils-traceroute package
# RUN apt-get install -y inetutils-traceroute

# # Install the iproute2 package
# RUN apt-get install -y iproute2

# # Install the curl, telnet, dnsutils, and vim packages
# RUN apt-get install -y curl telnet dnsutils vim

# start from the Nginx image
FROM nginx

RUN apt-get update

# Install the iputils-ping package
RUN apt-get install -y iputils-ping

# Install the inetutils-traceroute package
RUN apt-get install -y inetutils-traceroute

# Install the iproute2 package
RUN apt-get install -y iproute2

# Install the curl, telnet, dnsutils, and vim packages
RUN apt-get install -y curl telnet dnsutils vim
# copy custom Nginx configuration file

COPY nginx.conf /etc/nginx/nginx.conf

COPY  ./app/dist /usr/share/nginx/html

