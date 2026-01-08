// services/ingestion-engine/cmd/server/main.go

/*
Main entry point for the Ingestion Engine Microservice.
Responsible for dependency injection and server startup.
*/
package main

import (
	"fmt"
	"log"
	"net/http"
	"os"
	"time"

	"powergrid/ingestion/internal/api"
	"powergrid/ingestion/internal/domain"
)

func main() {
	// 1. Configuration
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	// 2. Initialize Domain Services
	simulator := domain.NewSimulator()

	// Start Simulation: 50 meters, updating every 2 seconds
	// In a real scenario, this would be 10,000+ meters.
	simulator.Start(50, 2*time.Second)

	// 3. Initialize API Handlers
	handler := &api.Handler{Sim: simulator}

	// 4. Setup Router (Standard Library)
	mux := http.NewServeMux()
	mux.HandleFunc("/api/energy/telemetry", handler.GetTelemetry) // Specific path for Gateway routing
	mux.HandleFunc("/health", handler.HealthCheck)

	// 5. Start Server
	serverAddr := fmt.Sprintf(":%s", port)
	log.Printf("🚀 Ingestion Engine starting on %s...", serverAddr)
	log.Printf("📡 Endpoint: http://localhost%s/api/energy/telemetry", serverAddr)

	if err := http.ListenAndServe(serverAddr, mux); err != nil {
		log.Fatalf("❌ Server failed: %v", err)
	}
}
