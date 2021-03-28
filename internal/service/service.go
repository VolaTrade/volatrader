//go:generate mockgen -package=mocks -destination=../mocks/service.go github.com/Action-for-Racial-Justice/Cortex-backend/internal/service Service

package service

import (
	"github.com/google/uuid"
	"github.com/google/wire"

	logger "github.com/volatrade/currie-logs"
	stats "github.com/volatrade/k-stats"

	"github.com/volatrade/volatrader/internal/models"
	"github.com/volatrade/volatrader/internal/strategies"
	"github.com/volatrade/volatrader/internal/tscommunicator"
	"github.com/volatrade/volatrader/internal/tsprocessor"
)

//Module to denote wire binding function
var Module = wire.NewSet(
	New,
)

type Config struct {
	CommunicatorCount int
}

//Service interface to describe VolatraderService struct receiver functions
type Service interface {
	AddSession(indicators []string, sessionID string,
		sessionProcessor *tsprocessor.TSProcessor,
	)
	DeleteTradeSession(sessionID string)
	IndicatorUpdate(iu models.IndicatorUpdate) (*models.CommMessage, error)
	KillSessionRoutine(sessionID string) error
	StartSessionRoutine(strategyID string) (string, error)
}

//VolatraderService struct to hold relevant inner data members and hold functions for business logic
type VolatraderService struct {
	config            *Config
	logger            *logger.Logger
	kstats            stats.Stats
	strategies        strategies.Strategies
	sessionProcesses  map[string]*tsprocessor.TSProcessor
	indicatorSessions map[string]map[string]*tsprocessor.TSProcessor
	commChannel       chan models.IndicatorUpdate
	relayChannel      chan models.CommMessage
	commMap           map[string]*tscommunicator.VTTSCommunicator
}

//New ... constructor
func New(cfg *Config, logger *logger.Logger,
	kstats stats.Stats, strategies strategies.Strategies) *VolatraderService {

	commChannel := make(chan models.IndicatorUpdate)
	relayChannel := make(chan models.CommMessage)
	commMap := make(map[string]*tscommunicator.VTTSCommunicator, cfg.CommunicatorCount)

	for i := 0; i < cfg.CommunicatorCount; i++ {
		commID := uuid.New()
		comm := tscommunicator.New(commID, logger, commChannel, relayChannel)
		commMap[commID.String()] = comm
		go comm.WaitAndSlave()
	}
	return &VolatraderService{
		config:            cfg,
		commChannel:       commChannel,
		commMap:           commMap,
		logger:            logger,
		kstats:            kstats,
		relayChannel:      relayChannel,
		strategies:        strategies,
		sessionProcesses:  make(map[string]*tsprocessor.TSProcessor, 0),
		indicatorSessions: make(map[string]map[string]*tsprocessor.TSProcessor, 0),
	}
}
