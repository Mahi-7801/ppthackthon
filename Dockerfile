FROM node:22-alpine

WORKDIR /app

# Copy backend package dependencies and install
COPY backend/package*.json ./
RUN npm install --production

# Copy backend application code
COPY backend/ ./

# Expose server port
EXPOSE 3001

# Run SecureSign backend server
CMD ["node", "server.js"]
