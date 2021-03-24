//go:generate mockgen -package=mocks -destination=../mocks/service.go github.com/Action-for-Racial-Justice/Cortex-backend/internal/service Service

package service

import (
	"github.com/google/wire"

	logger "github.com/volatrade/currie-logs"
	stats "github.com/volatrade/k-stats"

	"github.com/volatrade/volatrader/internal/strategies"
)

//Module to denote wire binding function
var Module = wire.NewSet(
	New,
)

//Service interface to describe VolatraderService struct receiver functions
type Service interface {
}

//VolatraderService struct to hold relevant inner data members and hold functions for business logic
type VolatraderService struct {
	logger     *logger.Logger
	kstats     stats.Stats
	strategies strategies.Strategies
}

//New ... constructor
func New(logger *logger.Logger, kstats stats.Stats, strategies strategies.Strategies) *VolatraderService {

	return &VolatraderService{
		logger:     logger,
		kstats:     kstats,
		strategies: strategies,
	}
}
