// ingestion-engine/internal/domain/reading.go

/*
Package domain defines the core business objects and logic for the Ingestion Engine.
It contains the data structures for Energy Readings and the logic to simulate
realistic meter behavior.
*/
package domain

import (
	"math"
	"time"
)

// EnergyReading represents a single telemetry packet from a smart meter.
// It is tagged with JSON for OData/Power Platform compatibility.
type EnergyReading struct {
	DeviceID  string    `json:"deviceId"`  // Unique Identifier (e.g., "METER-001")
	Timestamp time.Time `json:"timestamp"` // ISO 8601 Timestamp
	Value     float64   `json:"value"`     // Energy consumption in kWh
	Unit      string    `json:"unit"`      // Unit of measurement
	Status    string    `json:"status"`    // "Normal", "Peak", "Maintenance"
}

// GenerateSimulatedValue creates a realistic energy reading based on time of day.
// We use a Sine wave function to simulate daily consumption patterns (higher in day, lower at night).
// baseLoad: The minimum constant usage.
// volatility: Random variance to make it look "live".
func GenerateSimulatedValue(deviceID string, t time.Time) EnergyReading {
	// Convert time to a float representation of hours (0.0 to 24.0)
	hour := float64(t.Hour()) + float64(t.Minute())/60.0

	// Logic: Sine wave peaking at 14:00 (14.0)
	// Function: A * sin(B * (x - C)) + D
	// Period is 24 hours.
	amplitude := 10.0
	period := (2 * math.Pi) / 24.0
	phaseShift := 14.0    // Peak at 2pm
	verticalShift := 15.0 // Base load

	// Calculate usage
	usage := amplitude*math.Sin(period*(hour-phaseShift)) + verticalShift

	// Add slight randomness (Volatility)
	// In a real app, we'd use crypto/rand, but math/rand is fine for simulation speed.
	// We are keeping it deterministic here for simplicity of the "Summer Trainee" scope.

	status := "Normal"
	if usage > 22.0 {
		status = "Peak"
	}

	return EnergyReading{
		DeviceID:  deviceID,
		Timestamp: t,
		Value:     math.Round(usage*100) / 100, // Round to 2 decimal places
		Unit:      "kWh",
		Status:    status,
	}
}
