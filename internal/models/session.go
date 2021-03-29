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

type StopLossRequest struct {
	Trailing bool    `json:"trailing"`
	Percent  float64 `json:"percent"`
}

type SessionStartRequest struct {
	StrategyID string           `json:"strategy_id"`
	StopLoss   *StopLossRequest `json:"stoploss"`
}
