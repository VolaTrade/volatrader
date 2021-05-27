//tsprocessor --> Trade Session Communication package
package tscommunicator

import (
	"fmt"
	"sync"

	"context"

	"github.com/google/uuid"
	logger "github.com/volatrade/currie-logs"
	"github.com/volatrade/volatrader/internal/models"
)

type TSCommunicator interface {
}

type VTTSCommunicator struct {
	id                  uuid.UUID
	logger              *logger.Logger
	mux                 *sync.RWMutex
	indicatorSessionMap map[string]map[string]map[string]chan models.IndicatorUpdate
	indicatorChannel    chan models.IndicatorUpdate
	relayChannel        chan models.CommMessage
}

func New(id uuid.UUID, logger *logger.Logger,
	svcChan chan models.IndicatorUpdate, relayChannel chan models.CommMessage) *VTTSCommunicator {
	return &VTTSCommunicator{
		id:                  id,
		logger:              logger,
		mux:                 &sync.RWMutex{},
		relayChannel:        relayChannel,
		indicatorChannel:    svcChan,
		indicatorSessionMap: make(map[string]map[string]map[string]chan models.IndicatorUpdate),
	}

}

func (com *VTTSCommunicator) UpdateSessionMap(newMap map[string]map[string]map[string]chan models.IndicatorUpdate) {
	com.mux.Lock()
	com.indicatorSessionMap = newMap
	com.mux.Unlock()
}

func (com *VTTSCommunicator) WaitAndSlave(ctx context.Context) {
	com.logger.Infow("Starting communicator slave process", "ID", com.id.String())
	for {
		select {

		case <-ctx.Done():
			return

		case indUpdate := <-com.indicatorChannel:
			relayMessage := models.CommMessage{ID: com.id.String()}
			com.mux.RLock()
			if sessionProcMap, ok := com.indicatorSessionMap[indUpdate.Pair][indUpdate.Indicator]; ok {
				for _, processChannel := range sessionProcMap {
					processChannel <- indUpdate
				}
			} else {
				relayMessage.Error = fmt.Errorf(fmt.Sprintf("Could not find indicator %s", indUpdate.Indicator))
			}
			com.mux.RUnlock()
			com.relayChannel <- relayMessage

		}
	}
}
