# -----------------------------------------------------------------------------
# NODE BUILD ENVIRONMENT
# -----------------------------------------------------------------------------
FROM node:18-alpine

WORKDIR /app

COPY package.json ./
# RUN npm install

COPY . .

EXPOSE 3000

# CMD ["npm", "start"]
# Temporary CMD to keep container alive during Phase 1
CMD ["tail", "-f", "/dev/null"]