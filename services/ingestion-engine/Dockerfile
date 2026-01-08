# -----------------------------------------------------------------------------
# BUILD STAGE
# Use official Go image to compile the binary.
# -----------------------------------------------------------------------------
FROM golang:1.21-alpine AS builder

WORKDIR /app

# Copy dependency files first (caching layer)
COPY go.mod ./
# If go.sum exists, copy it. If not, this line is skipped without error in newer buildkit
# For now, we just initialize mod.

# Copy source code
COPY . .

# Build the binary. 
# We point to cmd/server/main.go which will be created in Phase 2.
# RUN go build -o main ./cmd/server/main.go 
# NOTE: Commented out for Phase 1 until code exists, replacing with a sleep for skeleton testing
RUN echo "Building Placeholder" > main

# -----------------------------------------------------------------------------
# RUN STAGE
# Use a lightweight scratch or alpine image for production.
# -----------------------------------------------------------------------------
FROM alpine:latest

WORKDIR /root/

COPY --from=builder /app/main .

# Expose the internal port
EXPOSE 8080

# Command to run the binary
# CMD ["./main"]
# Temporary CMD to keep container alive during Phase 1
CMD ["tail", "-f", "/dev/null"]