package models

import (
	"time"
)

type IndicatorUpdate struct {
	Indicator string  `json:"indicator"`
	Value     float64 `json:"value"`
}

type SessionStartResponse struct {
	SessionID string    `json:"session_id"`
	StartTime time.Time `json:"start_time"`
}
