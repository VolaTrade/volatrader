package streamer

import (
	"context"
	"fmt"
	"time"

	"github.com/google/uuid"
	"github.com/google/wire"

	logger "github.com/volatrade/currie-logs"
	"github.com/volatrade/go-errors/apierrors"
	"github.com/volatrade/volatrader/internal/models"
	"github.com/volatrade/volatrader/internal/tscommunicator"
)

var Module = wire.NewSet(
	New,
)

type Config struct {
	CommunicatorCount int
}

type Streamer interface {
	AddSession(indicators []string, sessionID string,
		updateChan chan models.IndicatorUpdate, deathChan chan bool,
	)
	IndicatorUpdate(iu models.IndicatorUpdate) (*models.CommMessage, error)
	DeleteTradeSession(sessionID string)
}

type VTStreamer struct {
	config            *Config
	commChannel       chan models.IndicatorUpdate
	relayChannel      chan models.CommMessage
	deathMap          map[string]chan bool
	indicatorSessions map[string]map[string]chan models.IndicatorUpdate
	commMap           map[string]*tscommunicator.VTTSCommunicator
}

func New(cfg *Config, logger *logger.Logger) (*VTStreamer, func()) {

	commChannel := make(chan models.IndicatorUpdate)
	relayChannel := make(chan models.CommMessage)
	commMap := make(map[string]*tscommunicator.VTTSCommunicator, cfg.CommunicatorCount)

	ctx, end := context.WithCancel(context.Background())
	for i := 0; i < cfg.CommunicatorCount; i++ {
		commID := uuid.New()
		comm := tscommunicator.New(commID, logger, commChannel, relayChannel)
		commMap[commID.String()] = comm
		go comm.WaitAndSlave(ctx)
	}

	return &VTStreamer{
		config:            cfg,
		commChannel:       commChannel,
		relayChannel:      relayChannel,
		deathMap:          make(map[string]chan bool, 0),
		indicatorSessions: make(map[string]map[string]chan models.IndicatorUpdate, 0),
		commMap:           commMap,
	}, end

}

func (vts *VTStreamer) AddSession(indicators []string, sessionID string,
	updateChan chan models.IndicatorUpdate, deathChan chan bool,
) {
	vts.deathMap[sessionID] = deathChan
	for _, indicator := range indicators {

		if _, ok := vts.indicatorSessions[indicator]; !ok {
			vts.indicatorSessions[indicator] = make(map[string]chan models.IndicatorUpdate, 0)
		}
		if _, ok := vts.indicatorSessions[indicator][sessionID]; !ok {
			vts.indicatorSessions[indicator][sessionID] = updateChan
		}
	}

	for _, commStruct := range vts.commMap {
		commStruct.UpdateSessionMap(vts.indicatorSessions)
	}
}

func (svc *VTStreamer) DeleteTradeSession(sessionID string) {

	for _, sessionProcMap := range svc.indicatorSessions {

		if _, ok := sessionProcMap[sessionID]; ok {
			delete(sessionProcMap, sessionID)
		}
	}
}

func (vts *VTStreamer) IndicatorUpdate(iu models.IndicatorUpdate) (*models.CommMessage, error) {
	vts.commChannel <- iu
	timer := time.NewTimer(1 * time.Second)
	defer timer.Stop()
	select {

	case commMessage := <-vts.relayChannel:
		return &commMessage, nil

	case <-timer.C:
		return nil, apierrors.NewError(
			apierrors.InternalErrorType,
			"Timeout trying to wait for verification").
			WithExternalMessage(fmt.Sprintf("Indicator update failed: %+v", iu))
	}
}
