FROM nginx:1.25

# Removing old nginx config files
RUN rm etc/nginx/conf.d/default.conf
# Copying new nginx config files
COPY nginx.conf etc/nginx/conf.d