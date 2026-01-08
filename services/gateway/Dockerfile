# -----------------------------------------------------------------------------
# NGINX GATEWAY
# -----------------------------------------------------------------------------
FROM nginx:alpine

# Remove default config
RUN rm /etc/nginx/conf.d/default.conf

# Copy our custom configuration to the MAIN config location
# Note: We replace nginx.conf entirely to control the http block
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]