# -----------------------------------------------------------------------------
# NGINX GATEWAY
# -----------------------------------------------------------------------------
FROM nginx:alpine

# Remove default nginx config
RUN rm /etc/nginx/conf.d/default.conf

# Copy our custom gateway config (Created in Phase 4)
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]