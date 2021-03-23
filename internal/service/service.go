//go:generate mockgen -package=mocks -destination=../mocks/service.go github.com/Action-for-Racial-Justice/Cortex-backend/internal/service Service

package service

import (
	"github.com/google/wire"

	logger "github.com/volatrade/currie-logs"
	stats "github.com/volatrade/k-stats"
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
	logger *logger.Logger
	kstats stats.Stats
}

//New ... constructor
func New(logger *logger.Logger, kstats stats.Stats) *VolatraderService {

	return &VolatraderService{
		logger: logger,
		kstats: kstats,
	}
}
