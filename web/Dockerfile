# web/Dockerfile

FROM node:20-alpine

WORKDIR /app

# Add node_modules/.bin to the system path
ENV PATH /app/node_modules/.bin:$PATH

# Install Dependencies
COPY package.json ./
# package-lock.json might not exist if you just ran npm install, 
# but usually it's good to copy if present.
COPY package-lock.json ./ 
RUN npm install

# Copy source
COPY . .

# Vite default port is 5173, but we configured it to 3000 in vite.config.ts
EXPOSE 3000

# CHANGED: "npm start" usually runs "react-scripts start". 
# We changed package.json scripts so "dev" runs "vite".
CMD ["npm", "run", "dev"]