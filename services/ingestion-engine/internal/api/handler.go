// ingestion-engine/internal/api/handler.go

/*
Package api handles HTTP requests and responses.
It adheres to REST principles and outputs JSON compatible with OData/PowerPlatform.
*/
package api

import (
	"encoding/json"
	"net/http"
	"powergrid/ingestion/internal/domain"
)

// Handler holds dependencies for the API.
type Handler struct {
	Sim *domain.Simulator
}

// GetTelemetry handles GET /telemetry
// Returns an array of current meter readings.
func (h *Handler) GetTelemetry(w http.ResponseWriter, r *http.Request) {
	// Handle Preflight requests
	if r.Method == "OPTIONS" {
		w.WriteHeader(http.StatusOK)
		return
	}

	// 2. Fetch Data (Thread-safe)
	data := h.Sim.GetAllReadings()

	// 3. Encode JSON
	w.Header().Set("Content-Type", "application/json")
	if err := json.NewEncoder(w).Encode(data); err != nil {
		http.Error(w, "Failed to encode telemetry", http.StatusInternalServerError)
	}
}

// HealthCheck for Azure App Service readiness probes
func (h *Handler) HealthCheck(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK)
	w.Write([]byte("OK"))
}
