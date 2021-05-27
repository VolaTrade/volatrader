//go:generate mockgen -package=mocks -destination=../mocks/service.go github.com/Action-for-Racial-Justice/Cortex-backend/internal/service Service

package service

import (
	"github.com/google/wire"

	logger "github.com/volatrade/currie-logs"
	stats "github.com/volatrade/k-stats"

	"github.com/volatrade/volatrader/internal/models"
	"github.com/volatrade/volatrader/internal/strategies"
	"github.com/volatrade/volatrader/internal/streamer"
)

//Module to denote wire binding function
var Module = wire.NewSet(
	New,
)

//Service interface to describe VolatraderService struct receiver functions
type Service interface {
	IndicatorUpdate(iu models.IndicatorUpdate) (*models.CommMessage, error)
	KillSessionRoutine(sessionID string) error
	StartSessionRoutine(startRequest models.SessionStartRequest) (string, error)
}

//VolatraderService struct to hold relevant inner data members and hold functions for business logic
type VolatraderService struct {
	logger     *logger.Logger
	kstats     stats.Stats
	strategies strategies.Strategies
	streamer   streamer.Streamer
}

//New ... constructor
func New(logger *logger.Logger, sr streamer.Streamer,
	kstats stats.Stats, strategies strategies.Strategies) *VolatraderService {

	return &VolatraderService{
		logger:     logger,
		kstats:     kstats,
		streamer:   sr,
		strategies: strategies,
	}
}
