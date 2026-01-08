# ingestion-engine/Dockerfile

# -----------------------------------------------------------------------------
# BUILD STAGE
# -----------------------------------------------------------------------------
FROM golang:1.21-alpine AS builder

WORKDIR /app

# Copy dependency files
COPY go.mod ./
# (Optional) COPY go.sum ./

# Copy source code
COPY . .

# Build the binary
# We explicitly point to the main file in cmd/server
RUN CGO_ENABLED=0 GOOS=linux go build -o main ./cmd/server/main.go

# -----------------------------------------------------------------------------
# RUN STAGE
# -----------------------------------------------------------------------------
FROM alpine:latest

WORKDIR /root/

# Copy binary from builder
COPY --from=builder /app/main .

# Expose the internal port
EXPOSE 8080

# Run the simulator
CMD ["./main"]